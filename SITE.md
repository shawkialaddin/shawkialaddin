# Personal page

A small dependency-free HTML/CSS/JavaScript page that accompanies the GitHub profile README. The design is a personal reference page, not a job application or sales page.

## Files

- `site/`: deployable website.
- `assets/profile-*.svg`: designed GitHub README sections, with `assets/profile-header.gif` providing the approved continuous portrait animation.
- `scripts/build_profile_assets.py`: rebuilds the designed README sections from the checked-in portrait and activity data.
- `scripts/refresh_activity.py`: refreshes the last three years of the public GitHub contribution calendar without a token.
- `.github/workflows/pages.yml`: verifies, refreshes, and deploys the site on pushes, manually, and daily.

## Run locally

Requires Python 3.10+; Node.js 20+ is used for checks.

```bash
python3 -m http.server 8000 --directory site
```

Open `http://localhost:8000`. Use an HTTP server rather than opening the HTML directly, because the contribution snapshot is loaded from JSON.

## GitHub Pages setup

In this repository's **Settings → Pages → Build and deployment → Source**, select **GitHub Actions**. Run the **Personal page** workflow from the Actions tab if necessary. The resulting URL is `https://shawkialaddin.github.io/shawkialaddin/`.

GitHub's standard workflow token can deploy to Pages after it has been enabled, but cannot enable Pages for the first time. The GitHub connector used to prepare this repository does not expose the required Pages administration action.

No custom domain has been configured. The previously linked `shawkialaddin.com` is not modified by this implementation.

## Activity data

The checked-in snapshot is real public GitHub contribution data, not sample activity. The daily deployment refreshes it into the deployed artifact without creating automated commits. It contains only dates, counts, and intensity levels from the public calendar, not private repository names or details. Contributions include more than commits. The calendar links each date to the corresponding GitHub profile overview.

If the public GitHub markup changes or fetching fails, the workflow keeps the last valid snapshot and emits a warning. The page shows its snapshot date. If the JSON cannot be loaded, the page explicitly says so and links to GitHub instead of inventing activity.

The README contribution board is a dated snapshot from the latest asset build. The interactive page refreshes at deployment. To regenerate the README artwork after a data update, run `python3 scripts/build_profile_assets.py` and commit the generated SVG files.

## Motion and accessibility

The portrait automatically disperses and reassembles, with no hero controls. Motion respects the operating system's reduced-motion preference, and a discreet footer preference can stop automatic motion. Keyboard users can operate the satellite with labeled rotation and zoom sliders, and navigate calendar dates with arrow keys. Nothing requires hover to read.

## Validation

```bash
python3 -m unittest discover -s tests -v
node --check site/app.js
node --test tests/calendar.test.cjs
```

The research description reflects the current Satellite Repair Lab README. It deliberately makes no claim of a published paper, flight qualification, or evaluated AI-generated repairs.

## Approved contribution portrait

`site/portrait-loop.gif` is the original approved 96-frame, 640×640 animation. The page shows it directly, with a still frame when reduced motion is selected. `assets/profile-header.gif` combines the same frames with the vector header for GitHub README compatibility. No manual disperse or reassemble controls are required.

The research and experiments sections use looping GIFs rendered from `site/satellite.js`, the same shaded 3D mesh used by the live page. Regenerate their frames with `node scripts/export_satellite.cjs` (requires `@napi-rs/canvas`), then encode the 96 PNG frames per section as looping GIFs with 100 ms frame duration. The live model retains drag, zoom, and reduced-motion controls.
