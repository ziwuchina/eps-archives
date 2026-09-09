#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include <chrono>
#include <cstdint>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <mutex>
#include <sstream>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr wchar_t kLogPath[]       = L"D:\\EPS2026G\\Temp\\wz_ext_bridge.log";
constexpr wchar_t kTxtPath[]       = L"D:\\EPS2026G\\Temp\\wz_ext_probe.txt";
constexpr wchar_t kCsvPath[]       = L"D:\\EPS2026G\\Temp\\wz_ext_probe.csv";
constexpr wchar_t kPointsCsvPath[] = L"D:\\EPS2026G\\Temp\\wz_ext_points.csv";
constexpr wchar_t kCmdPath[]       = L"D:\\EPS2026G\\Temp\\wz_ext_cmd.txt";   // command intent from EPS
constexpr wchar_t kResultPath[]    = L"D:\\EPS2026G\\Temp\\wz_ext_result.txt"; // reply from DLL

const wchar_t* const kCandidateRawFiles[] = {
    L"D:\\EPS2026G\\Temp\\wz_ext_selection.txt",
    L"D:\\EPS2026G\\Temp\\wz_ext_selection.csv",
    L"D:\\EPS2026G\\Temp\\wz_sel_ext.txt",
    L"D:\\EPS2026G\\Temp\\eps_selection_ext.txt",
    L"D:\\EPS2026G\\Temp\\wz_ext_probe_raw.txt",
};

const wchar_t* const kCandidatePointFiles[] = {
    L"D:\\EPS2026G\\Temp\\wz_ext_points_raw.csv",
    L"D:\\EPS2026G\\Temp\\wz_ext_points_raw.txt",
    L"D:\\EPS2026G\\Temp\\wz_ext_selection_points.csv",
    L"D:\\EPS2026G\\Temp\\wz_ext_selection.csv",
    L"D:\\EPS2026G\\Temp\\wz_ext_selection.txt",
    L"D:\\EPS2026G\\Temp\\wz_sel_ext.txt",
    L"D:\\EPS2026G\\Temp\\eps_selection_ext.txt",
    L"D:\\EPS2026G\\Temp\\wz_ext_probe_raw.txt",
};

std::mutex g_logMutex;
std::mutex g_dispatchMutex;
std::string g_module_name;
std::unordered_set<std::string> g_registered_commands;

bool EnsureTempDir();
bool AppendLog(const char* function_name, const void* opaque_context, const std::string& detail);

struct PointRow {
    std::string point_no;
    std::string x;
    std::string y;
};

std::string CurrentTimestamp() {
    using clock = std::chrono::system_clock;
    const auto now = clock::now();
    const std::time_t now_c = clock::to_time_t(now);

    std::tm local_tm{};
    localtime_s(&local_tm, &now_c);

    std::ostringstream oss;
    oss << std::put_time(&local_tm, "%Y-%m-%d %H:%M:%S");
    return oss.str();
}

std::string WideToUtf8(const std::wstring& value) {
    if (value.empty()) {
        return std::string();
    }

    const int needed = WideCharToMultiByte(CP_UTF8, 0, value.c_str(), -1, nullptr, 0, nullptr, nullptr);
    if (needed <= 1) {
        return std::string();
    }

    std::string out(static_cast<size_t>(needed - 1), '\0');
    WideCharToMultiByte(CP_UTF8, 0, value.c_str(), -1, &out[0], needed, nullptr, nullptr);
    return out;
}

bool EnsureTempDir() {
    const wchar_t* temp_dir = L"D:\\EPS2026G\\Temp";
    if (CreateDirectoryW(temp_dir, nullptr) != 0) {
        return true;
    }

    const DWORD err = GetLastError();
    return err == ERROR_ALREADY_EXISTS;
}

