#!/usr/bin/env python3
"""Read the public GitHub calendar. No token or private repository data is used."""
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import argparse
import json
import re
import urllib.request

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.cells = {}; self.labels = {}; self.tip = None
    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if a.get('data-date') and a.get('data-level') is not None:
            self.cells[a['id']] = {'date': a['data-date'], 'level': int(a['data-level'])}
        if tag == 'tool-tip':
            self.tip = a.get('for'); self.labels[self.tip] = ''
    def handle_data(self, text):
        if self.tip is not None: self.labels[self.tip] += text
    def handle_endtag(self, tag):
        if tag == 'tool-tip': self.tip = None
    def days(self):
        result = []
        for key, cell in self.cells.items():
            label = self.labels.get(key, '').strip()
            match = re.match(r'([\d,]+) contributions?\b', label)
            if match: count = int(match[1].replace(',', ''))
            elif label.startswith('No contributions'): count = 0
            else: raise ValueError('Unknown GitHub contribution tooltip; refusing to fabricate counts')
            result.append({**cell, 'count': count})
        return sorted(result, key=lambda d: d['date'])

def fetch_year(year, username='shawkialaddin'):
    url = f'https://github.com/users/{username}/contributions?from={year}-01-01&to={year}-12-31'
    request = urllib.request.Request(url, headers={'User-Agent': 'ShawkiProfile/1.0', 'Accept-Language': 'en-US,en;q=0.9'})
    with urllib.request.urlopen(request, timeout=45) as response: source = response.read().decode('utf-8')
    parser = CalendarParser(); parser.feed(source)
    days = [d for d in parser.days() if d['date'].startswith(str(year))]
    if len(days) < 28: raise ValueError(f'Incomplete calendar for {year}')
    return days

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', default='site/activity.json'); parser.add_argument('--year', type=int, default=date.today().year); args = parser.parse_args()
    target = Path(args.output)
    years = {}
    for year in range(args.year, args.year - 3, -1):
        years[str(year)] = fetch_year(year)
    payload = {'username': 'shawkialaddin', 'source': 'https://github.com/shawkialaddin', 'updatedAt': datetime.now(timezone.utc).isoformat(), 'years': years}
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix('.tmp'); temporary.write_text(json.dumps(payload, separators=(',', ':')) + '\n'); temporary.replace(target)
    print(f'Wrote {sum(map(len, years.values()))} real calendar days for {len(years)} years')
if __name__ == '__main__': main()
