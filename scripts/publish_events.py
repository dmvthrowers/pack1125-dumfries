#!/usr/bin/env python3
"""Put the calendar events that scripts/sync_calendar.py pulled (events.generated.json) onto docs/calendar.html
and write docs/calendar.ics. Run by the deploy workflow on its own copy of the files, after the sync and before
the site is published; nothing is committed. With no events.generated.json this does nothing.

    python3 scripts/sync_calendar.py && python3 scripts/publish_events.py

The list goes between the "events:start" and "events:end" comments in docs/calendar.html. In the repository that
spot is empty, so the page is the same without the sync. Places are left off unless CALENDAR_SHOW_PLACES=true.
Standard library only.
"""
import datetime as dt
import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
LIMIT = 20
START, END = "<!-- events:start -->", "<!-- events:end -->"


def fmt_date(d):
    return f"{DAYS[d.weekday()]}, {MONTHS[d.month - 1]} {d.day}, {d.year}"


def fmt_time(hhmm):
    h, m = int(hhmm[:2]), int(hhmm[3:5])
    return f"{(h % 12) or 12}:{m:02d} {'AM' if h < 12 else 'PM'}"


def when_text(e):
    d = dt.date.fromisoformat(e["date"])
    text = fmt_date(d)
    if e.get("end_date"):
        text += " – " + fmt_date(dt.date.fromisoformat(e["end_date"]))
    if e.get("start"):
        text += " · " + fmt_time(e["start"]) + (" – " + fmt_time(e["end"]) if e.get("end") and not e.get("end_date") else "")
    return text


def render_list(events, synced, show_places):
    esc = html.escape
    rows = []
    for e in events[:LIMIT]:
        where = f' <span class="event-place">at {esc(e["place"])}</span>' if show_places and e.get("place") else ""
        details = f'<p>{esc(e["details"])}</p>' if e.get("details") else ""
        rows.append(f'<li><span class="event-date">{esc(when_text(e))}</span><strong>{esc(e["title"])}</strong>{where}{details}</li>')
    d = dt.date.fromisoformat(synced)
    return (f'{START}\n      <h2>Upcoming Pack Events</h2>\n      <ul class="event-list">\n        ' + "\n        ".join(rows) +
            '\n      </ul>\n      <p class="btn-row"><a class="btn btn-navy" href="calendar.ics" download>Add these events to your calendar (.ics)</a></p>\n'
            f'      <p class="cal-fallback">Pulled from the pack calendar on {MONTHS[d.month - 1]} {d.day}, {d.year}. Dates and locations may change.</p>\n      {END}')


def render_ics(events, synced, show_places):
    def text(t):
        return str(t).replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\r", "").replace("\n", "\\n")

    def fold(line):                                                  # lines are at most 75 bytes; continuations start with a space
        out, cur = [], ""
        for ch in line:
            if len((cur + ch).encode()) > (75 if not out else 74):
                out.append(cur)
                cur = ch
            else:
                cur += ch
        out.append(cur)
        return "\r\n ".join(out)

    stamp = synced.replace("-", "") + "T000000Z"
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Cub Scout Pack 1125//Pack Site//EN", "CALSCALE:GREGORIAN",
             "METHOD:PUBLISH", "X-WR-CALNAME:Cub Scout Pack 1125"]
    for e in events:
        d = dt.date.fromisoformat(e["date"])
        last = dt.date.fromisoformat(e["end_date"]) if e.get("end_date") else d
        slug = re.sub(r"[^a-z0-9]+", "-", e["title"].lower()).strip("-") or "event"
        clock = (e.get("start") or "").replace(":", "")
        lines += ["BEGIN:VEVENT", f"UID:{d:%Y%m%d}{clock}-{slug}@dmvthrowers.club", f"DTSTAMP:{stamp}"]
        if e.get("start"):                                           # a time of day is written as local ("floating") time
            lines.append(f"DTSTART:{d:%Y%m%d}T{clock}00")
            if e.get("end"):
                lines.append(f"DTEND:{last:%Y%m%d}T{e['end'].replace(':', '')}00")
        else:
            lines += [f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{last + dt.timedelta(days=1):%Y%m%d}"]
        lines.append(f"SUMMARY:{text(e['title'])}")
        if show_places and e.get("place"):
            lines.append(f"LOCATION:{text(e['place'])}")
        if e.get("details"):
            lines.append(f"DESCRIPTION:{text(e['details'])}")
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(x) for x in lines) + "\r\n"


def publish(data, page_text, show_places=False):
    """Returns (new calendar.html text, calendar.ics text), or None when there is nothing to publish."""
    events = [e for e in data.get("events", []) if e.get("title") and e.get("date")]
    if not events or START not in page_text or END not in page_text:
        return None
    block = render_list(events, data["synced"], show_places)
    page = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, page_text, count=1, flags=re.S)
    return page, render_ics(events, data["synced"], show_places)


def main():
    src = ROOT / "events.generated.json"
    if not src.exists():
        print("Publish events skipped: no events.generated.json (no calendar sync ran).")
        return 0
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
        data["synced"] = dt.date.fromisoformat(data["synced"]).isoformat()
    except (OSError, ValueError, KeyError, TypeError):
        print("Publish events skipped: events.generated.json could not be read.")
        return 0
    page_path = DOCS / "calendar.html"
    show = os.environ.get("CALENDAR_SHOW_PLACES", "").strip().lower() == "true"
    done = publish(data, page_path.read_text(encoding="utf-8"), show)
    if not done:
        print("Publish events skipped: no upcoming events, or calendar.html has no events markers.")
        return 0
    page_path.write_text(done[0], encoding="utf-8")
    (DOCS / "calendar.ics").write_bytes(done[1].encode("utf-8"))
    print(f"Publish events: {len(data['events'])} event(s) on calendar.html (first {min(len(data['events']), LIMIT)} listed) and calendar.ics.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