bool WriteTextFileUtf8(const wchar_t* path, const std::string& content, bool bom) {
    std::ofstream out(path, std::ios::binary | std::ios::trunc);
    if (!out.is_open()) {
        return false;
    }

    if (bom) {
        const unsigned char utf8_bom[3] = {0xEF, 0xBB, 0xBF};
        out.write(reinterpret_cast<const char*>(utf8_bom), 3);
    }
    out.write(content.c_str(), static_cast<std::streamsize>(content.size()));
    return static_cast<bool>(out);
}

bool AppendLog(const char* function_name, const void* opaque_context, const std::string& detail) {
    std::lock_guard<std::mutex> lock(g_logMutex);

    std::ofstream log_stream(kLogPath, std::ios::app);
    if (!log_stream.is_open()) {
        return false;
    }

    log_stream << "[" << CurrentTimestamp() << "] "
               << function_name
               << " called, context=" << opaque_context
               << ", detail=" << detail
               << "\n";
    return static_cast<bool>(log_stream);
}

std::string TrimCopy(const std::string& input) {
    size_t first = 0;
    while (first < input.size() && (input[first] == ' ' || input[first] == '\t' || input[first] == '\r' || input[first] == '\n')) {
        ++first;
    }

    size_t last = input.size();
    while (last > first && (input[last - 1] == ' ' || input[last - 1] == '\t' || input[last - 1] == '\r' || input[last - 1] == '\n')) {
        --last;
    }

    return input.substr(first, last - first);
}

bool TryReadFile(const wchar_t* path, std::string* content_out) {
    std::ifstream in(path, std::ios::binary);
    if (!in.is_open()) {
        return false;
    }

    std::ostringstream oss;
    oss << in.rdbuf();
    *content_out = oss.str();
    return true;
}

std::vector<std::pair<std::string, std::string>> ParseKeyValueLines(const std::string& raw) {
    std::vector<std::pair<std::string, std::string>> rows;
    std::istringstream iss(raw);
    std::string line;

    while (std::getline(iss, line)) {
        const std::string trimmed = TrimCopy(line);
        if (trimmed.empty()) {
            continue;
        }

        size_t split = std::string::npos;
        for (const char delim : {'=', ':', '\t', ','}) {
            split = trimmed.find(delim);
            if (split != std::string::npos) {
                break;
            }
        }

        if (split == std::string::npos || split == 0 || split + 1 >= trimmed.size()) {
            rows.push_back(std::make_pair(std::string("line"), trimmed));
            continue;
        }

        std::string key = TrimCopy(trimmed.substr(0, split));
        std::string val = TrimCopy(trimmed.substr(split + 1));
        if (key.empty()) {
            key = "line";
        }
        rows.push_back(std::make_pair(key, val));
    }

    return rows;
}

std::vector<std::string> SplitByComma(const std::string& value) {
    std::vector<std::string> parts;
    std::string current;

    for (char ch : value) {
        if (ch == ',') {
            parts.push_back(TrimCopy(current));
            current.clear();
        } else {
            current.push_back(ch);
        }
    }
    parts.push_back(TrimCopy(current));
    return parts;
}

std::string NormalizePointLine(const std::string& line) {
    std::string out;
    out.reserve(line.size());
    for (unsigned char ch : line) {
        if (ch == '\t' || ch == ';' || ch == '|') {
            out.push_back(',');
        } else {
            out.push_back(static_cast<char>(ch));
        }
    }
    return out;
}

bool IsLikelyNumber(const std::string& text) {
    if (text.empty()) {
        return false;
    }

    size_t i = 0;
    if (text[i] == '+' || text[i] == '-') {
        ++i;
    }

    bool has_digit = false;
    bool has_dot = false;
    for (; i < text.size(); ++i) {
        const char c = text[i];
        if (c >= '0' && c <= '9') {
            has_digit = true;
            continue;
        }
        if (c == '.' && !has_dot) {
            has_dot = true;
            continue;
        }
        return false;
    }
    return has_digit;
}

