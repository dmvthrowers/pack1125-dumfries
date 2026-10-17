"""Tests for scripts/publish_events.py:  python3 -m unittest discover -s scripts -p "test_*.py" """
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publish_events as pe

PAGE = "<main>\n      <!-- events:start -->\n      <!-- events:end -->\n      <div>gate</div>\n</main>"
DATA = {"synced": "2026-10-17", "events": [
    {"title": "Pack <Meeting> & More", "date": "2026-11-05", "start": "18:30", "end": "19:30", "place": "School, Dumfries", "details": "Bring a pencil."},
    {"title": "Campout", "date": "2026-11-13", "end_date": "2026-11-14"},
]}


class PublishTests(unittest.TestCase):
    def test_list_is_escaped_and_placed_between_the_markers(self):
        page, _ = pe.publish(DATA, PAGE)
        self.assertIn("Pack &lt;Meeting&gt; &amp; More", page)
        self.assertIn("Thu, Nov 5, 2026 · 6:30 PM – 7:30 PM", page)
        self.assertIn("Fri, Nov 13, 2026 – Sat, Nov 14, 2026", page)
        self.assertLess(page.index("events:start"), page.index("Campout"))
        self.assertLess(page.index("Campout"), page.index("events:end"))
        self.assertTrue(page.endswith("<div>gate</div>\n</main>".split("\n")[1] + "\n</main>") or "<div>gate</div>" in page)

    def test_places_only_when_allowed(self):
        self.assertNotIn("School, Dumfries", pe.publish(DATA, PAGE)[0])
        self.assertNotIn("LOCATION", pe.publish(DATA, PAGE)[1])
        page, ics = pe.publish(DATA, PAGE, show_places=True)
        self.assertIn("at School, Dumfries", page)
        self.assertIn("LOCATION:School\\, Dumfries", ics)

    def test_run_twice_gives_the_same_page(self):
        once, _ = pe.publish(DATA, PAGE)
        twice, _ = pe.publish(DATA, once)
        self.assertEqual(once, twice)

    def test_ics_has_times_and_all_day_ranges(self):
        _, ics = pe.publish(DATA, PAGE)
        self.assertIn("DTSTART:20261105T183000\r\n", ics)
        self.assertIn("DTEND:20261105T193000\r\n", ics)
        self.assertIn("DTSTART;VALUE=DATE:20261113\r\nDTEND;VALUE=DATE:20261115\r\n", ics)
        self.assertIn("SUMMARY:Pack <Meeting> & More", ics)
        self.assertIn("SUMMARY:A\\; B\\, C\\\\ D", pe.publish({"synced": "2026-10-17", "events": [{"title": "A; B, C\\ D", "date": "2026-11-05"}]}, PAGE)[1])
        self.assertTrue(ics.endswith("END:VCALENDAR\r\n"))

    def test_nothing_to_publish(self):
        self.assertIsNone(pe.publish({"synced": "2026-10-17", "events": []}, PAGE))
        self.assertIsNone(pe.publish(DATA, "<main>no markers</main>"))


if __name__ == "__main__":
    unittest.main()
