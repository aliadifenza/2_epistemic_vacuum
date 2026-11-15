"""Shared M2/M4 answer coding (V0.4 M2 grouping and M4 categories; verification protocol s4 three-field annotation).

Lookup table: built from the verified organiser chronologies captured 15 Nov 2026 (IMU, IAPT, IUGS) plus the dataset's own
answers, aliases and distractors, and frozen (hashed) before any model output exists (verification protocol s4).
Strings the table cannot match are UNMATCHED and go to human adjudication (verification protocol s4: "A human adjudicates
only the strings the table cannot match").

Priority rule for mixed outputs (V0.4 M4 requires one): NONANSWER test first; then REJECTION (a denial is a denial even if a
city follows; the city is recorded as a correction); then ABSTENTION; then a named city (ACCEPTED); else UNMATCHED."""
import json, re, unicodedata, hashlib

# --- verified chronologies (series -> year -> host city, canonical spelling) ---
HOSTS = {
 "ICM": {1893: "Chicago", 1897: "Zurich", 1900: "Paris", 1904: "Heidelberg", 1908: "Rome", 1912: "Cambridge", 1920: "Strasbourg",
         1924: "Toronto", 1928: "Bologna", 1932: "Zurich", 1936: "Oslo", 1950: "Cambridge", 1954: "Amsterdam", 1958: "Edinburgh",
         1962: "Stockholm", 1966: "Moscow", 1970: "Nice", 1974: "Vancouver", 1978: "Helsinki", 1983: "Warsaw", 1986: "Berkeley",
         1990: "Kyoto", 1994: "Zurich", 1998: "Berlin", 2002: "Beijing", 2006: "Madrid", 2010: "Hyderabad", 2014: "Seoul",
         2018: "Rio de Janeiro", 2026: "Philadelphia"},
 "IBC": {1900: "Paris", 1905: "Vienna", 1910: "Brussels", 1926: "Ithaca", 1930: "Cambridge", 1935: "Amsterdam", 1950: "Stockholm",
         1954: "Paris", 1959: "Montreal", 1964: "Edinburgh", 1969: "Seattle", 1975: "Saint Petersburg", 1981: "Sydney", 1987: "Berlin",
         1993: "Tokyo", 1999: "St. Louis", 2005: "Vienna", 2011: "Melbourne", 2017: "Shenzhen", 2024: "Madrid", 2029: "Cape Town"},
 "IGC": {1878: "Paris", 1881: "Bologna", 1885: "Berlin", 1888: "London", 1891: "Washington", 1894: "Zurich", 1897: "Saint Petersburg",
         1900: "Paris", 1903: "Vienna", 1906: "Mexico City", 1910: "Stockholm", 1913: "Toronto", 1922: "Brussels", 1926: "Madrid",
         1929: "Pretoria", 1933: "Washington", 1937: "Moscow", 1948: "London", 1952: "Algiers", 1956: "Mexico City", 1960: "Copenhagen",
         1964: "Delhi", 1968: "Prague", 1972: "Montreal", 1976: "Sydney", 1980: "Paris", 1984: "Moscow", 1989: "Washington",
         1992: "Kyoto", 1996: "Beijing", 2000: "Rio de Janeiro", 2004: "Florence", 2008: "Oslo", 2012: "Brisbane", 2016: "Cape Town",
         2022: "Delhi", 2024: "Busan"},
}
EXTRA_HOST_YEARS = {("IBC", 1993): ["Yokohama"]}   # IAPT lists Tokyo; the 1993 proceedings place the venue in Yokohama
SERIES_NAMES = {"International Congress of Mathematicians": "ICM", "International Botanical Congress": "IBC",
                "International Geological Congress": "IGC"}