std::vector<PointRow> ParsePointRows(const std::string& raw) {
    std::vector<PointRow> rows;
    std::istringstream iss(raw);
    std::string line;

    while (std::getline(iss, line)) {
        const std::string trimmed = TrimCopy(line);
        if (trimmed.empty()) {
            continue;
        }

        // Keep parsing rules strict to avoid polluting points CSV with non-coordinate rows.
        const std::string normalized = NormalizePointLine(trimmed);
        std::vector<std::string> parts = SplitByComma(normalized);
        if (parts.size() < 3) {
            continue;
        }

        const std::string pno = parts[0];
        const std::string x = parts[1];
        const std::string y = parts[2];
        if (pno.empty()) {
            continue;
        }

        if (x == "X" || x == "x" || y == "Y" || y == "y") {
            continue;
        }

        if (!IsLikelyNumber(x) || !IsLikelyNumber(y)) {
            continue;
        }

        PointRow row;
        row.point_no = pno;
        row.x = x;
        row.y = y;
        rows.push_back(row);
    }

    return rows;
}

std::string EscapeCsv(const std::string& value) {
    bool need_quote = false;
    for (char c : value) {
        if (c == ',' || c == '"' || c == '\n' || c == '\r') {
            need_quote = true;
            break;
        }
    }

    if (!need_quote) {
        return value;
    }

    std::string escaped;
    escaped.reserve(value.size() + 4);
    escaped.push_back('"');
    for (char c : value) {
        if (c == '"') {
            escaped.push_back('"');
        }
        escaped.push_back(c);
    }
    escaped.push_back('"');
    return escaped;
}

BOOL SafeProbeImpl(const char* function_name, const void* opaque_context) {
    try {
        if (!EnsureTempDir()) {
            (void)AppendLog(function_name, opaque_context, "EnsureTempDir failed");
            return FALSE;
        }

        std::string raw_payload;
        std::wstring hit_file;
        for (const wchar_t* candidate : kCandidateRawFiles) {
            if (TryReadFile(candidate, &raw_payload) && !raw_payload.empty()) {
                hit_file = candidate;
                break;
            }
        }

        const std::string ts = CurrentTimestamp();
        std::vector<std::pair<std::string, std::string>> kv_rows;
        if (!raw_payload.empty()) {
            kv_rows = ParseKeyValueLines(raw_payload);
        }

        if (kv_rows.empty()) {
            kv_rows.push_back(std::make_pair(std::string("status"), std::string("fallback_skeleton")));
            kv_rows.push_back(std::make_pair(std::string("reason"), std::string("no_stable_selection_file_or_no_parsable_data")));
        }

        std::vector<PointRow> point_rows;
        std::wstring points_hit_file;
        std::string points_reason;
        for (const wchar_t* candidate : kCandidatePointFiles) {
            std::string point_raw;
            if (!TryReadFile(candidate, &point_raw) || point_raw.empty()) {
                continue;
            }

            point_rows = ParsePointRows(point_raw);
            if (!point_rows.empty()) {
                points_hit_file = candidate;
                break;
            }
        }

        if (point_rows.empty()) {
            points_reason = "no_coordinate_candidate_or_no_parsable_point_rows";
            PointRow fallback;
            fallback.point_no = "SKELETON";
            fallback.x = "";
            fallback.y = "";
            point_rows.push_back(fallback);
        } else {
            points_reason = "ok";
        }

        std::ostringstream txt;
        txt << "WzExtBridge Probe Report\n";
        txt << "function=" << function_name << "\n";
        txt << "timestamp=" << ts << "\n";
        txt << "pid=" << GetCurrentProcessId() << "\n";
        txt << "tid=" << GetCurrentThreadId() << "\n";
        txt << "context=" << opaque_context << "\n";
        if (!hit_file.empty()) {
            txt << "source_file=" << WideToUtf8(hit_file) << "\n";
        } else {
            txt << "source_file=<none>\n";
        }
        if (!points_hit_file.empty()) {
            txt << "points_source_file=" << WideToUtf8(points_hit_file) << "\n";
        } else {
            txt << "points_source_file=<none>\n";
        }
        txt << "points_reason=" << points_reason << "\n";
        txt << "rows=" << kv_rows.size() << "\n";
        txt << "point_rows=" << point_rows.size() << "\n";
        txt << "\n";
        for (size_t i = 0; i < kv_rows.size(); ++i) {
            txt << kv_rows[i].first << "=" << kv_rows[i].second << "\n";
        }

        const std::string csv_header = WideToUtf8(L"\x5B57\x6BB5,\x503C");
        std::ostringstream csv;
        csv << csv_header << "\n";
        for (const auto& row : kv_rows) {
            csv << EscapeCsv(row.first) << "," << EscapeCsv(row.second) << "\n";
        }
        csv << "timestamp," << EscapeCsv(ts) << "\n";

        const std::string points_header = WideToUtf8(L"\x70B9\x53F7,X,Y");
        std::ostringstream points_csv;
        points_csv << points_header << "\n";
        for (const auto& point : point_rows) {
            points_csv << EscapeCsv(point.point_no) << "," << EscapeCsv(point.x) << "," << EscapeCsv(point.y) << "\n";
        }
        if (points_reason != "ok") {
            points_csv << "DIAG," << EscapeCsv(points_reason) << "," << "\n";
        }

        const bool txt_ok = WriteTextFileUtf8(kTxtPath, txt.str(), true);
        const bool csv_ok = WriteTextFileUtf8(kCsvPath, csv.str(), true);
        const bool points_ok = WriteTextFileUtf8(kPointsCsvPath, points_csv.str(), true);
        const bool log_ok = AppendLog(function_name, opaque_context,
            (txt_ok ? "txt=ok" : "txt=fail") + std::string(";") +
            (csv_ok ? "csv=ok" : "csv=fail") + std::string(";") +
            (points_ok ? "points=ok" : "points=fail") + std::string(";") +
            "points_reason=" + points_reason);

        return (txt_ok && csv_ok && points_ok && log_ok) ? TRUE : FALSE;
    } catch (...) {
        return FALSE;
    }
}

}  // namespace

