# Chrono Arcade

History games about when and where things happened. A sibling to Atlas Arcade.

- **Decade Drop**: sort ten events into five decades, centuries, or millennia.
- **Where and When**: drop a pin where it happened and dial in the year. Up to 1,000 points per event.
- **Closer Than You Think**: which event is closer in time to the one on top?

Daily sets are the same for everyone on a given date; Practice mode is endless. Stats live in the browser's local storage.

A static site with no build step. Serve the folder with any web server or deploy to Vercel as-is.

## Data
- Events: 278 hand-curated events in `data/events.txt` (one per line: `year|title|place|lat|lng|category|fact`, `~` marks circa, negative years are BCE). Run `python3 tools/build.py` to rebuild `data/events.json`.
- Map: Natural Earth 1:50m country boundaries (modern borders) via Atlas Arcade's world data.
