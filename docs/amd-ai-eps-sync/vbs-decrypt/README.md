# V6_0307 — OCR Page Reconstruction Scripts

Batch processing scripts that assemble OCR-produced line CSV files into
reconstructed page files with special characters, page breaks, and
metadata tags.

## Overview

OCR scans produce one CSV file per page, listing the raw text content
of each line. These scripts reconcile the raw OCR output into clean
page files by:

1. Stripping blank/spacing-only lines from book-level CSVs
2. Building per-page metadata (line positions, spacing info)
3. Identifying single-line (1LINE) and double-line (2LINE) page types
4. Generating BND (boundary) tags and page metadata tags
5. Reconciling boundary markers with OCR book text

## Directory Layout

```
V6_0307/
├── books_raw_0/            # 50 raw OCR book CSVs (book1.csv .. book50.csv)
├── books_raw_1/            # 50 more raw OCR book CSVs
├── books_raw_2/            # 49 more raw OCR book CSVs
├── books_lines_0/          # 50 line-index CSVs (books_lines_1.csv .. books_lines_50.csv)
├── books_lines_1/          # 50 more line-index CSVs
├── books_lines_2/          # 49 more line-index CSVs
├── pages_raw_0/            # 250 raw page CSVs (page1.csv .. page250.csv)
├── pages_raw_1/            # 250 more raw page CSVs
├── pages_raw_2/            # 250 more raw page CSVs
├── pages_raw_3/            # 200 more raw page CSVs
├── pages_lines_0/          # 250 per-line metadata CSVs (lines-page1.csv ..)
├── pages_lines_1/          # 250 more per-line metadata CSVs
├── pages_lines_2/          # 250 more per-line metadata CSVs
├── pages_lines_3/          # 200 more per-line metadata CSVs
├── removed_lines_0/        # 250 blank-line CSVs (RemovedLinesN.csv)
├── removed_lines_1/        # 250 more blank-line CSVs
├── removed_lines_2/        # 250 more blank-line CSVs
├── removed_lines_3/        # 200 more blank-line CSVs
├── tags_0/                 # 250 tag CSVs (tag-1.csv .. tag-250.csv)
├── tags_1/                 # 250 more tag CSVs
├── tags_2/                 # 250 more tag CSVs
├── tags_3/                 # 200 more tag CSVs
├── books.bk                # Combined book metadata CSV
├── booksCombinedAll.bk     # Combined books-all CSV
├── booksCombinedAllLines.bk # Combined books-all lines CSV
├── page_data.csv           # Page data CSV
├── 00accsv.bat             # Reconcile: apply book lines to raw page CSVs
├── 00StripBooksToLines.bat # Strip all books and build line indices
├── 01runcsv.bat            # Apply line indices to raw page CSVs
├── action_build_include.bat # Build documentation
├── RUNALL.BAT              # Master script: runs steps 1–5 then final scripts
├── RunAll_1line.bat        # Run 1-line page assembly (all pages)
├── RunAll_2line.bat        # Run 2-line page assembly (all pages)
├── RunAll_page.bat         # Run standard page assembly (all pages)
├── manual_bnd1.bat         # Manual: Process all pages (main pipeline)
├── manual_bnd2.bat         # Manual: Apply BND boundary tags
├── manual_page.bat         # Manual: Apply page metadata tags
├── 1line_page.bat          # Manual: Assemble 1-line pages
├── 2line_page.bat          # Manual: Assemble 2-line pages
├── manual_rnd.bat          # Manual: Create testing/output directories
├── testing.csv             # Test data CSV
└── *.cs                    # C# source files (companion scripts)
```

**CSV counts per directory:** 250 (directories 0, 1, 2) or 200 (directory 3)
**Total pages:** ~950 (across directories 0–3)

## Script Categories

### Automated Pipelines

| Script | Purpose |
|--------|---------|
| `RUNALL.BAT` | Master script — runs all 5 steps + final assembly scripts |
| `01runcsv.bat` | Step 1 — Apply line-index metadata to raw page CSVs |
| `02pageStrip.bat` | Step 2 — Generate per-line metadata for each page |
| `03pageTypes.bat` | Step 3 — Classify pages as 1LINE, 2LINE, or NORMAL |
| `04manual_bnd2.bat` | Step 4 — Apply BND boundary tags to all pages |
| `05pagestrings.bat` | Step 5 — Generate BND and page tag files |
| `06pagemetadata.bat` | Step 6 — Generate page metadata tags |
| `Reconcile_00.bat` | Final — Reconcile all pages |
| `00StripBooksToLines.bat` | Book processing — Strip books and build line indices |

### Batch Assembly (New)

| Script | Purpose |
|--------|---------|
| `RunAll_page.bat` | Assemble all NORMAL pages (pages 1–239) |
| `RunAll_1line.bat` | Assemble all 1LINE pages (pages 1–240) |
| `RunAll_2line.bat` | Assemble all 2LINE pages (pages 1–240) |

### Manual Scripts