bool SafeProbeLight(const char* function_name, const void* opaque_context) {
    try {
        EnsureTempDir();
        return AppendLog(function_name, opaque_context, "light=ok");
    } catch (...) {
        return false;
    }
}

bool TryReadAsciiPrintable(const void* ptr, std::string* out) {
    if (ptr == nullptr || out == nullptr) {
        return false;
    }

    out->clear();
#if defined(_MSC_VER)
    __try {
#endif
        const unsigned char* p = reinterpret_cast<const unsigned char*>(ptr);
        for (size_t seen = 0; seen < 256; ++seen, ++p) {
            const unsigned char ch = *p;
            if (ch == 0) {
                return !out->empty();
            }
            if ((ch < 0x20 || ch > 0x7E) && ch != '\t') {
                return false;
            }
            out->push_back(static_cast<char>(ch));
        }
        return false;
#if defined(_MSC_VER)
    } __except (EXCEPTION_EXECUTE_HANDLER) {
        out->clear();
        return false;
    }
#endif
}

bool ContainsProbeToken(const std::string& haystack) {
    return haystack.find("WzExtProbe") != std::string::npos ||
           haystack.find("wzextprobe") != std::string::npos ||
           haystack.find("WzExtProbeWithSelection") != std::string::npos;
}

// Writes the received command intent to a file so the OpenClaw agent (polling the
// Temp directory) can pick it up and drive the real logic.
bool WriteCommandRecord(const std::string& cmd, void* arg1, void* arg2, void* arg3) {
    (void)arg2;
    (void)arg3;

    std::ostringstream oss;
    oss << CurrentTimestamp() << "\n";
    oss << "cmd=" << cmd << "\n";
    oss << "arg1=" << (arg1 ? "present" : "null") << "\n";

    std::string text1;
    if (TryReadAsciiPrintable(arg1, &text1) && !text1.empty()) {
        oss << "text=" << text1 << "\n";
    }

    return WriteTextFileUtf8(kCmdPath, oss.str(), true);
}

