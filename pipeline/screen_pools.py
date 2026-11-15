"""Screen candidate distractor pools against the Dataset V0.7 distractor rule (READ ME, 'Distractor rule'):
same continent/region and settlement type, existed at the date, never hosted any ICM/IBC/IGC session (incl. the 1893
Chicago precursor), not an A answer, no common-word or first-name city names; selected before any scoring.
Usage: python3 screen_pools.py exp2/pools_candidates.json exp2/pools.json"""
import json, sys
HOSTS = {  # every host city on the IMU, IAPT and IUGS lists captured 15 Nov 2026, plus the 1893 precursor and the 1993 IBC venue
 "Zurich","Paris","Heidelberg","Rome","Cambridge","Strasbourg","Toronto","Bologna","Oslo","Amsterdam","Edinburgh","Stockholm","Moscow",
 "Nice","Vancouver","Helsinki","Warsaw","Berkeley","Kyoto","Berlin","Beijing","Madrid","Hyderabad","Seoul","Rio de Janeiro","Philadelphia",
 "Vienna","Bruxelles","Brussels","Ithaca","Montreal","Seattle","Leningrad","Saint Petersburg","St. Petersburg","Sydney","Tokyo","St. Louis",
 "Melbourne","Shenzhen","Cape Town","Bologna","London","Washington","Mexico City","Pretoria","Algiers","Copenhagen","New Delhi","Delhi",
 "Prague","Montréal","Florence","Oslo","Brisbane","Busan","Chicago","Evanston","Yokohama"}
A_ANSWERS = {"Helsinki","Tokyo","Munich","Mexico City","Los Angeles","Seoul","Barcelona","Atlanta","Sydney","Athens","Beijing","Rio de Janeiro",
             "Lillehammer","Nagano","Salt Lake City","Turin"}
NAME_RULE = {  # first names, common words, or names carrying a known lexical confound in this dataset
 "Adelaide":"first name","Hobart":"first name","Kobe":"first name","Florence":"first name","Sofia":"first name","Victoria":"first name",
 "Hamilton":"first name","Nelson":"first name","Darwin":"surname of a botanist (botany items)","Napier":"surname of a mathematician",
 "Split":"common word","Bath":"common word","Reading":"common word","Siena":"first name (Sienna)","Verona":"first name",
"Utrecht":"known 'IBC Utrecht' misattribution (M28)","Mackay":"surname"}
EVENT_YEAR = {"Kyoto": 1990, "Sydney": 1981, "Vienna": 2005, "Hyderabad": 2010}
ANACHRONISTIC_BEFORE = {"Istanbul": 1930}   # name official from 1930; PI decision 6 concerns the 1903-1908 items only
cand = json.load(open(sys.argv[1])); out = {}; report = {}
for ans, cities in cand.items():
    keep, drop = [], {}
    for c in dict.fromkeys(cities):               # de-duplicate, keep order
        if c in HOSTS: drop[c] = "congress host"
        elif c in A_ANSWERS: drop[c] = "A answer"
        elif c in NAME_RULE: drop[c] = NAME_RULE[c]
        elif c == ans: drop[c] = "is the answer"
        elif c in ANACHRONISTIC_BEFORE and EVENT_YEAR.get(ans, 0) < ANACHRONISTIC_BEFORE[c]: drop[c] = "anachronistic name for this event year"
        else: keep.append(c)
    out[ans] = keep; report[ans] = dict(kept=len(keep), dropped=drop)
json.dump(out, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
print(json.dumps(report, indent=1, ensure_ascii=False))
