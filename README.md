# Precious Onojerame · Portfolio

A static portfolio for GitHub Pages, focused on processor architecture, RTL,
AI accelerator dataflow, GPU-style memory, and on-chip communication.

## RTL architecture projects

The [Circuit Works collection](engineering/README.md) includes four implemented
projects: a four-core RV32I cluster, INT8 systolic tile, warp-memory structures,
and a buffered mesh NoC. Each includes RTL, testbenches, architectural guides,
verification plans, independent checks, and reproducible measurements.

```sh
cd engineering
make test
make lint
make synth
make report
```

See [tool setup](engineering/docs/getting-started.md). The GitHub Actions RTL
workflow runs the same checks. Generic synthesis does not establish physical
timing, area, or power. The website describes the implemented educational scope.

## Editing

The source for page content and shared templates is
`scripts/build_portfolio.py`. It uses only the Python standard library.

```bash
python3 scripts/build_portfolio.py
python3 scripts/package_engineering.py
```

Commit the generated HTML alongside changes to the generator. GitHub Pages serves
the checked-in files directly, so no server or build action is required.

- `assets/portfolio.css`: responsive theme, layout, diagrams, and print styles.
- `assets/portfolio.js`: mobile navigation and progressive contact-form handling.
- `assets/favicon.svg`: portfolio monogram.
- `index.html`: profile, selected projects, experience, recognition, and contact.
- `projects.html`: complete project collection.
- `project-*.html`: individual project case studies.
- `engineering.html`: documentation hub and verification overview.
- `engineering/`: complete hardware project source and documentation.
- `scripts/engineering_projects.py`: hardware case studies and circuit diagrams.
- `downloads/circuit-works.zip`: standalone source, test, documentation, and results bundle.

The main portfolio now prioritizes the four RTL studies, followed by AMHS and
two applied research projects. The six less relevant coursework/browser case
pages have been removed. The package manifest, lockfile, résumé, and unrelated
legacy assets remain. The redesigned pages use a local font and have
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
is the root `index.html`; the retained project URLs and previous homepage section
anchors remain supported. Changes on a review branch go live when merged into
the branch selected in the repository's Pages settings.
