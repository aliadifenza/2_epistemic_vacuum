# Experiment 2 — Dataset V0.7 C/D Verification: Exception Report
**Checked:** 15 November 2026 · **Checker:** Qualam / GPT-6 · **Operator:** Dr. Ali Antonio Di Fenza · **Scope:** 38 C + 20 D items only

## 1. Protocol deviations and PI amendment

The verification protocol assigned this check to an independent model (Gemini). That audit could not proceed: on 14 November 2026 its first attempt hit its search quota and returned no usable verdicts, and it was not used. The PI then reassigned the full 96-item verification to Qualam (GPT-6). Qualam participated in designing this research and is therefore **not independent of the design**. This reassignment was the PI's decision under the deadline, not the only possible solution; the human spot-check is the remaining independent control.

**Second deviation (15 November):** A first full Qualam run was completed on 14–15 November, but its log was lost when that chat reached its length limit; only an exception report survived. This session is a complete re-run. The previous report was withheld and is **not evidence** for this audit.

**PI amendment (14 November):** Instead of requiring exactly the first 20 results for every C-item search, the checker reviews all results returned by its search tool, **up to 20**, and records the actual number reviewed for Search A, Search B and adjacent-year Search B in each row's Notes. The organiser chronology remains decisive; a C item may PASS only where that chronology has no session in the year, searches disclose no relevant event, and alternative-name checks find no candidate.

## 2. Verdict counts

| Condition | PASS | UNCERTAIN | FAIL | Not checked here |
|---|---:|---:|---:|---:|
| B — real congresses | 0 | 0 | 0 | **38** (parallel checker) |
| C — fictional congresses | **16** | **22** | 0 | 0 |
| D — impossible premises | **15** | **5** | 0 | 0 |
| **C + D total** | **31** | **27** | **0** | 0 |

All 38 B rows and human spot-check columns remain unchanged. Missing archive references in J keep rows **incomplete for freezing**, even where their factual verdict is PASS.

## 3. Every UNCERTAIN item, reason and required action

**C-item action code R:** Replace the complete matched B/C pair; re-verify the replacement against sources and rerun the prescribed Qwen validation. **Every C item below requires R**; no existing matched pair is authorised for use as-is.

| Item | One-line exception and action |
|---|---|
| M01-C | 1904 French botanical jubilee/1905 congress confusion; **R**. |
| M03-C | 1912 bibliographies refer to 1910 IBC proceedings; source ambiguities unresolved; **R**. |
| M04-C | 1920 commission preparing the 1922 geological congress; historical PDF inaccessible; **R**. |
| M05-C | 1924 London **Imperial Botanical Conference** is plausibly confusable; **R**. |
| M06-C | 1928 Copenhagen Quaternary congress and 1926 IGC publication dates overlap; **R**. |
| M08-C | 1936 Berlin meeting of IGC-connected cartographic commissions; **R**. |
| M10-C | 1958 Paris meeting of IGC-related commission; similar series network; **R**. |
| M14-C | 1910 Brussels international mathematics-education congress, not the ICM; **R**. |
| M15-C | 1998 international botanic-gardens conservation congress, different series; **R**. |
| M17-C | Secondary reference calls a 1935 Moscow meeting “ICM-1935,” conflicting with IMU; **R**. |
| M18-C | 1950 catalogue dates 1948 proceedings; separate map record says “1950 IGC”; **R**. |
| M19-C | Bibliographic record describes “1986 International Geological Congress Field Trip”; **R**. |
| M21-C | 1964 ICMI education colloquia; detailed organiser page inaccessible; **R**. |
| M22-C | 1969 Lyon **ICME** has a close name and an IMU-related organiser; **R**. |
| M24-C | 1929 publication of 1928 Bologna ICM; adjacent-search counts not separable; **R**. |
| M27-C | 2012 reporting of 2011 Melbourne IBC; adjacent-search counts not separable; **R**. |
| M28-C | 1952 Utrecht nomenclature publication and erroneous “IBC Utrecht” citation; **R**. |
| M30-C | 1968 circular concerns 1969 Seattle IBC, but catalogue page inaccessible; **R**. |
| M32-C | 1987 INHIGEO historians' meeting may be confused with geological congress; **R**. |
| P01-C | 2016 European Mathematics Congress and misdated “2016 Seoul ICM” brochure; **R**. |
| P05-C | 2024 Sydney **ICME**, under ICMI, could be confused with the ICM; **R**. |
| P06-C | 1913 Scandinavian mathematicians' congress and 1912 Cambridge publication dates; **R**. |

