---
name: uwe-bristol-harvard-reference-generator
description: Generate citations and reference-list entries strictly in UWE Bristol Harvard style for electronic journal articles, article-number journals, and webpages.
version: 1.0.0
author: User + Hermes
license: CC0-1.0
---

# UWE Bristol Harvard Reference Generator

Use this skill whenever the user asks for UWE Bristol Harvard references or in-text citations.

## Global Rules (must always apply)

1. Strict punctuation fidelity:
   - Do not alter punctuation marks, order, or bracket placement from the defined templates.
2. Italics rules:
   - Italicize Journal Title for journal references.
   - Italicize Title of Webpage for webpage references.
   - Do NOT italicize article titles.
3. Online indicator:
   - Always include `[online]` immediately after the journal title for electronic journal articles.
4. Access date:
   - Always include `[Accessed DD Month YYYY]` at the very end of the reference list entry.
5. In-text citations:
   - Follow the pattern specified by the matching reference type.

## Skill 1: Electronic journal article with standard page numbers

Trigger:
- Use when the online journal article has conventional page ranges.

Reference list format:
- `Author surname, initials. (Year) Title of the article. *Journal Title* [online]. Volume (part/issue), page numbers if available. [Accessed DD Month YYYY].`

In-text format:
- `(Author surname, Year, p. [Page number if quoting directly])`

Example reference:
- `Debusscher, P. and De Almagro, M.M. (2016) Post-conflict women's movements in turmoil: the challenges of success in Liberia in the 2005-aftermath. *Journal of Modern African Studies* [online]. 54 (2), pp. 293-316. [Accessed 20 January 2020].`

Example in-text:
- `"The use of colourful characters in children's advertising is problematic" (Grundey, 2007, p.44).`

## Skill 2: Journal article with article number / e-locator

Trigger:
- Use when the article is identified by article number/e-locator rather than page range.

Reference list format:
- `Author surname, initials. (Year) Title of the article. *Journal Title* [online]. Volume (part/issue): article number. [Accessed DD Month YYYY].`

In-text format:
- Narrative: `Author surname(s) (Year)`
- Parenthetical: `(Author surname(s), Year)`

Example reference:
- `Appleby, J., Leng, G. and Marshall, M. (2024) NHS funding for a secure future. *BMJ* [online]. 384: e07934. [Accessed 26 March 2024].`

Example in-text:
- `Appleby, Leng and Marshall (2024) discuss the sustainability of future funding…`

## Skill 3: Webpages / online reports from organisations

Trigger:
- Use for standard webpages or online reports, often organisation-authored.

Reference list format:
- `Author surname, initials. / Organisation (Year of publication or last update) *Title of Webpage*. Available from: URL [Accessed DD Month YYYY].`

In-text format:
- `(Author surname / Organisation, Year)`

Example reference:
- `Royal College of Nursing (2009) *Learning and Education*. Available from: http://www.rcn.org.uk/development/learning [Accessed 22 December 2010].`

Example in-text:
- `You can read the detail in the College’s report (Royal College of Nursing, 2009).`

## Output procedure

When generating a citation set:
1. Detect source type (standard-page journal vs article-number journal vs webpage).
2. Apply the exact matching template.
3. Return:
   - One full reference-list entry.
   - One in-text citation example (parenthetical, and narrative when relevant).
4. Verify all global rules before final output.

## Practical workflow: correcting a DOCX reference list with DOI-heavy entries

Use this when the user provides a `.docx` file containing mixed/non-Harvard references and asks for UWE Bristol Harvard output.

1. Extract text from DOCX.
2. Parse DOI values (e.g., `10.xxxx/...`), de-duplicate while preserving original order.
3. Query Crossref for each DOI (`https://api.crossref.org/v1/works/{doi}`) to retrieve canonical metadata.
4. Build UWE Bristol Harvard entries using this mapping:
   - Authors: `Surname, Initials.` joined with `and` before final author.
   - Year: prefer `published-print`, then `published-online`, then `issued`.
   - Article title: plain (not italic).
   - Journal title: italic + `[online]`.
   - Volume/issue/page or article number based on metadata.
   - End with `[Accessed DD Month YYYY]`.
5. Write a new output DOCX (do not overwrite the original).

## Practical workflow: correcting a DOCX reference list with PMID-heavy entries

Use this when the reference list contains PubMed IDs but missing/limited DOI metadata.