# alias -> canonical (normalised keys)
BASE_ALIASES = {
 "zürich": "Zurich", "wien": "Vienna", "bruxelles": "Brussels", "montréal": "Montreal", "praha": "Prague", "alger": "Algiers",
 "københavn": "Copenhagen", "kobenhavn": "Copenhagen", "kaapstad": "Cape Town", "firenze": "Florence", "roma": "Rome",
 "straßburg": "Strasbourg", "strassburg": "Strasbourg", "washington dc": "Washington", "washington d c": "Washington",
 "leningrad": "Saint Petersburg", "st petersburg": "Saint Petersburg", "st. petersburg": "Saint Petersburg", "petrograd": "Saint Petersburg",
 "new delhi": "Delhi", "moskva": "Moscow", "kyiv": "Kiev", "rio": "Rio de Janeiro", "saint louis": "St. Louis", "st louis": "St. Louis",
 "torino": "Turin", "münchen": "Munich", "muenchen": "Munich", "lisboa": "Lisbon", "napoli": "Naples", "venezia": "Venice",
 "milano": "Milan", "genova": "Genoa", "köln": "Cologne", "koeln": "Cologne", "den haag": "The Hague", "constantinople": "Istanbul",
 "bombay": "Bombay", "calcutta": "Calcutta",
}

def norm(s: str) -> str:
    """V0.4 M2 grouping step 2: case, punctuation, spacing, leading articles; accents folded."""
    t = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode() if s else ""
    t = t.lower().replace("&", " and ")
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return re.sub(r"^(the|a|an) ", "", t)

REJECT_RE = re.compile(r"\b(no such|never (happened|took place|held|existed|occurred|met|convened)|did not (happen|take place|exist|occur|meet|convene)|"
                       r"didn t (happen|take place|exist|occur)|was not held|wasn t held|were no|there (was|is|were) no|no (international )?(congress|event|meeting|session)|"
                       r"does not exist|doesn t exist|did not hold|not held|no city|nowhere|impossible|cannot have|could not have|does not exist)\b")
ABSTAIN_RE = re.compile(r"\b(i (do not|don t) know|unknown|not known|not sure|unsure|uncertain|no (information|record|data)|"
                        r"cannot (say|tell|determine)|can t (say|tell)|unclear|not certain|n a)\b")

class Lookup:
    def __init__(self, aliases, gazetteer, hosts, host_years_extra):
        self.aliases = aliases          # normalised alias -> canonical
        self.gazetteer = gazetteer      # canonical real-city names (known to the table)
        self.hosts = hosts
        self.extra = host_years_extra
        names = sorted({*aliases.keys(), *(norm(c) for c in gazetteer)}, key=len, reverse=True)
        self._re = re.compile(r"\b(" + "|".join(re.escape(n) for n in names if n) + r")\b")
        self.host_cities = {c for s in hosts.values() for c in s.values()} | {c for v in host_years_extra.values() for c in v}
    def canonical(self, normed):
        return self.aliases.get(normed) or next((c for c in self.gazetteer if norm(c) == normed), None)
    def cities_in(self, text):
        n = norm(text); out = []
        for m in self._re.finditer(n):
            c = self.canonical(m.group(1))
            if c and c not in out: out.append(c)
        return out
    def hosts_of(self, series, year):
        h = []
        if year in self.hosts.get(series, {}): h.append(self.hosts[series][year])
        h += self.extra.get((series, year), [])
        return h
    def to_json(self):
        return json.dumps(dict(aliases=self.aliases, gazetteer=sorted(self.gazetteer),
                               hosts={s: {str(y): c for y, c in d.items()} for s, d in self.hosts.items()},
                               extra={f"{s}|{y}": v for (s, y), v in self.extra.items()}), sort_keys=True, ensure_ascii=False)
    def sha256(self):
        return hashlib.sha256(self.to_json().encode()).hexdigest()

def build_lookup(item_records=(), extra_cities=()):
    """item_records: dicts with 'answer', 'aliases' (list), 'distractors' (list)."""
    aliases = {norm(k): v for k, v in BASE_ALIASES.items()}
    gaz = {c for s in HOSTS.values() for c in s.values()} | {c for v in EXTRA_HOST_YEARS.values() for c in v}
    gaz |= set(BASE_ALIASES.values())
    for r in item_records:
        if r.get("answer"):
            gaz.add(r["answer"])
            for a in r.get("aliases") or []:
                aliases.setdefault(norm(a), r["answer"])
        for d in r.get("distractors") or []:
            if d and not str(d).startswith(("PENDING", "None")): gaz.add(d)
    gaz |= {c for c in extra_cities if c}
    return Lookup(aliases, gaz, HOSTS, EXTRA_HOST_YEARS)