int DispatchByCommandHints(const char* entry_name, void* arg1, void* arg2, void* arg3) {
    (void)arg3;

    // Some EPS flows invoke extension entry points with command names in arg1/arg2.
    // If we can see a probe command hint, route to the matching probe handler.
    std::string text1;
    std::string text2;
    const bool ok1 = TryReadAsciiPrintable(arg1, &text1);
    const bool ok2 = TryReadAsciiPrintable(arg2, &text2);

    std::string probe_hint;
    if (ok1) {
        probe_hint.assign(text1);
    }
    if (ok2) {
        probe_hint.append(" ");
        probe_hint.append(text2);
    }

    if (ContainsProbeToken(probe_hint)) {
        (void)WriteCommandRecord(probe_hint, arg1, arg2, arg3);
        if (probe_hint.find("WithSelection") != std::string::npos) {
            return SafeProbeImpl("WzExtProbeWithSelection(dispatch)", arg1) ? TRUE : FALSE;
        }
        return SafeProbeImpl("WzExtProbe(dispatch)", arg1) ? TRUE : FALSE;
    }

    // Keep unknown dispatches non-fatal; log for reverse-analysis and return success.
    (void)WriteCommandRecord(probe_hint, arg1, arg2, arg3);
    return SafeProbeImpl(entry_name, arg1) ? TRUE : FALSE;
}

std::string FirstPrintableArg(void* arg1, void* arg2, void* arg3) {
    std::string out;
    if (TryReadAsciiPrintable(arg1, &out)) {
        return out;
    }
    if (TryReadAsciiPrintable(arg2, &out)) {
        return out;
    }
    if (TryReadAsciiPrintable(arg3, &out)) {
        return out;
    }
    return std::string();
}

bool ContainsRegisteredCommandToken(const std::string& haystack) {
    std::lock_guard<std::mutex> lock(g_dispatchMutex);
    for (const auto& cmd : g_registered_commands) {
        if (!cmd.empty() && haystack.find(cmd) != std::string::npos) {
            return true;
        }
    }
    return false;
}

int RegisterCommandName(void* arg1, void* arg2, void* arg3) {
    const std::string cmd = FirstPrintableArg(arg1, arg2, arg3);
    if (cmd.empty()) {
        (void)AppendLog("RegisterCmd", arg1, "empty");
        return 1;
    }

    {
        std::lock_guard<std::mutex> lock(g_dispatchMutex);
        g_registered_commands.insert(cmd);
    }
    (void)AppendLog("RegisterCmd", arg1, cmd);
    return 1;
}

int ExecByRegisteredOrHint(void* arg1, void* arg2, void* arg3) {
    std::string text1;
    std::string text2;
    std::string text3;
    const bool ok1 = TryReadAsciiPrintable(arg1, &text1);
    const bool ok2 = TryReadAsciiPrintable(arg2, &text2);
    const bool ok3 = TryReadAsciiPrintable(arg3, &text3);

    std::string all;
    if (ok1) {
        all.append(text1);
    }
    if (ok2) {
        if (!all.empty()) {
            all.push_back(' ');
        }
        all.append(text2);
    }
    if (ok3) {
        if (!all.empty()) {
            all.push_back(' ');
        }
        all.append(text3);
    }

    // Always route to the probe handler — EPS's internal command registry doesn't
    // know about "wzbridgeprobe", so we intercept ALL ExecFunction calls and
    // check if the text looks like a probe command or any registered command.
    (void)WriteCommandRecord(all, arg1, arg2, arg3);
    if (ContainsProbeToken(all) || ContainsRegisteredCommandToken(all)) {
        return DispatchByCommandHints("ExecFunction(dispatch)", arg1, arg2, arg3);
    }

    return SafeProbeImpl("ExecFunction(unknown-cmd)", arg1) ? TRUE : FALSE;
}