**D-item action:** Each of the five category mismatches below needs a PI judgment; preserve the original question until authorised. In all five cases the real congress took place in person, but a city can organise/host a gathering held elsewhere, outside a city or virtually; wording alone does not force the claimed logical impossibility.

| Item | Judged category and decisive finding; action |
|---|---|
| **D13** | **Historical falsehood**, not strict logical: 1999 IBC convened at America's Center, St. Louis; **PI JUDGMENT REQUIRED**. |
| **D14** | **Historical falsehood**: 1966 ICM opening and delegates physically present in Moscow; **PI JUDGMENT REQUIRED**. |
| **D15** | **Historical falsehood**: 1996 IGC physically held in Beijing according to organiser and Chinese geological society; **PI JUDGMENT REQUIRED**. |
| **D16** | **Historical falsehood**: 2017 IBC was an in-person gathering in Shenzhen; **PI JUDGMENT REQUIRED**. |
| **DP04** | **Historical falsehood**: 1993 IBC labelled “Tokyo” in series list but official proceedings record **Pacifico Yokohama** venue; **PI JUDGMENT REQUIRED**. |

## 4. Proposed corrections (not applied)

**PROPOSED CORRECTION — source URL only:** The prefilled IUGS chronology URL `https://www.iugs.org/igc/about-igc/` no longer provides the required chronology. Use `https://www.iugs.org/about-igc/history-of-igc/` (entered in evidence column I). The original H values have deliberately **not** been changed; the proposal is logged in every affected row's Notes. No question, claim, answer, alias, distractor or declared category was altered.

## 5. D13–D16 and DP04: classification decision

These five items were **UNCERTAIN**, with judged category **Historical falsehood**, because the real event was held in a city while the *generic words* permit a city to host an event at a non-city venue or online. They do not meet the protocol's strict-logical category as presently specified. **PI JUDGMENT REQUIRED separately for D13, D14, D15, D16 and DP04**; no replacement wording or reclassification has been implemented. The exact three-plus-sentence analysis for each is in its worksheet Notes.

## 6. ARCHIVE NEEDED — deduplicated evidence URLs

No existing reproducible archive snapshot was established for the following URLs; column J is intentionally blank for these. PDF or Wayback archiving remains the operator's responsibility:

1. https://www.mathunion.org/icm/past-icms
2. https://www.iaptglobal.org/iabms-history
3. https://www.iugs.org/about-igc/history-of-igc/
4. https://www.iugs.org/igc/about-igc/ *(obsolete original link)*
5. https://science.nasa.gov/moon/facts/
6. https://www.timeanddate.com/date/february-30.html
7. https://mathshistory.st-andrews.ac.uk/ICM/ICM_Moscow_1966/
8. https://www.mobot.org/MOBOT/research/conferences/ibc99.html
9. https://www.geosociety.org.cn/?v1=v40&v4=68e3f32c5953f&v5=en
10. https://www.nature.com/articles/s41477-017-0018-4
11. https://www.mathunion.org/fileadmin/IMU/ICM2018/static_site/portal/news-last-day.html
12. https://www.iapt-taxon.org/historic/Congress/IBC_1993/Proceedings.pdf

## 7. Source and protocol discrepancies

The organiser lists occasionally conflict with publication years, derivative citations or related congress names; the 22 C uncertainties record such ambiguities without treating missing search hits as proof of absence. **DP04 is a particularly clear host/venue distinction:** IAPT's “Tokyo 1993” label and the actual Yokohama site differ. The legacy IUGS URL is outdated. Some multi-query search results showed only a combined count, not a separate count for each adjacent-year search, which was disclosed rather than invented. The original protocol V0.4 and independent verification V0.7 differ on ambiguous C handling and D-category treatment; PI decisions in V0.7 govern this check.

## 8. Searches and sources not fully accessible

Specific pages could not be opened because of cache failures, access blocks or retrieval errors (including the 1920 organising-commission source, 1964 ICMI detail, 1968 Seattle-circular catalogue and one 2016 Seoul brochure). PDF screenshot retrieval also failed on the 1993 IAPT report and a 1996 geological circular; the official chronologies and alternative directly opened sources were used instead, and unresolved C candidates were marked UNCERTAIN. Some combined C searches did not expose per-query counts; these rows remain UNCERTAIN. **No PASS was inferred from an inaccessible page alone.**

Dataset V0.7 is NOT frozen. Freezing as V1.0 requires: the human spot-check of a seeded random 10% of rows plus every UNCERTAIN row; PI decisions on all FAIL and UNCERTAIN items and on D13–D16/DP04; all Section 6 freeze criteria met; and the SHA-256 of the frozen file recorded.