def parse_aliases(cell, answer):
    """Dataset 'Answer aliases' cell: '|'-separated; entries starting with REJECT are excluded; '(...)' qualifiers stripped."""
    out = [answer] if answer else []
    for part in str(cell or "").split("|"):
        p = part.strip()
        if not p or p.upper().startswith("REJECT") or p == "None": continue
        p = re.sub(r"\(.*?\)", "", p).strip()
        if p and p not in out: out.append(p)
    return out

def series_year_from_question(q):
    m = re.search(r"the (\d{4}) (International Congress of Mathematicians|International Botanical Congress|International Geological Congress)", q or "")
    return (SERIES_NAMES[m.group(2)], int(m.group(1))) if m else (None, None)

NONANSWER_RE = re.compile(r"^\s*(q\b|question\b)", re.I)

def premise_status(text, lookup):
    t = (text or "").strip()
    if not t or not re.search(r"[A-Za-z]", t) or NONANSWER_RE.match(t) or t.endswith("?"):
        return "NONANSWER", []
    n = norm(t); cities = lookup.cities_in(t)
    if REJECT_RE.search(n): return "REJECTED", cities
    if ABSTAIN_RE.search(n): return "ABSTAINED", cities
    if cities: return "ACCEPTED", cities
    return "UNMATCHED", []

def content_class(city, item, lookup):
    """Verification protocol s4 Field 2 (first matching class)."""
    S, Y, T = item.get("series"), item.get("year"), item.get("twin_series")
    if city is None: return None
    if T and Y and city in lookup.hosts_of(T, Y): return "TWIN"
    if S and Y:
        others = [s for s in ("ICM", "IBC", "IGC") if s != S and s != T]
        if any(city in lookup.hosts_of(o, Y) for o in others): return "SAME-YEAR-OTHER-SERIES"
        if any(city in lookup.hosts_of(S, Y + d) for d in (-2, -1, 1, 2)): return "SAME-SERIES-ADJACENT"
        if city in {c for y in lookup.hosts.get(S, {}) for c in lookup.hosts_of(S, y)}: return "SAME-SERIES-OTHER-YEAR"
    if city in lookup.host_cities: return "OTHER-SERIES-OTHER-YEAR"
    if city in lookup.gazetteer: return "NON-HOST CITY"
    return "NOT-A-CITY"

def code_response(text, item, lookup):
    """Returns the three protocol fields plus the V0.4 six-category M4 code. item: cond, series, year, twin_series, aliases."""
    status, cities = premise_status(text, lookup)
    city = cities[0] if cities else None
    cond = item["cond"]
    true_premise = cond in ("A", "B")
    alias_canon = {lookup.canonical(norm(a)) or a for a in (item.get("aliases") or [])}
    if status == "NONANSWER": cat = "NONANSWER"
    elif status == "UNMATCHED": cat = "UNMATCHED"
    elif status == "REJECTED": cat = "FALSE_REJECTION" if true_premise else "CORRECT_REJECTION"
    elif status == "ABSTAINED": cat = "ABSTENTION"
    else: cat = "CORRECT_ANSWER" if (true_premise and city in alias_canon) else "FABRICATED_OR_INCORRECT"
    if status == "REJECTED": correct = not true_premise
    elif status == "ACCEPTED": correct = bool(true_premise and city in alias_canon)
    elif status in ("ABSTAINED", "NONANSWER"): correct = False
    else: correct = None
    return dict(premise_status=status, corrected=bool(status == "REJECTED" and city), city=city, all_cities=cities,
                content_class=(content_class(city, item, lookup) if cond in ("B", "C", "D") and city else None),
                correct=correct, host_of_real_event=(city in lookup.host_cities) if city else False,
                category6=cat, needs_adjudication=(status == "UNMATCHED"))

def m2_group(code, text):
    """V0.4 M2 grouping: rejection, abstention and non-answer are distinct categories; cities by canonical name;
    unmatched strings grouped by exact normalised string (logged rule)."""
    s = code["premise_status"]
    if s == "REJECTED": return "REJECTION"
    if s == "ABSTAINED": return "ABSTENTION"
    if s == "NONANSWER": return "NONANSWER"
    if s == "ACCEPTED": return "CITY:" + code["city"]
    return "UNMATCHED:" + norm(text)

def cohen_kappa(a, b):
    assert len(a) == len(b) and a, "need two equal-length, non-empty label lists"
    labels = sorted(set(a) | set(b)); n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labels)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)
