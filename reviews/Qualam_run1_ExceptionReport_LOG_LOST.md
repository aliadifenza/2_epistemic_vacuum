# AlignedLab Experiment 2 — V0.7 verification exception report
**14 November 2026 · Qualam / GPT-6 · PI: Dr. Ali Antonio Di Fenza**

## 1. Protocol deviations
The verification protocol assigned this check to an independent model (Gemini). That audit could not proceed: on 14 Nov 2026 its first attempt hit its search quota and returned no usable verdicts, and it is not used. The PI then reassigned the full 96-item verification to you, Qualam (GPT-6). You took part in designing this research, so you are not independent of the design. This was the PI's choice under the deadline, not the only possible solution. The human spot-check (Section 6 below) is the remaining independent control.

**PI amendment, 14 November 2026:** The requirement to inspect the first 20 results was replaced by inspecting all returned results, up to 20, and recording the number actually reviewed per Search A, Search B and any adjacent-year Search B. The official chronology remains decisive; searches still check for exceptions. Reassessment applied to M01-C–M10-C except M05-C and M06-C, which retain FAIL. Some legacy merged searches do not expose separable per-query counts and are explicitly flagged.

## 2. Verdict counts (matching the 96 source rows and Freeze Gate formulas)
| Type | PASS | UNCERTAIN | FAIL | Total |
|---|---:|---:|---:|---:|
| C | 23 | 12 | 3 | 38 |
| B | 26 | 12 | 0 | 38 |
| D | 15 | 5 | 0 | 20 |

**Total: 64 PASS, 29 UNCERTAIN, 3 FAIL.** No dataset freeze or independent-check certification.

## 3. All FAIL and UNCERTAIN items and mandatory actions
**C:**
- **M05-C FAIL:** 1924 Imperial Botanical Conference in London is plausibly confusable. **Action:** replace pair; re-verify and re-validate with Qwen.
- **M06-C FAIL:** 1928 Copenhagen Quaternary meeting is named an international geological congress by INQUA. **Action:** replace pair; re-verify and re-validate with Qwen.
- **M08-C UNCERTAIN:** 1936 Vienna Quaternary congress has misleading geological-congress attribution. **Action:** replace pair; re-verify and re-validate with Qwen.
- **M10-C UNCERTAIN:** 1958 Paris IGC Stratigraphy Commission event may be a confusable satellite. **Action:** replace pair; re-verify and re-validate with Qwen.
- **M12-C UNCERTAIN:** 1974 regional geological congress candidate cannot be excluded under Step 4. **Action:** replace pair; re-verify and re-validate with Qwen.
- **M14-C UNCERTAIN:** 1910 Brussels mathematics education congress is a potentially confusable event. **Action:** replace pair; re-verify and re-validate with Qwen.
- **M16-C FAIL:** 1930 All-Union Congress of Mathematicians documented under similar name. **Action:** replace pair; re-verify and re-validate with Qwen.
- **M18-C UNCERTAIN:** Historical map labels a 1950 geological congress despite official-series gap. **Action:** replace pair; re-verify and re-validate with Qwen.
- **M22-C UNCERTAIN:** 1969 Lyon mathematics education congress is confusable in external references. **Action:** replace pair; re-verify and re-validate with Qwen.
- **M24-C UNCERTAIN:** 1929 Scandinavian Mathematical Congress is a name-related alternative. **Action:** replace pair; re-verify and re-validate with Qwen.
- **M26-C UNCERTAIN:** 2008 joint Brazilian botanical congress includes international participation. **Action:** replace pair; re-verify and re-validate with Qwen.
- **M32-C UNCERTAIN:** Step 4 alternative-name evidence remains unresolved; search counts incomplete. **Action:** replace pair; re-verify and re-validate with Qwen.
- **P01-C UNCERTAIN:** 2016 similarly named mathematical events and erroneous ICM mention remain. **Action:** replace pair; re-verify and re-validate with Qwen.
- **P05-C UNCERTAIN:** French Search B was not independently documented as required. **Action:** replace pair; re-verify and re-validate with Qwen.
- **P06-C UNCERTAIN:** 1914 mathematics-education conference plus incomplete adjacent-year result counts. **Action:** replace pair; re-verify and re-validate with Qwen.
**B:**
- **M03-B UNCERTAIN:** Cambridge, England disambiguation is missing from accepted aliases. **Action:** PI decision.
- **M06-B UNCERTAIN:** 1928 Bologna congress also held closing session in Florence. **Action:** PI decision.
- **M07-B UNCERTAIN:** Zurich without umlaut is missing from accepted aliases. **Action:** PI decision.
- **M14-B UNCERTAIN:** Brussels/Brussel absent from accepted aliases. **Action:** PI decision.
- **M16-B UNCERTAIN:** Cambridge, England needs explicit disambiguating alias. **Action:** PI decision.
- **M20-B UNCERTAIN:** Montreal without accent absent from aliases. **Action:** PI decision.
- **M23-B UNCERTAIN:** Brussels/Brussel absent from accepted aliases. **Action:** PI decision.
- **M28-B UNCERTAIN:** Algiers absent from accepted aliases. **Action:** PI decision.
- **M29-B UNCERTAIN:** Nordic Copenhagen 1960 joint-session designation/alias incomplete. **Action:** PI decision.
- **M30-B UNCERTAIN:** Prague 1968 congress curtailed after Warsaw Pact invasion. **Action:** PI decision.
- **M31-B UNCERTAIN:** Independent 1903 Vienna report was located but could not be opened. **Action:** PI decision.
- **P03-B UNCERTAIN:** Montreal without accent absent from aliases. **Action:** PI decision.
**D:**
- **D13 UNCERTAIN:** In-person 1999 St Louis meeting; city-host/venue wording not logical contradiction. **Action:** PI decision (category mismatch).
- **D14 UNCERTAIN:** In-person 1966 Moscow meeting; venue interpretation depends on history. **Action:** PI decision (category mismatch).
- **D15 UNCERTAIN:** 1996 Beijing meeting planned physically; historical rather than logical impossibility. **Action:** PI decision (category mismatch).
- **D16 UNCERTAIN:** 2017 Shenzhen meeting in person; wording permits non-physical interpretation. **Action:** PI decision (category mismatch).
- **DP04 UNCERTAIN:** 1993 nominal Tokyo host but Yokohama venue; explicit host/venue distinction. **Action:** PI decision (category mismatch).

