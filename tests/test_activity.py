import importlib.util
import unittest
from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('activity', ROOT/'scripts/refresh_activity.py')
activity = importlib.util.module_from_spec(spec); spec.loader.exec_module(activity)

class ActivityTests(unittest.TestCase):
    def test_count_and_date_parsing(self):
        parser = activity.CalendarParser()
        parser.feed('''<td id="b" data-date="2026-02-02" data-level="4"></td><tool-tip for="b">1,234 contributions on February 2nd.</tool-tip><td id="a" data-date="2026-02-01" data-level="0"></td><tool-tip for="a">No contributions on February 1st.</tool-tip>''')
        self.assertEqual(parser.days(), [{'date':'2026-02-01','level':0,'count':0},{'date':'2026-02-02','level':4,'count':1234}])
    def test_unknown_markup_fails_instead_of_inventing_data(self):
        parser = activity.CalendarParser(); parser.feed('<td id="a" data-date="2026-01-01" data-level="1"></td><tool-tip for="a">Changed text</tool-tip>')
        with self.assertRaises(ValueError): parser.days()
    def test_snapshot_is_real_and_well_formed(self):
        data = json.loads((ROOT/'site/activity.json').read_text())
        self.assertEqual(data['username'], 'shawkialaddin')
        for year, days in data['years'].items():
            self.assertGreater(len(days), 27)
            self.assertEqual(len(days), len({d['date'] for d in days}))
            for day in days:
                self.assertTrue(day['date'].startswith(year)); self.assertGreaterEqual(day['count'],0); self.assertIn(day['level'], range(5))
    def test_svg_is_valid_and_has_accessible_description(self):
        svg = ET.fromstring((ROOT/'assets/profile-header.svg').read_text())
        self.assertIsNotNone(svg.find('{http://www.w3.org/2000/svg}desc'))
    def test_no_job_pitch_or_removed_project(self):
        for path in ['README.md','site/index.html']:
            text = (ROOT/path).read_text().lower()
            for forbidden in ['saqqar','hire me','connect on linkedin','have something worth building']:
                self.assertNotIn(forbidden,text)

if __name__=='__main__': unittest.main()
