# Shahzad MS — Enterprise Architecture & Delivery Portfolio

Single-page responsive portfolio at https://shahzadms7.github.io/.

## Content

Six anonymized engagement stories, a discovery-to-handover workflow, 41 project families and 15 technology domains. Direct email, LinkedIn and GitHub routes. No tracking, form backend, cookies, hosted fonts or external runtime dependencies.

## Edit and build

`build.py` contains page structure and engagement stories. `portfolio-data.json` contains project-family content; `technology-data.json` holds the broader capability inventory. Styles and interactions are in `assets/css/portfolio.css` and `assets/js/portfolio.js`.

Run `python3 build.py` to regenerate the page, favicon and six legacy redirects. Preview using `python3 -m http.server 8765` at http://localhost:8765.

Core content and disclosure panels work without JavaScript. Search, filters, mobile menu and printing controls are progressively enhanced.

## Content rules

Do not add confidential client identities, identifying combinations or proprietary artifacts. Do not publish the unredacted master resume. Resume requests use email.

Separate production delivery, architecture/design, prototype/pilot, training and evaluation. A family aggregates experience; it does not imply every listed tool was deployed together. Match metrics to units and periods. Never present roadmap features, evaluated tools or availability targets as delivered results.

The catalog is resume-derived and owner-supplied, not independently certified. Product names in historical/evaluated inventories are not assertions of current availability. Future additions require source, chronology and confidentiality review.

## Deployment and recovery

GitHub Pages retains its existing main-branch configuration. Submit a branch and PR, verify rendered behavior, then merge and confirm the Pages workflow and live content.

Pre-redesign baseline: `ea2f66ec4f17d0497130b2e21e1ec2c3494cc745`. Roll back by reverting the redesign merge through a reviewed commit; do not force-reset main. The previous design remains in Git history.

Legacy solution URLs redirect to the relevant section of the single page.

## Verification

Check generated content, asset/anchor targets, confidentiality, desktop/mobile overflow, keyboard navigation, search/filter/reset, disclosures, JavaScript-disabled reading and console errors. Check mailto destinations without sending messages. Page load should use local assets only.