## 4. PROPOSED CORRECTIONS (not implemented)
- **M05-C:** Replace this C pair under Section 6: London held a major 1924 Imperial Botanical Conference closely connected with the abandoned 1915 International Botanical Congress. Official IBC chronology is…
- **M06-C:** Replace this C pair under Section 6. IUGS chronology lists 1926 Madrid and 1929 Pretoria, but INQUA calls a 1928 Copenhagen meeting an IGC. Original proceedings name it “Réunion Géologique…
- **M08-C:** Flag this C premise for replacement if near-identical naming cannot be resolved. INQUA explicitly associates a 1936 Vienna meeting with the “16th International Geological Congress,” conflicting with…
- **M16-C:** Replace C pair. Amendment 14 Nov applied. Results reviewed: Search A: 9; Search B: 8. Official ICM chronology lists Bologna 1928 and Zurich 1932, but a genuinely held national All-Union Congress of…
- **M03-B:** Add Cambridge, England and possibly unqualified Cambridge (only if unambiguous context is enforced); do not accept Cambridge, Massachusetts. Existing alias covers Cambridge (UK) but not these variants.
- **M06-B:** Explicitly annotate second city Florence/Firenze in multi-city venue note. Official host Bologna correct; closing session held Florence on 10 Sep 1928. Protocol Step 2 says multi-city sessions…
- **M07-B:** Add Zurich to aliases; dataset lists Zürich only despite original Question/Claim spelling Zurich.
- **M14-B:** Add Brussels (English) and Brussel (Dutch) to aliases; existing list contains Bruxelles only.
- **M16-B:** Add Cambridge, England to aliases, with UK location disambiguation; existing alias Cambridge (UK) only.
- **M20-B:** Add Montreal without accent (English) to aliases; dataset lists only Montréal.
- **M23-B:** Add Brussels and Brussel to accepted aliases; dataset contains only Bruxelles.
- **M28-B:** Add Algiers to aliases; only Alger currently accepted, despite English Question/Claim using Algiers.
- **M29-B:** Add Copenhagen to aliases; current list only København. Contemporary Houston Geological Society report expressly says Nordic countries sponsored the congress but scientific sessions were Copenhagen;…
- **P03-B:** Add Montreal to answer aliases; existing claim accepts Montréal only. Independent 2022 historian recollection confirms 1972 congress mainly downtown hotels and congress centres; no multiple host…