// EPS command dispatcher calls exported command handlers as __cdecl with 3 pointer args.
// Keep this ABI to avoid stack corruption/crashes when invoking command-line entries.
extern "C" __declspec(dllexport) int __cdecl WzExtProbe(void* arg1, void* arg2, void* arg3) {
    (void)arg2;
    (void)arg3;
    (void)WriteCommandRecord("WzExtProbe", arg1, arg2, arg3);
    return SafeProbeImpl("WzExtProbe", arg1) ? 1 : 0;
}

extern "C" __declspec(dllexport) int __cdecl WzExtProbeWithSelection(void* arg1, void* arg2, void* arg3) {
    (void)arg2;
    (void)arg3;
    (void)WriteCommandRecord("WzExtProbeWithSelection", arg1, arg2, arg3);
    return SafeProbeImpl("WzExtProbeWithSelection", arg1) ? 1 : 0;
}

// EPS SDL/DLL loader checks for these legacy entry names on many modules.
// Return 0 — no dangerous CSDLInterface object needed.
extern "C" __declspec(dllexport) int __cdecl CreateInterface() {
    (void)EnsureTempDir();
    (void)AppendLog("CreateInterface", nullptr, "v-restored-returns-one");
    return 1;   // non-zero = success — EPS will then call RegisterCmd then ssExcuteFunction/ExecFunction
}

extern "C" __declspec(dllexport) int __cdecl SSInterfaceHandle() {
    return 0;
}

extern "C" __declspec(dllexport) int __cdecl GetSDLCommandInfo() {
    return 0;
}

// Legacy registration chain used by some EPS loadext flows.
extern "C" __declspec(dllexport) int __cdecl SetModulName(void* arg1, void* arg2, void* arg3) {
    const std::string module_name = FirstPrintableArg(arg1, arg2, arg3);
    {
        std::lock_guard<std::mutex> lock(g_dispatchMutex);
        g_module_name = module_name;
    }
    (void)EnsureTempDir();
    (void)AppendLog(module_name.empty() ? "SetModulName" : "SetModulName", nullptr, module_name);
    return 1;
}

extern "C" __declspec(dllexport) int __cdecl RegisterCmd(void* arg1, void* arg2, void* arg3) {
    return RegisterCommandName(arg1, arg2, arg3);
}

extern "C" __declspec(dllexport) int __cdecl ExecFunction(void* arg1, void* arg2, void* arg3) {
    return ExecByRegisteredOrHint(arg1, arg2, arg3);
}

// Compatibility shims: many modules are called through generic dispatcher names.
extern "C" __declspec(dllexport) int __cdecl ExecuteCommand(void* arg1, void* arg2, void* arg3) {
    return DispatchByCommandHints("ExecuteCommand", arg1, arg2, arg3);
}

extern "C" __declspec(dllexport) int __cdecl ExecuteCommandLine(void* arg1, void* arg2, void* arg3) {
    return DispatchByCommandHints("ExecuteCommandLine", arg1, arg2, arg3);
}

extern "C" __declspec(dllexport) int __cdecl ExecuteSDLFunction(void* arg1, void* arg2, void* arg3) {
    return DispatchByCommandHints("ExecuteSDLFunction", arg1, arg2, arg3);
}

extern "C" __declspec(dllexport) int __cdecl SDLFunctionExecute(void* arg1, void* arg2, void* arg3) {
    return DispatchByCommandHints("SDLFunctionExecute", arg1, arg2, arg3);
}

BOOL APIENTRY DllMain(HMODULE module, DWORD reason, LPVOID reserved) {
    (void)module;
    (void)reason;
    (void)reserved;
    return TRUE;
}
