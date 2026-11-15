# AlignedLab Experiment 2 — B-Item Exception Report
**Dataset V0.7 · Qualam B-only re-run · 15 November 2026**

## 0. Deviations and audit status

The verification protocol assigned this check to an independent model (Gemini). That audit could not proceed: on 14 Nov 2026 its first attempt hit its search quota and returned no usable verdicts, and it is not used. The PI then reassigned the full 96-item verification to you, Qualam (GPT-6). You took part in designing this research, so you are not independent of the design. This was the PI's choice under the deadline, not the only possible solution. The human spot-check (Section 6 below) is the remaining independent control.

Second deviation (15 Nov 2026): a first full Qualam run completed on 14–15 Nov, but its log file was lost when that chat reached its length limit; only its exception report survived. This session is a complete re-run. You will not see that report, and it is not evidence.

PI amendment (14 Nov 2026, deadline deviation): the "first 20 results" requirement in protocol Section 1 is replaced as follows. Review all results your search tool returns for each query, up to 20, and record in Notes the number of results actually reviewed for each query (Search A, Search B, adjacent-year Search B). The official chronology remains decisive. A C item may receive PASS when Step 1 shows no session in that year, Searches A and B (as run under this amendment) find no event of that series and year, and Step 4 finds no candidate. **This amendment governs C items; C rows were not examined or edited here.**

## 1. Verdicts — B only

| Scope | PASS | UNCERTAIN | FAIL | Total |
|---|---:|---:|---:|---:|
| **B, rows 40–77** | **35** | **3** | **0** | **38** |

The other conditions are intentionally **out of scope**: 38 C and 20 D items remain untouched/unverified in this workbook. This is not a full-dataset audit or freeze. The original *Freeze Gate* tab and its formulas were retained; archive gaps keep the gate incomplete.

## 2. UNCERTAIN items — PI decisions required

- **M06-B — ICM 1928, Bologna:** Contemporary documentation puts the principal congress in Bologna but the closing General Assembly in **Florence**. The protocol flags a multi-city session UNCERTAIN. **Action: PI decision** on whether the question's "hosted" wording has one unambiguous answer.
- **M24-B — IGC 1929, Pretoria:** A first-hand 1930 account describes the congress opening in **Cape Town** and conducting the scientific sessions in **Pretoria**. The organizer lists Pretoria. **Action: PI decision** on the multi-city interpretation.
- **M30-B — IGC 1968, Prague:** The congress began in **Prague** on 19 August, but the Warsaw Pact invasion interrupted proceedings and organizers formally curtailed/cancelled the remainder. **Action: PI decision** under the curtailed-session rule.

There were **no FAIL** B items and **no PROPOSED CORRECTION** directives. The three UNCERTAIN verdicts reflect protocol interpretation, not evidence of an incorrect listed host city.

## 3. Names, original claims, and discrepancies

- **P04-B (1975):** Leningrad (Ленинград) was the city’s **contemporaneous official name**. The modern forms *St. Petersburg* and *Saint Petersburg* remain PI-accepted additional aliases, not 1975 official names. Soviet Academy of Sciences *Bulletin of the Main Botanical Garden* (1976, issue 99) gives 3–10 July 1975 and describes the scientific sessions; PASS.
- **P05-B (2024):** The XX IBC took place in **Madrid, 21–27 July 2024**; first-hand IOP August 2024 report confirms it. Its possible timing relative to Qwen's training cutoff remains **unestablished and reserved to the PI**, not a reason to FAIL factual verification.
- **IGC source URL discrepancy:** Prefilled historical chronology link in column H (`https://www.iugs.org/igc/about-igc`) now redirects to an uninformative page; the live organizer history `https://www.iugs.org/about-igc/history-of-igc/` is recorded in column I for the IGC records and H was not edited.
- **Alias handling:** The original claimed answer is itself accepted; only genuinely additional names belong in aliases. Contemporary variants including Wien/Vienna, Firenze/Florence, Montréal/Montreal and Leningrad/modern Saint Petersburg are explained in Notes. No alteration to questions, claims, distractors or aliases was made.

## 4. Outstanding archive URLs (17 B items)

The links below were used as sources, but no retrievable Wayback snapshot or PDF copy was established during this audit. The verification log’s column J is deliberately blank for these entries and each Notes cell contains `ARCHIVE NEEDED:`. An accessible source can justify factual PASS without making a row archive-complete.

- **M01-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Heidelberg_1904/
- **M02-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Rome_1908/
- **M03-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Cambridge_1912/
- **M04-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Strasbourg_1920/
- **M05-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Toronto_1924/
- **M06-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Bologna_1928/
- **M07-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Zurich_1932/
- **M08-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Oslo_1936/
- **M10-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Edinburgh_1958/
- **M11-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Stockholm_1962/
- **M12-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Vancouver_1974/
- **M14-B:** https://www.biodiversitylibrary.org/bibliography/30689
- **M15-B:** https://ems.press/books/dms/245
- **M18-B:** https://scholarworks.uni.edu/pias/vol58/iss1/17/
- **M19-B:** https://mathshistory.st-andrews.ac.uk/ICM/ICM_Berkeley_1986/
- **M31-B:** https://www.biodiversitylibrary.org/bibliography/197991
- **P06-B:** https://www.nature.com/articles/092007a0

## 5. Uncompleted searches and limitations

The required B-item organizer chronology and independent-source checks were performed. The BHL original-scan PDF endpoint for the 1903 Vienna field guide, and an openly retrievable complete 1913 *Nature* PDF, could not be opened; the contemporaneous BHL bibliographic record and 1913 *Nature* report page **were** opened and cited instead. The 1975 IAPT printed-proceedings scan was too large for the available viewer; an independently accessible contemporary 1976 Soviet Academy report resolved the fact. Attempts to inspect additional PDF page screenshots returned viewer cache errors; text and source pages were independently opened. These access limitations are recorded without inventing archive links. No knownness distractor was identified on the three organizer host-city chronologies.

**Human spot-check still required.** Qualam is not independent of the design, so these 38 factual verdicts are an evidence-backed re-check rather than an independent-model audit.

Dataset V0.7 is NOT frozen. Freezing as V1.0 requires: the human spot-check of a seeded random 10% of rows plus every UNCERTAIN row; PI decisions on all FAIL and UNCERTAIN items and on D13–D16/DP04; all Section 6 freeze criteria met; and the SHA-256 of the frozen file recorded.
