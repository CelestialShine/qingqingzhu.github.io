# Qingqing Zhu — Personal Research Website

A dependency-free academic website built from Qingqing Zhu's CV. It uses semantic HTML, custom responsive CSS, and a small amount of vanilla JavaScript, so it can be hosted on GitHub Pages without a build step.

Live site: <https://celestialshine.github.io/qingqingzhu.github.io/>

GitHub repository: <https://github.com/CelestialShine/qingqingzhu.github.io>

## Preview locally

```bash
python3 -m http.server 8000 --directory personal-website
```

Then open `http://localhost:8000`.

Run the dependency-free integrity check with:

```bash
python3 personal-website/scripts/check_site.py
```

## Structure

- `index.html` — profile, research themes, selected publications, experience, honors, talks, and contact details
- `styles.css` — responsive visual system, light/dark themes, and reduced-motion support
- `script.js` — theme switcher, mobile navigation, publication filters, reveal effects, and active navigation
- `assets/` — reserved for a future professional headshot or social preview image

## Content and privacy

The site content was adapted from `NIW/Personal Information and Identification/RenderCV_Classic_Theme (1).pdf`. It intentionally omits the applicant's phone number, street address, passport image, and immigration records. No files from the NIW petition are copied into this public website folder.

## Design research

The information architecture was informed by the MIT-licensed [al-folio](https://github.com/alshedivat/al-folio) academic website project, with a custom dependency-free implementation for easier deployment and maintenance. Additional portfolio patterns were reviewed from Academic Pages, HugoBlox Academic CV, as-folio, and Bartosz Jarocki's CV project. No template source code was copied.

## Deploy updates on GitHub Pages

The public site deploys from the `main` branch of `CelestialShine/qingqingzhu.github.io`. Copy the contents of `personal-website/` to the repository root, commit, and push to `main`.

Because the site has no build dependencies, it will publish directly.
