# Agent Instructions

## Project

This is a recovered, static Thai-first character quiz and mini-game for the Khon Tid Buak Roadshow. It supports Thai, English, Myanmar, and Lao. The site is intended to run without a build step or external JavaScript runtime.

## Source of Truth

- `index.html` is the standalone version and the deployable site entry point. Its HTML, CSS, quiz, translations, and mini-game logic are maintained together.
- `bundled-template.html` and the hashed files in `assets/` are recovered reference material from the original bundled version. Do not treat them as the active app source or edit them as part of a change to `index.html` unless the task explicitly requires changing the recovered version too.
- `assets/` contains images, fonts, and the legacy runtime. Keep references relative to the project root so the site works when hosted from a subpath or opened locally.
- `README.md` documents local use and Netlify deployment. Keep it aligned with any changes to those workflows.

## Working Guidelines

- Preserve the no-build, no-framework setup. Do not add dependencies, a package manager, or a build pipeline for a small change unless requested.
- Keep edits focused. Follow the existing single-file structure in `index.html`; avoid broad formatting changes to recovered or generated content.
- Preserve existing language coverage and update the Thai, English, Myanmar, and Lao UI/content together when changing user-facing text or behavior.
- Preserve existing character IDs, screen IDs, DOM hooks, and local-storage behavior unless the requested change requires updating their consumers too.
- Keep all referenced images and fonts inside `assets/`; check that each referenced path exists when adding or changing an asset.
- Treat hashed recovered assets and the bundled template as source artifacts; do not regenerate, rename, or remove them without an explicit need.
- Do not introduce external CDN dependencies when an existing local asset or native browser API is sufficient.

## Validation

- There is no configured build or automated test suite. Do not claim tests passed when none were run.
- For a code change, inspect the affected HTML/CSS/JavaScript and check that referenced local assets exist. Use available static checks where practical.
- The site can be served locally with `python -m http.server 8765` and opened at `http://127.0.0.1:8765/`.
- Do not use browser automation for screenshots or visual preview; leave browser-based inspection to the user. Clearly report any validation that could not be performed.

## Deployment

Deploy the project root as a static site with `index.html` at the site root. No server-side runtime is required.