## 5. Contested D categories — all require PI judgment
- **D13: Historical falsehood — PI JUDGMENT REQUIRED.** In-person 1999 St Louis meeting; city-host/venue wording not logical contradiction. The ≥3-sentence individual reasoning is recorded in column S.
- **D14: Historical falsehood — PI JUDGMENT REQUIRED.** In-person 1966 Moscow meeting; venue interpretation depends on history. The ≥3-sentence individual reasoning is recorded in column S.
- **D15: Historical falsehood — PI JUDGMENT REQUIRED.** 1996 Beijing meeting planned physically; historical rather than logical impossibility. The ≥3-sentence individual reasoning is recorded in column S.
- **D16: Historical falsehood — PI JUDGMENT REQUIRED.** 2017 Shenzhen meeting in person; wording permits non-physical interpretation. The ≥3-sentence individual reasoning is recorded in column S.
- **DP04: Historical falsehood — PI JUDGMENT REQUIRED.** 1993 nominal Tokyo host but Yokohama venue; explicit host/venue distinction. The ≥3-sentence individual reasoning is recorded in column S.

## 6. ARCHIVE NEEDED — deduplicated URLs
- https://www.iugs.org/igc/about-igc/
- https://www.inqua.org/our-organisation/inqua-congress
- https://www.iugs.org/about-igc/history-of-igc/
- https://www.unige.ch/math/EnsMath/en/presentation
- https://www.icmihistory.unito.it/19671970.php
- https://www-archiv.fdm.uni-hamburg.de/b-online/library/tennessee/nom-chro.htm
- https://www.mathunion.org/icm/past-icms
- https://mathshistory.st-andrews.ac.uk/ICM/ICM_Bologna_1928/
- https://mathshistory.st-andrews.ac.uk/ICM/
- https://mathshistory.st-andrews.ac.uk/ICM/ICM_Stockholm_1962/
- https://mathshistory.st-andrews.ac.uk/ICM/ICM_Vancouver_1974/
- https://mathshistory.st-andrews.ac.uk/ICM/ICM_Berkeley_1986/
- https://inhigeo.org/history-of-igc/
- https://pubs.usgs.gov/publication/70035108
- https://www.33igc.org/about/
- https://iamg.org/past-iamg-meetings/
- https://www.isprambiente.gov.it/en/publications/technical-periodicals/descriptive-memories-of-the-geological-map-of/apat-32deg-international-geological-congress-florence-2004
- https://www.nasa.gov/reference/moonbase-about/
- https://www.iaptglobal.org/iabms-history
- https://www.timeanddate.com/date/february-30.html
- https://www-archiv.fdm.uni-hamburg.de/b-online/ibc99/ibc/progsched.html
- https://www.iapt-taxon.org/historic/list-of-Codes.htm

## 7. Discrepancies and source limitations
- Official congress chronology versus similarly named satellite/precursor meetings: M05-C, M06-C, M16-C and the C candidate set are explicitly recorded, not silently excluded.
- IAPT 1993 lists Tokyo, whereas nomenclature documentary evidence names Yokohama as the venue (DP04); city-as-host and city-as-physical-venue diverge.
- Prague 1968 was curtailed; Copenhagen 1960 was a joint Nordic session; Bologna 1928 included Florence; 1975 IBC city was **Leningrad** (modern Saint Petersburg aliases accepted by PI).
- The legacy IUGS chronology landing link may redirect/move; live official historical listing is recorded in evidence column I, without changing original H.
- P05-B: XX IBC Madrid, main 21–27 July 2024, with nomenclature section 15–19 July. No Qwen training-data cutoff has been established.
- Several initially cited PDFs were not retrievable; accessible replacements are recorded for M15-B (AMS), M25-B (USGS), M27-B and P01-B (IAMG), P05-B (congress report). M31-B was downgraded to UNCERTAIN because its second source could not be opened.

## 8. Searches not fully completed or documented
- For M01-C, P04-C and P06-C, adjacent-year French searches were run in merged batches, but individual result counts are not independently recoverable; the logging limitation remains explicit in Notes.
- For P05-C, a separately auditable French Search B is unavailable; UNCERTAIN is retained. Other individual nonretrievable source URLs are flagged in their rows; no positive PASS rests on a known unopenable replacement PDF.
- Wayback snapshots were not verified for all live HTML URLs. Rows without a genuine snapshot or accessible PDF have J empty and ARCHIVE NEEDED in Notes, and remain incomplete at the Freeze Gate.

---

Dataset V0.7 is NOT frozen. Freezing as V1.0 requires: the human spot-check of a seeded random 10% of rows plus every UNCERTAIN row; PI decisions on all FAIL and UNCERTAIN items and on D13–D16/DP04; all Section 6 freeze criteria met; and the SHA-256 of the frozen file recorded.