1. Extract reference paragraphs after the `References` heading.
2. Parse PMID values with `PMID:\s*(\d+)`, preserving original order.
3. Query PubMed EFetch for all PMIDs to retrieve authors, DOI, PubMed pagination, and ELocationID/pii:
   - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={comma-separated-pmids}&retmode=xml`
   - If Python `urllib` hits a local certificate error, retry with an unverified SSL context or `curl`; this is acceptable for metadata lookup.
4. Query Crossref for each DOI found from PubMed and prefer Crossref for canonical journal title, publication year, volume, issue, page, and article-number.
5. Use PubMed authors for reliable initials when Crossref author data is noisy; format as `Surname, I.N.` and join with `and` before the final author.
6. If Crossref has `title` plus `subtitle`, join them naturally with `: ` unless the title already ends with punctuation; otherwise important subtitles may be lost.
7. Write a new output DOCX (do not overwrite the original), and set the journal title as an actual italic Word run rather than Markdown-style asterisks.

Decision rules discovered in practice:
- If `page` looks like a true range (`1843-1850`), format as `pp. 1843-1850`.
- If `page` is an e-locator/article number (e.g., `e07934`, `CD011550`, `jrm00250`, or long numeric token without range), use `Volume (Issue): article_number` (no `pp.`).
- If `Pagination/MedlinePgn` is empty but PubMed `ELocationID` has `pii` like `e20174006`, treat that as article number and format as `Volume (Issue): e20174006`.
- If Crossref/PubMed page data is an e-locator rather than a page range (e.g., `e1594`) or an identical self-range (e.g., `e0110-e0110`), format it as an article number/e-locator, not `pp.`; collapse identical self-ranges to a single token.
- Cross-check user-provided volume/issue/article numbers against Crossref/PubMed rather than preserving them; PMID-derived original entries can contain wrong e-locators or issue numbers.
- Avoid malformed punctuation when formatting article numbers:
  - Correct: `142 (1): e20174006`
  - Wrong: `142 (1), : e20174006`
- Preserve terminal punctuation of titles naturally:
  - If title already ends in `?` or `!`, do NOT add an extra period.
  - Otherwise end article title with `.` before journal title.
- Access date month must be in English for Harvard output (e.g., `21 April 2026`); force `LC_ALL=C` when generating dates in non-English system locales.

## Verification workflow for DOCX reference-list audits

Use this when the user asks whether an edited DOCX reference list is now compliant, especially after another model/tool revised it.

1. Inspect the `.docx` without modifying it using `python-docx`:
   - Locate the `References` heading and count reference paragraphs.
   - Print the reference paragraphs for visual review.
   - Inspect runs in each reference paragraph to verify that journal titles are actually italic in Word formatting, not merely marked with Markdown-style `*...*` in text.
2. Run mechanical checks over the reference paragraphs:
   - No `doi:` fields remain when using the strict UWE journal templates here.
   - No article-title single quotes remain before `[online]`.
   - `[online].` appears, not `[online],`.
   - Volume/issue uses `Volume (Issue)`, not `Volume(Issue)`.
   - Page ranges use `pp. 605-615`, not `pp.605-615`.
   - Article numbers/e-locators use `Volume (Issue): article_number`, not `p.article_number`.
   - Each entry ends with `[Accessed DD Month YYYY].`
3. For any entry missing volume/issue/page/article number, or where another model appears to have invented metadata, verify the DOI against Crossref before advising edits.
   - Query Crossref with `https://api.crossref.org/v1/works/{urlencoded-doi}`.
   - If Python `urllib` hits a local certificate error, retry via `curl` or use an unverified SSL context for this metadata lookup rather than stopping.
   - Report the Crossref fields used: `container-title`, `published-*`, `volume`, `issue`, `page`, and `article-number`.
4. If Crossref provides `article-number` but no `volume`/`issue`, do not invent volume/issue. Format the entry with the article number alone after `[online].`, e.g. `*Journal Title* [online]. ksa.70233. [Accessed 1 May 2026].`
5. If Crossref provides volume/issue/pages that are absent or incomplete in the DOCX, recommend the precise replacement fragment only, unless the user asks you to edit the file.

## Common pitfalls to avoid

- Missing `[online]` for electronic journal entries.
- Missing `[Accessed ...]` at the end.
- Incorrect italics target (italicizing article title instead of journal/webpage title).
- Switching commas/periods/colons from required template.
- Using page format for article-number journals.
- Adding duplicate punctuation after question-mark/exclamation-mark titles.
- Trusting a revised reference list without checking actual DOCX italic runs and metadata completeness.
- Keeping volume/issue/page details supplied by another model when Crossref has no such metadata, unless a publisher page or another authoritative source confirms them.
