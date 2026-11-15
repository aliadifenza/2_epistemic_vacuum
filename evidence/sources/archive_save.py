#!/usr/bin/env python3
"""Save Wayback snapshots for every source URL and write a CSV mapping (source -> snapshot).
Run on the Mac:  python3 archive_save.py archive_urls.txt archive_map.csv
Needs no API key; one save per ~15 s to stay within archive.org rate limits."""
import sys, time, csv, urllib.request, urllib.parse, json
src, dst = sys.argv[1], sys.argv[2]
urls = [l.split('\t')[0].strip() for l in open(src) if l.strip() and not l.startswith('#')]
rows = []
for u in urls:
    snap = ''
    try:
        req = urllib.request.Request('https://web.archive.org/save/' + u, headers={'User-Agent': 'AlignedLab-Exp2/1.0'})
        with urllib.request.urlopen(req, timeout=120) as r:
            snap = r.headers.get('Content-Location') or r.geturl()
            if snap.startswith('/'): snap = 'https://web.archive.org' + snap
    except Exception as e:
        try:  # fall back to the newest existing snapshot
            q = 'https://archive.org/wayback/available?url=' + urllib.parse.quote(u, safe='')
            j = json.load(urllib.request.urlopen(q, timeout=60))
            snap = j['archived_snapshots']['closest']['url'] + '  (pre-existing; save failed: %s)' % e
        except Exception as e2:
            snap = 'FAILED: %s / %s' % (e, e2)
    print(u, '->', snap, flush=True)
    rows.append((u, snap, time.strftime('%Y-%m-%d %H:%M %Z')))
    time.sleep(15)
with open(dst, 'w', newline='') as f:
    csv.writer(f).writerows([('source_url', 'snapshot_url', 'saved_at')] + rows)
print('wrote', dst)
