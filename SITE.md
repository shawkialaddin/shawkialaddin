# Personal page

A small dependency-free HTML/CSS/JavaScript page that accompanies the GitHub profile README. The design is a personal reference page, not a job application or sales page.

## Files

- `site/`: deployable website.
- `assets/profile-header.svg`: automatically animated GitHub README header.
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

## Motion and accessibility

The portrait automatically disperses and reassembles, with no hero controls. Motion respects the operating system's reduced-motion preference, and a discreet footer preference can stop automatic motion. Keyboard users can operate the satellite with labeled rotation and zoom sliders, and navigate calendar dates with arrow keys. Nothing requires hover to read.

## Validation

```bash
python3 -m unittest discover -s tests -v
node --check site/app.js
node --test tests/calendar.test.cjs
```

The research description reflects the current Satellite Repair Lab README. It deliberately makes no claim of a published paper, flight qualification, or evaluated AI-generated repairs.
