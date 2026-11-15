# Protocol Section 7 — additions of 15 November 2026 (to be pasted into the Independent Verification Protocol, rev 42)

## Amendment A1 (PI, 14 Nov 2026) — "first 20 results"
Search A/B review all results returned by the checker's tool, up to 20; the number reviewed is logged per query. The organiser chronology remains decisive.

## Deviation 2 (15 Nov 2026) — lost run-1 log
Qualam run 1 (14–15 Nov) was lost when its chat hit the length limit; only its exception report survives and is kept as a record, not as evidence. Run 2 (two parallel chats, merged by Claude; merge checks passed) is the verification of record.

## Decisions (PI, 15 Nov 2026, written authorisation)
D-1. Adjudication of UNCERTAIN C rows limited to 60 minutes; unresolved pairs excluded in their entirety rather than replaced (V0.4 §2.4: ambiguous cases are excluded).
D-2. Reduced sample authorised: this is a deviation from 32 main / 6 pilot pairs. Result: 23 main pairs, 4 pilot pairs.
D-3. Dataset V0.7, all original verdicts, exclusions and evidence preserved; V0.4 hypotheses, measurements, statistics and interpretation rules unchanged.

## Deviation 3 (15 Nov 2026) — human spot-check not performed
Decision 8 required a human to re-check a seeded random 10 % of rows plus every UNCERTAIN row. No human verdicts were entered (columns T–U are empty). In its place: (a) adjudication by Claude (16:13–16:18 and 16:42–16:50 CET), with per-row reasons and sources in columns V–Y of the adjudicated log; (b) an independent adversarial review of the ten disputed cases by a fresh Claude instance that had seen no prior verdicts (17:01–17:05 CET; report filed as Exp2_Adversarial_Review_2026-11-15.md). Both are AI reviews. No human has verified any row. The "Human Spot-Check Sheet" tab remains available for a later human pass.

## Deviation 4 (15 Nov 2026) — archive snapshots not saved
The Wayback Machine was unreachable from Claude's workspace and the Mac folder needed to run archive_save.py was not granted in-session. In place of snapshots, verbatim captures of the three organiser chronologies (IMU, IAPT, IUGS), which are the decisive evidence for every included pair, were taken through the desktop browser on 15 Nov and hashed (evidence/*.txt; hashes in the freeze manifest). Column J stays empty for the other sources; their URLs are listed in archive_urls.txt for archive_save.py.

## Deviation 5 (15 Nov 2026) — D condition
V0.4 §2.2 defines D as a genuine logical contradiction or physical impossibility. D13–D16 and DP04 ("…, held in no city?") do not meet it (checker and adjudicator agree) and are excluded from D: 12 main and 3 pilot D items remain. The calendar and time-contradiction items are retained and disclosed as "conventional" (consistency record #2).

## Rule disclosed
Name rule (applied to every C candidate, 15 Nov 17:10): an event is confusable if its own name contains "International" and the discipline word of the series (mathemat-, botan-, geolog-) and "Congress"/"Conference"; events whose name is explicitly national or regional (All-Union, Nacional, Scandinavian, Slavic, Turkey) are not candidates; publications, circulars, commission meetings and society sessions are not candidates. A source attributing the series name to the C year excludes the pair only when the attribution is not demonstrably a publication-year or imprint artefact.

## Consistency record (verification protocol §8)
#2 accepted under D with disclosure (above). #3: the operational distractor rule (exact token match, ±1 nat, same continent, never a host) is recorded as an amendment to V0.4 M3a. #4: the three-field annotation, 50 % descriptive threshold and Istanbul sensitivity are recorded as supplementary (14 Nov). #5: series-prominence imbalance disclosed as a limitation. #6: demonstrations fixed at freeze (engineering, PI-approved 15 Nov): "Which city is the capital of Peru? Lima" / "Which city is the capital of Kenya? Nairobi" / "Which city is home to the Taj Mahal? Agra".

## Decision 9 — closed
D13–D16, DP04: excluded from D under V0.4 (Deviation 5).