| Script | Purpose |
|--------|---------|
| `manual_bnd1.bat` | Process pages one at a time (main pipeline) |
| `manual_bnd2.bat` | Process pages one at a time (BND tags) |
| `manual_page.bat` | Process pages one at a time (page tags) |
| `manual_rnd.bat` | Create output directory structure |
| `1line_page.bat` | Assemble single-line pages |
| `2line_page.bat` | Assemble double-line pages |
| `00accsv.bat` | Reconcile book lines with raw page CSVs |
| `03pageTypes1line.bat` | Find 1LINE pages in a specific page range |
| `03pageTypes2line.bat` | Find 2LINE pages in a specific page range |
| `03pageTypes4line.bat` | Find 4LINE pages in a specific page range |
| `03pageTypesdefault.bat` | Find remaining page types |
| `03pagetypes.bat` | Classify all page types in a range |
| `Removepg1-16.bat` | Remove pages 1–16 (Roman numeral pages) |
| `Removepg171-174.bat` | Remove pages 171–174 |
| `Removepg225-227.bat` | Remove pages 225–227 |
| `Removedpgs1-16.bat` | Remove pages 1–16 (alternate) |
| `Removepgs189-192.bat` | Remove pages 189–192 |
| `Removepgs183-184.bat` | Remove pages 183–184 |
| `Removepgs225-227.bat` | Remove pages 225–227 (alternate) |

### Page Types

- **1LINE**: Single-line page (last line < 45 characters)
- **2LINE**: Double-line page (last line is whitespace only)
- **NORMAL**: Standard multi-line page

## Processing Pipeline

### Step 1: 00StripBooksToLines

Strips blank/spacing-only lines from book CSVs and builds line-index files.

**Input:** `books_raw_N/bookN.csv`
**Output:** `books_lines_N/books_lines_N.csv` (line index), `removed_lines_N/RemovedLinesN.csv`

The line-index CSV tracks:
- `st` — start character index in stripped line text
- `slen` — character length of non-blank text
- `fstart` — original file start index
- `flen` — original file length (0 for blank lines)
- `@` — file number

### Step 2: 01runcsv

Applies line-index metadata to raw page CSVs.

**Input:** `pages_raw_N/pageN.csv`, `books_lines_N/books_lines_N.csv`
**Output:** Enhanced page CSV with per-line position tracking

### Step 3: 02pageStrip

Generates per-line metadata for each page.

**Input:** Enhanced page CSV
**Output:** `pages_lines_N/lines-pageN.csv`

The per-line metadata CSV contains:
- `book` — book number
- `line` — line number within book
- `start` — start position
- `ws`/`we` — word start/end
- `sr`/`er` — spacing range

### Step 4: 03pageTypes

Classifies pages as 1LINE, 2LINE, or NORMAL.

**Rules:**
- 1LINE: Last line character count < 45
- 2LINE: Last line is only whitespace
- NORMAL: Everything else

### Step 5: 05pagestrings + 06pagemetadata

Generates BND boundary tags and page metadata tags.

**Output:** `tags_N/tag-N.csv` files containing:

| Tag | Purpose |
|-----|---------|
| `@5E` | BND boundary marker |
| `@5E1` | Page end marker |
| `@5E2` | Next-page start marker |
| `@5E3` | BND boundary variant |
| `@10B` | Newline separator |
| `@1B` | Page type tag |
| `@1C` | Page metadata tag |
| `{~p}` | Page suffix marker |

### Step 6: Reconcile

Final validation and reconciliation of all pages.

## Output

Reconstructed page files are written to:
- `1line_page_test/` — 1LINE page outputs
- `2line_page_test/` — 2LINE page outputs
- `output_page_test/` — NORMAL page outputs

## Dependencies

- **awk** — Required for CSV manipulation (GNU awk or mawk)
- **Windows CMD** — All batch scripts use Windows batch syntax
- **sourceIt.bat** — Shared utility for CSV manipulation (referenced by scripts)

## Usage

### Full Automated Run

```batch
RUNALL.BAT
```

Runs all 5 steps plus final assembly scripts.

### Individual Steps

```batch
01runcsv.bat    :: Step 1: Apply line indices
02pageStrip.bat :: Step 2: Generate page metadata
03pageTypes.bat :: Step 3: Classify page types
04manual_bnd2.bat :: Step 4: Apply BND tags
05pagestrings.bat :: Step 5: Generate tag files
06pagemetadata.bat :: Step 6: Generate metadata tags
```

### Batch Assembly

```batch
RunAll_page.bat   :: Assemble all NORMAL pages
RunAll_1line.bat  :: Assemble all 1LINE pages
RunAll_2line.bat  :: Assemble all 2LINE pages
```

## CSV Format Notes

- All CSVs use comma delimiters
- Multi-page files span directories 0 through 3
- Raw page CSVs: ~950 total (250+250+250+200)
- Book CSVs: 149 total (50+50+49)
- Line-index CSVs: 149 total
- Tags CSVs: ~950 total
- Files use 0-based indexing throughout
- Character counts are byte-level (not Unicode-aware)
