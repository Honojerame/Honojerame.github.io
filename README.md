# Precious Onojerame · Portfolio

A static portfolio for GitHub Pages, focused on computer engineering, embedded
systems, software, and applied machine learning.

## Editing

The source for page content and shared templates is
`scripts/build_portfolio.py`. It uses only the Python standard library.

```bash
python3 scripts/build_portfolio.py
```

Commit the generated HTML alongside changes to the generator. GitHub Pages serves
the checked-in files directly, so no server or build action is required.

- `assets/portfolio.css`: responsive theme, layout, diagrams, and print styles.
- `assets/portfolio.js`: mobile navigation and progressive contact-form handling.
- `assets/favicon.svg`: portfolio monogram.
- `index.html`: profile, selected projects, experience, recognition, and contact.
- `projects.html`: complete project collection.
- `project-*.html`: individual project case studies.

The existing package manifest, lockfile, learning demos, downloadable résumé, and
legacy assets remain available. The redesigned pages use a local font and have
no third-party JavaScript or runtime package dependency.

## Contact

The form retains the portfolio's existing Formspree endpoint. With JavaScript,
submission status reflects the server response and preserves the draft on
failure. Without JavaScript, it uses the native POST workflow. The email link
is available independently of the form.

Checking the form should use mocked requests unless an actual test message is
intended. Do not submit visitor data as part of automated validation.

## Accessibility

The pages include semantic landmarks, labeled inputs, a skip link, visible
keyboard focus, a keyboard-operable mobile menu, reduced-motion support, and
native links that remain usable without JavaScript. The conceptual diagrams do
not present decorative motion as live equipment telemetry.

## GitHub Pages

Keep the repository's existing Pages source settings. The publishing entry point
is the root `index.html`; all project URLs and the previous homepage section
anchors remain supported. Changes on a review branch go live when merged into
the branch selected in the repository's Pages settings.
