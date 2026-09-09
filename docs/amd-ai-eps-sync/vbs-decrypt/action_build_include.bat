// ============================================================
// V6_0307 INCLUDE FILES — BUILD SCRIPT
// Strips spacing lines from books_*.csv, builds line indices,
// generates page tags, BND tags, and {~p} page metadata tags.
// ============================================================

// --- 00: GENERAL STRIP (manual mode) ---
// Works on a single book CSV. Strips blank/whitespace-only lines
// and places them in RemovedLines.csv for later reinsertion.

// Usage: {set sPath to "..."; set sOutput to "..."; process ...}
{sOutput} = {sPath};
strip {sOutput} ;
  --{sOutput} goes into the blank line CSV
  --compare line by line with source, strip whitespace-only
  --and then output the whitespace and spacing lines into
  --{sOutput} with two numeric fields (sp and wp):
  --  sp = number of space lines
  --  wp = number of word wrap lines
  --{sOutput} is the CSV for that book with spacing lines removed
  --and {strippedCSV} is the working file for making the
  --stripped CSV file into data record structures

// ============================================================
// 01: BOOK INCLUDE
// For every BookN.csv that exists, strip spacing lines and
// generate the books_lines_[BookN].csv line index.
// ============================================================

// For each BookN file (where N = 1..499):
// 1. Strip the CSV to remove blank/spacing lines
// 2. Create a line-index CSV: books_lines_[N].csv with 5 columns:
//    st = start character index (0-based into stripped line text)
//    slen = character length of the non-blank line
//    fstart = original file start index (0-based)
//    flen = original file length
//    @ = file number
//    Original lines must NOT be removed from the source CSV,
//    only whitespace-only lines get their flen set to 0.
//    Lines with both words and spacing have slen set to the
//    character count of only the words, while flen retains
//    the full original length including spacing.

// ============================================================
// 02: PAGE STRIP (manual mode)
// Works on a single page CSV. Generates lines-page<N>.csv
// with per-line metadata (book, line, position, spacing info).
// ============================================================

// page [page number] in [page CSV file] strip [output prefix]
// The page-numbered line CSV adds one line to every line:
//   book, line, start, ws, we, sr, er
// where start = start character, ws/we = word start/end,
// sr/er = spacing line ranges
// Also generates lines-page[N].csv containing per-line metadata:
//   st = start in page line text, slen = length in page line text,
//   pos = position from page start (cumulative offset)
//   bn/bn1 = "booknumber" / "booknumber-1" (from book line index)
//   ws/we/sr/er = spacing word end / spacing range info

// ============================================================
// 03: 1LINE + 2LINE PAGE TYPES
// ==============================================1============
// Identifies single-line and double-line page types:
// - 1LINE: Last line char count < 45 (single line page)
// - 2LINE: Last line is only whitespace (double line page)

// HasConstantType [page CSV] -- Outputs 1LINE, 2LINE, or NORMAL

// ============================================================
// 04: BND RECONCILIATION (manual mode)
// Compares boundary metadata between raw and processed CSVs.
// Outputs line indices for BND boundary lines (0-based).
// ============================================================

// boundary [boundary number] in [page CSV] reconcile [output prefix]
// Outputs a CSV with columns: 0 (space) 1 (BN1 value)

// ============================================================
// 05: PAGESTRINGS & BND TAGS
// Generates tag-*.csv files with BND boundary markers:
//   @5E, @5E1, @5E2, @5E3, etc.
// for every page, including prefix/suffix tags.
// ============================================================

// pagestrings -- Creates tag-N.csv for each page with:
//   BND tags, page tags, and page-type-specific tags
//   {~p} suffix tags for pages ending with trailing text
//   @10B suffix for pages needing newline separators

// BND tags use the @5E family:
//   @5E  = basic BND (spacing-only line)
//   @5E1 = page end (end index = first on next page minus 1)
//   @5E2 = next-page start (next page line 0 start)
//   @5E3 = another BND variant

// ============================================================
// 06: PAGENETADATA (manual mode)
// Generates the page metadata tag file for a single page.
// ============================================================

// page [page number] in [page CSV] PAGENETADATA [output tag]
// Generates tag output with @1B, @1C, @10B tags based on
// page type (1LINE, 2LINE, or NORMAL).

// ============================================================
// BUILD SEQUENCE:
//   1. 01BOOK_INCLUDE  — strip books, build line indices
//   2. 02PAGE_STRIP   — strip pages, build per-line metadata
//   3. 03PAGE_TYPES   — identify 1LINE/2LINE pages
//   4. 05PAGESTRINGS  — generate BND tags and page tags
//   5. RECONCILE_00   — final validation
//
// The outputs from steps 1-4 feed into RUNALL.BAT or
// the manual scripts (manual_bnd1.bat, manual_bnd2.bat,
// manual_page.bat, 1line_page.bat, 2line_page.bat).
// ============================================================
