from __future__ import annotations

import ctypes
import time


WM_GETTEXT = 0x000D
WM_GETTEXTLENGTH = 0x000E
WM_SETTEXT = 0x000C
EM_SETSEL = 0x00B1
EM_REPLACESEL = 0x00C2
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_CHAR = 0x0102
VK_RETURN = 0x0D

user32 = ctypes.windll.user32


class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]


def _window_text(hwnd: int) -> str:
    buf = ctypes.create_unicode_buffer(512)
    user32.GetWindowTextW(hwnd, buf, 512)
    return buf.value


def _window_rect(hwnd: int) -> RECT:
    rect = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect


def _window_width(hwnd: int) -> int:
    r = _window_rect(hwnd)
    return int(r.right - r.left)


def _window_height(hwnd: int) -> int:
    r = _window_rect(hwnd)
    return int(r.bottom - r.top)


def _window_visible(hwnd: int) -> bool:
    return bool(user32.IsWindowVisible(hwnd))


def _window_enabled(hwnd: int) -> bool:
    return bool(user32.IsWindowEnabled(hwnd))


def _enum_windows() -> list[int]:
    handles: list[int] = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def _cb(hwnd, _lparam):
        handles.append(int(hwnd))
        return True

    user32.EnumWindows(_cb, 0)
    return handles


def _enum_child_hwnds(parent_hwnd: int) -> list[int]:
    children: list[int] = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def _cb(hwnd, _lparam):
        children.append(int(hwnd))
        return True

    user32.EnumChildWindows(parent_hwnd, _cb, 0)
    return children


def _class_name(hwnd: int) -> str:
    buf = ctypes.create_unicode_buffer(128)
    user32.GetClassNameW(hwnd, buf, 128)
    return buf.value


def _find_eps_main_window(title_hint: str) -> int:
    # Prefer real EPS MDI windows and avoid unrelated shell/explorer windows.
    candidates: list[tuple[int, int]] = []

    for hwnd in _enum_windows():
        if not _window_visible(hwnd):
            continue

        title = _window_text(hwnd)
        if not title:
            continue
        tl = title.lower()
        if title_hint.lower() not in tl:
            continue

        cls = _class_name(hwnd)
        cls_l = cls.lower()

        # Skip known non-EPS classes that can contain "eps" text in captions.
        if (
            "chrome_widget" in cls_l
            or "qt" in cls_l
            or cls_l in {"cabinetwclass", "explorewclass", "workerw"}
            or cls_l.startswith("shell_")
        ):
            continue

        w = _window_width(hwnd)
        h = _window_height(hwnd)
        # EPS main window can be resized small; only filter out tiny utility windows.
        if w < 420 or h < 220:
            continue

        score = 0
        if "eps2016(" in tl or "eps2026(" in tl:
            score += 30
        if ".edb" in tl:
            score += 20
        if cls.startswith("Afx:"):
            score += 15
        if "eps" in tl:
            score += 5
        score += min(w // 200, 10)

        candidates.append((score, hwnd))

    if not candidates:
        return 0

    candidates.sort(reverse=True)
    return candidates[0][1]


def _find_command_input_hwnd(main_hwnd: int) -> int:
    # Command input is typically the bottom, wide Edit (height around one-line input).
    main_rect = _window_rect(main_hwnd)
    bottom_threshold = int(main_rect.bottom - 140)

    candidates: list[int] = []
    for hwnd in _enum_child_hwnds(main_hwnd):
        if _class_name(hwnd) != "Edit":
            continue
        if not _window_visible(hwnd) or not _window_enabled(hwnd):
            continue

        rect = _window_rect(hwnd)
        w = int(rect.right - rect.left)
        h = int(rect.bottom - rect.top)

        if rect.top < bottom_threshold:
            continue
        if w < 500:
            continue
        if h < 14 or h > 40:
            continue
        candidates.append(hwnd)

    if candidates:
        # Prefer widest bottom line input.
        candidates.sort(key=lambda h: (_window_width(h), -_window_rect(h).top), reverse=True)
        return candidates[0]

    # Fallback: widest visible edit under EPS main window.
    fallback = [
        h for h in _enum_child_hwnds(main_hwnd)
        if _class_name(h) == "Edit" and _window_visible(h) and _window_enabled(h)
    ]
    if fallback:
        fallback.sort(key=_window_width, reverse=True)
        return fallback[0]

    return 0


def _get_text(hwnd: int) -> str:
    n = int(user32.SendMessageW(hwnd, WM_GETTEXTLENGTH, 0, 0))
    if n <= 0:
        return ""
    buf = ctypes.create_unicode_buffer(n + 1)
    user32.SendMessageW(hwnd, WM_GETTEXT, n + 1, buf)
    return buf.value


def send_command_to_eps(command: str, window_title: str = "EPS") -> bool:
    """Send a command to EPS command input and trigger Enter."""
    main_hwnd = _find_eps_main_window(window_title)
    if not main_hwnd:
        return False

    input_hwnd = _find_command_input_hwnd(main_hwnd)
    if not input_hwnd:
        return False

    user32.SetForegroundWindow(main_hwnd)
    time.sleep(0.05)
    user32.SetFocus(input_hwnd)
    time.sleep(0.03)

    # Clear previous content robustly before writing command.
    user32.SendMessageW(input_hwnd, EM_SETSEL, 0, -1)
    user32.SendMessageW(input_hwnd, EM_REPLACESEL, 1, ctypes.c_wchar_p(""))
    user32.SendMessageW(input_hwnd, WM_SETTEXT, 0, ctypes.c_wchar_p(command))
    time.sleep(0.06)

    if _get_text(input_hwnd) != command:
        return False

    # Use both WM_CHAR and key up/down for better compatibility with EPS command bar.
    user32.PostMessageW(input_hwnd, WM_CHAR, VK_RETURN, 0)
    user32.PostMessageW(input_hwnd, WM_KEYDOWN, VK_RETURN, 0)
    user32.PostMessageW(input_hwnd, WM_KEYUP, VK_RETURN, 0)
    return True
