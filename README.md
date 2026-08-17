# 🏡🐱 MoniCat Manor

> Draw a cat. Name it. Give it a personality. Watch it join a shared, illustrated
> manor with everyone else's cats where it can earn favorites, get petted, and
> maybe become today's most-loved cat in the house.

MoniCat Manor is a Django full-stack web application built for Code Institute's
Milestone 3 project. Users create custom cat portraits on an in-browser canvas,
give them a name and personality, and publish them into a shared illustrated
scene ("the manor") that changes appearance with the time of day. Visitors can
browse, comment, favorite, and pet cats with the most-petted cat each day
earning a "Cat of the Day" spotlight.

**Live site:** https://monicat-manor-8f86a39892eb.herokuapp.com/
**Repository:** https://github.com/MonicaFeis/monicat-manor
**Demo video:** [https://github.com/user-attachments/assets/eb7dfd30-3fa1-4687-9325-e1b42d4e5918]

---

## 📖 Table of Contents

- [Demo Video](#demo-video)
- [Project Goals](#project-goals)
- [UX Design](#ux-design)
- [Wireframes](#wireframes)
- [Data Model](#data-model)
- [User Stories](#user-stories)
- [Features](#features)
- [Features Not Included](#features-not-included)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Bugs Found & Fixed](#bugs-found--fixed)
- [Deployment](#deployment)
- [Credits](#credits)

---

## Demo Video

A short walkthrough covering account creation, drawing and publishing a
cat, the petting/favoriting mechanics, and the Cat of the Day spotlight:

**[Watch the demo video](#)** *(add your video link here)*

---

## Project Goals

**External user's goal:** create and personalize a cat character with minimal
effort, then share it with a small community of other cat lovers and no drawing
skill required to participate meaningfully.

**Site owner's goal:** provide a playful, low-friction creative outlet that
encourages people to return daily (via the Cat of the Day mechanic), while
keeping the shared space cohesive through a consistent visual theme and
straightforward moderation tools.

---

## UX Design

### Design evolution

The project went through two full visual identities during development:

1. **Cozy cottage palette** Warm terracotta, honey, and sage tones, paired
   with a hand-drawn cottage-garden background, reflecting a cottagecore
   aesthetic.
2. **Final theme: cozy-fantasy periwinkle** A deep blue/periwinkle/lavender
   palette layered over the same cottage illustration, chosen to match the
   project's hand-drawn logo mark. Warm accent colors (honey, rose) were kept
   for contrast against the cooler primary palette, giving the site a
   "magical twilight cottage" feel rather than a flat single-temperature
   palette.

| Token | Hex | Use |
|---|---|---|
| Periwinkle Blue | `#4E73F8` | Primary accent, buttons |
| Deep Blue | `#2A3B8F` | Headings, nav text |
| Soft Lavender | `#E9E6FB` | Secondary backgrounds, badges |
| Lavender Mist | `#F5F3FE` | Page background |
| Dusty Violet | `#A39BD6` | Borders, muted text |
| Mint Accent | `#78C8AA` | Public badge, success states |
| Rose Accent | `#E89BB2` | Private badge |

**Typography:** Fredoka (headings/buttons), DM Sans (body text), Caveat
(handwritten logo wordmark).

### The scene as the interface

Rather than a conventional hero-banner homepage, the illustrated manor scene
**is** the homepage is landing on the site immediately shows the shared space
with any public cats already living in it, in the spirit of interactive
"digital terrarium" style sites. The scene's background also changes between
day, dusk, and night illustrations based on the visitor's own local time,
giving the space a sense of being alive rather than static.

---

## Wireframes

Low-fidelity wireframes were sketched before implementation to plan the
core page layouts (the manor scene, gallery, and cat creation flow).
The final build diverged in some visual details as the design evolved
(see Design evolution above), but the underlying page structure and
navigation stayed consistent with the original plan.

### Homepage / manor scene

| Desktop | Tablet | Mobile |
|---|---|---|
| ![Homepage desktop wireframe](docs/wireframes/homepage-desktop.png) | ![Homepage tablet wireframe](docs/wireframes/homepage-tablet.png) | ![Homepage mobile wireframe](docs/wireframes/homepage-mobile.png) |

### Navbar (tablet/mobile)

![Navbar tablet and mobile wireframe](docs/wireframes/navbar-tablet-mobile.png)

### Gallery

| Desktop | Tablet | Mobile |
|---|---|---|
| ![Gallery desktop wireframe](docs/wireframes/gallery-desktop.png) | ![Gallery tablet wireframe](docs/wireframes/gallery-tablet.png) | ![Gallery mobile wireframe](docs/wireframes/gallery-mobile.png) |

### My Cats

| Desktop | Tablet | Mobile |
|---|---|---|
| ![My Cats desktop wireframe](docs/wireframes/my-cats-desktop.png) | ![My Cats tablet wireframe](docs/wireframes/my-cats-tablet.png) | ![My Cats mobile wireframe](docs/wireframes/my-cats-mobile.png) |

### Create / Edit a cat

The form is long enough to need two screenshots per breakpoint (top
and bottom of the page):

| | Desktop | Tablet | Mobile |
|---|---|---|---|
| **Part 1 (top)** | ![Cat form desktop wireframe part 1](docs/wireframes/cat-form-desktop-1.png) | ![Cat form tablet wireframe part 1](docs/wireframes/cat-form-tablet-1.png) | ![Cat form mobile wireframe part 1](docs/wireframes/cat-form-mobile-1.png) |
| **Part 2 (bottom)** | ![Cat form desktop wireframe part 2](docs/wireframes/cat-form-desktop-2.png) | ![Cat form tablet wireframe part 2](docs/wireframes/cat-form-tablet-2.png) | ![Cat form mobile wireframe part 2](docs/wireframes/cat-form-mobile-2.png) |

### Cat detail page

| Desktop | Tablet | Mobile |
|---|---|---|
| ![Cat detail desktop wireframe](docs/wireframes/cat-detail-desktop.png) | ![Cat detail tablet wireframe](docs/wireframes/cat-detail-tablet.png) | ![Cat detail mobile wireframe](docs/wireframes/cat-detail-mobile.png) |

### Sign up page

| Desktop | Tablet | Mobile |
|---|---|---|
| ![Sign up desktop wireframe](docs/wireframes/sign-up-desktop.png) | ![Sign up tablet wireframe](docs/wireframes/sign-up-tablet.png) | ![Sign up mobile wireframe](docs/wireframes/sign-up-mobile.png) |

### Log in page

| Desktop | Tablet | Mobile |
|---|---|---|
| ![Log in desktop wireframe](docs/wireframes/log-in-desktop.png) | ![Log in tablet wireframe](docs/wireframes/log-in-tablet.png) | ![Log in mobile wireframe](docs/wireframes/log-in-mobile.png) |

### 404 error page

| Desktop | Tablet | Mobile |
|---|---|---|
| ![404 desktop wireframe](docs/wireframes/404-desktop.png) | ![404 tablet wireframe](docs/wireframes/404-tablet.png) | ![404 mobile wireframe](docs/wireframes/404-mobile.png) |

### 500 error page

| Desktop | Tablet | Mobile |
|---|---|---|
| ![500 desktop wireframe](docs/wireframes/500-desktop.png) | ![500 tablet wireframe](docs/wireframes/500-tablet.png) | ![500 mobile wireframe](docs/wireframes/500-mobile.png) |

Data model planning, ERD, and ID structure were also worked through
before implementation please check [DATA_MODEL.md](DATA_MODEL.md) for the full
breakdown.

---

## Data Model

```mermaid
erDiagram
    USER ||--o{ CAT : owns
    USER ||--o{ COMMENT : writes
    USER ||--o{ REACTION : favorites
    USER ||--o{ DAILYPET : pets
    CAT ||--o{ COMMENT : receives
    CAT ||--o{ REACTION : receives
    CAT ||--o{ DAILYPET : receives

    USER {
        int id PK
        string username
        string email
    }
    CAT {
        int id PK
        int owner_id FK
        string name
        text personality
        string coat_color
        image drawing_image
        bool is_public
        datetime created_on
    }
    COMMENT {
        int id PK
        int cat_id FK
        int author_id FK
        text body
        datetime created_on
    }
    REACTION {
        int id PK
        int cat_id FK
        int user_id FK
        datetime created_on
    }
    DAILYPET {
        int id PK
        int cat_id FK
        int user_id FK
        date date
    }
```

**Relationships:**
- One `User` → many `Cat` (a user can own multiple cats)
- One `Cat` → many `Comment`; one `User` → many `Comment`
- `Cat` ↔ `User` many-to-many via `Reaction` (a permanent "favorite" one
  per user per cat, enforced with `unique_together`)
- `Cat` ↔ `User` many-to-many via `DailyPet` (a *daily* interaction that
  resets every day, one per user per cat per date, also enforced with
  `unique_together`) this is what powers the Cat of the Day feature

Full field-by-field reasoning lives in [DATA_MODEL.md](DATA_MODEL.md).

---

## User Stories

Full stories tracked as GitHub Issues. Format: **As a / I want / so that →
Acceptance Criteria → Priority (MoSCoW)**.

*(TODO: add a screenshot of your GitHub Issues board here — open this
file in GitHub's web editor and drag the image directly into this
spot, same method as the demo video below, rather than committing it
as a file in `docs/`.)*

### Epic 1: Authentication & Account

**US01 Register an account** *(Must have)*
As a visitor, I want to register for an account, so that I can create cats.
- Registration form accessible from nav and the logged-out toolbar
- On success, user is auto-logged-in and redirected to the manor

**US02 Log in / Log out** *(Must have)*
As a registered user, I want to log in and out, so that my account stays secure.
- Login/logout accessible from nav bar
- Logged-in state shows username in nav

### Epic 2: Creating & Managing Cats

**US03 Draw a cat** *(Must have)*
As a user, I want to draw a cat on a canvas with a chosen coat color, so that
I create something uniquely mine.
- Canvas supports mouse and touch drawing
- A limited, on-theme color palette is available
- Undo (single stroke) and Clear are both available
- **Cannot submit without drawing something** A clear warning is shown if
  the canvas is blank

**US04 Name and describe my cat** *(Must have)*
As a user, I want to give my cat a name and personality, so it has character.
- Both fields are required with example placeholder text shown

**US05 Edit / Delete my cat** *(Must have)*
As a user, I want to edit or delete a cat I own, so I can fix mistakes or
remove it.
- Editing preloads the existing drawing rather than starting blank
- Delete requires confirmation
- Both actions are available from "My Cats" and directly from the manor
  popup for cats I own

**US06 Toggle a cat's visibility** *(Should have)*
As a user, I want to quickly hide/show a cat from the public manor, so I
don't need the full edit form just to change visibility.
- One-click toggle badge on "My Cats"

### Epic 3: The Shared Manor & Gallery

**US07 View the shared manor scene** *(Must have)*
As any visitor, I want to see the illustrated scene with public cats the
moment I land on the site.
- No login required to view
- Background reflects real time of day (day/dusk/night)

**US08 View a cat's mini-profile** *(Must have)*
As any visitor, I want to click a cat to see its name and personality.
- Opens a popup with name, personality, and (for owners) edit/delete

**US09 Browse the gallery** *(Should have)*
As any visitor, I want a simple paginated grid of all public cats.

### Epic 4: Community Interaction

**US10 Favorite a cat** *(Should have)*
As a logged-in user, I want to permanently favorite a cat (🐾), so I can show
lasting appreciation.
- Toggleable, persists indefinitely, one per user per cat

**US11 Pet a cat today** *(Could have)*
As a logged-in user, I want to give a cat a daily "pet" (💗), so that I have
a reason to return each day and can help crown the Cat of the Day.
- Resets every day; one pet per user per cat per day
- Cannot be un-done same day (distinct from the permanent favorite)

**US12 See the Cat of the Day** *(Could have)*
As any visitor, I want to see which cat has been petted most today,
highlighted with a spotlight banner and crown badge.

**US13 Comment on a cat** *(Should have)*
As a logged-in user, I want to comment on a public cat.
- Full CRUD on my own comments

### Epic 5: Site Owner / Admin

**US14 Moderate content** *(Should have)*
As the site owner, I want to hide or delete inappropriate cats/comments via
Django admin. Restricted to superuser access only (documented as a
deliberate scope decision, see Features Not Included).

### Epic 6: General Experience

**US15 Responsive layout** *(Must have)*
As any user, I want the site to work well on mobile, tablet, and desktop.

**US16 Friendly error pages** *(Should have)*
As any visitor, I want a custom 404/500 page matching the site's theme
instead of a generic error screen.

---

## Features

- Full CRUD on cat portraits and comments
- Canvas drawing tool: touch + mouse support, undo, clear, coordinate
  scaling for any screen size, required-drawing validation
- 8-color on-theme palette for coat color
- Time-of-day-reactive manor background (day/dusk/night)
- Click-to-reveal cat mini-profiles with inline owner controls
- Permanent favorites (🐾) and daily pets (💗) as two distinct interactions
- "Cat of the Day" spotlight banner + crown badge (manor and gallery)
- Paginated manor scene, gallery, and "My Cats"
- One-click public/private visibility toggle
- Django admin moderation (superuser-only)
- Custom 404 and 500 error pages
- Responsive across mobile, tablet, and desktop
- Custom external stylesheet, properly separated from HTML

## Features Not Included

Documented as deliberate scope decisions:

- **Multi-moderator roles** This is a solo-developer assignment project
  with a single account (the site owner), so a staff permission tier would
  add complexity with no real use case; moderation is superuser only by
  design
- **Pre-publish approval queue for content moderation** Content
  (cats and comments) is deliberately made visible immediately on
  submission rather than held for approval first. A pre-approval
  queue would mean every test cat or comment an assessor submits
  stays invisible until manually approved, adding real friction to
  evaluating the app. Post-hoc moderation instead lets the site
  owner (superuser) instantly hide or delete any cat or comment via
  Django admin `CatAdmin` exposes `is_public` as a one-click
  editable field, and `CommentAdmin`/comment deletion covers the
  rest which satisfies real moderation needs without blocking
  normal use. This mirrors how most social platforms actually work
  (post first, remove if needed) rather than the smaller subset that
  gate everything behind approval
- **Automated content filtering** Deliberately left out for the
  same reason as above: an aggressive filter risks flagging or
  blocking legitimate content that a mentor or assessor enters while
  testing the app, obscuring functionality rather than demonstrating
  it
- **Password reset flow** Django's built-in URLs exist but no templates
  were built for them, since it wasn't part of the core user stories
- **Next-gen format conversion for the static background scene
  illustrations** Cat drawings (the majority of the site's imagery) are
  automatically served in the optimal format and quality via Cloudinary's
  `f_auto,q_auto` transformation, but the hand-drawn manor background
  images are static files and weren't manually converted to WebP/AVIF.
  Lighthouse still flags some remaining "Improve image delivery" savings
  on the homepage as a result I left as a deliberate time trade-off
  rather than a missed bug, since performance was otherwise already
  substantially improved (see Testing)
- Notifications, follower system, and real-time (no-refresh) updates

---

## Technologies Used

- **Backend:** Python, Django 4.2
- **Database:** PostgreSQL (production, via Heroku), SQLite (local dev)
- **Frontend:** HTML5, CSS3 (external stylesheet), JavaScript (Canvas API,
  Fetch API), Bootstrap 5
- **Media storage:** Cloudinary (production image hosting)
- **Static files:** WhiteNoise
- **Deployment:** Heroku
- **Version control:** Git & GitHub

---

## Testing

### Validator tools used

| Tool | Checks | Link |
|---|---|---|
| W3C Nu Html Checker | HTML | https://validator.w3.org/ |
| W3C CSS Validator (Jigsaw) | CSS | https://jigsaw.w3.org/css-validator/ |
| JSHint | JavaScript | https://jshint.com/ |
| Code Institute PEP8 Python Linter | Python (PEP8) | https://pep8ci.herokuapp.com/ |
| Flake8 Linting| Python (PEP8) | https://flake8.pycqa.org/|
| Lighthouse | Performance, Accessibility, Best Practices, SEO | Built into Chrome DevTools |
| TinyPNG | Image compression | https://tinypng.com/ |

### Manual testing performed

Extensive manual testing was carried out throughout development across
desktop, tablet, and mobile viewport sizes, and across two user accounts to
verify permission boundaries (owner-only edit/delete, private cat
visibility, comment ownership). See [Bugs Found & Fixed](#bugs-found--fixed)
for the specific issues this testing surfaced and how each was resolved.

### Automated / validator testing

| Tool | Target | Result |
|---|---|---|
| [W3C HTML Validator (Nu Html Checker)](https://validator.w3.org/) | All templates, checked via live URLs and view-source for login-required pages | ✅ No errors found (see bugs 28–31 for accessibility warnings caught and fixed along the way) |
| [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) | `style.css` | ✅ No errors found |
| [JSHint](https://jshint.com/) | `scene.js`, `cat_form.js` (ES version set to ESNext) | ✅ No errors found — default ES5 warnings cleared by setting the correct ES version; one real `undefined variable: bootstrap` warning resolved with a `/* global bootstrap */` annotation |
| [CI Python Linter](https://pep8ci.herokuapp.com) | `models.py`, `views.py`, `admin.py`, `apps.py`, `urls.py`, `tests.py`, `cloudinary_extras.py` (both apps), `settings.py`, `config/urls.py` | ✅ No errors found see bugs 38–39 |
| Python `manage.py test` | Model and view unit tests (`cats/tests.py`) | ✅ 42/42 passing |
| Lighthouse | Homepage, login, signup, gallery, my-cats, create-cat (Desktop + Mobile) | ✅ Desktop: Performance 97–100, Accessibility 90–95, Best Practices 100, SEO 91. Mobile (final, after optimization): Homepage 85, Gallery 98, My Cats 97, Create a Cat 97, Accessibility 92–95, Best Practices 100, SEO 91 see bugs 35–37 |

### How the test suite (`cats/tests.py`) works

41 automated tests, split into model tests and view tests, run with:
```
python3 manage.py test cats
```

**Model tests** cover each model's defaults, `__str__` output, ordering
(`Cat` newest-first vs `Comment` oldest-first), and both `unique_together`
constraints (`Reaction`, `DailyPet`) — confirming a duplicate reaction or a
second same-day pet actually raises `IntegrityError` rather than silently
allowing it.

**View tests** cover, per view:
- **Permissions** Every write action requires login; only a cat's owner
  can update/delete it or toggle its visibility (non-owners get `403`, and
  a non-owner hitting another user's toggle-visibility URL gets `404`
  rather than silently succeeding)
- **Context data** `SceneView` only shows public cats, correctly
  identifies `cat_of_the_day`, and (for logged-in users) populates
  `reacted_cat_ids`/`petted_cat_ids` so the popup reflects real state on
  first page load
- **AJAX endpoints** `toggle_reaction` and `pet_cat` are tested both as
  AJAX calls (checking the returned JSON) and as plain POST requests
  (checking the redirect), including that petting the same cat twice in
  one day doesn't create a second `DailyPet` row
- **Pagination ordering** A regression test creates more cats than fit
  on one page and asserts they appear in a deterministic newest-first
  order (this test was added specifically to catch bug 28 below)

**Storage handling:** the project's default file storage is Cloudinary
(see `settings.STORAGES`). Every test that creates a `Cat` runs under
`@override_settings`, pointing storage at a temporary local folder
instead, so running the test suite never makes a real upload to
Cloudinary or depends on production credentials being set locally.
Uploaded images in tests are tiny real PNGs generated in memory with
Pillow, so Django's `ImageField` validation genuinely passes rather than
being faked.

### Manual test checklist (already verified)

- [x] Register, log in, log out
- [x] Create a cat (public and private)
- [x] Cannot submit a cat with a blank canvas
- [x] Edit a cat without being forced to redraw
- [x] Edit preserves existing artwork and coat color selection
- [x] Delete a cat (from My Cats and from the manor popup)
- [x] Toggle public/private with one click
- [x] Favorite toggles correctly and persists across popup reopen
- [x] Pet works once per day, persists correctly across popup reopen
- [x] Cat of the Day updates correctly, resets daily, and shows no spotlight on a genuine tie
- [x] Comment CRUD, with ownership-only edit/delete
- [x] Only the cat's owner sees edit/delete controls in the popup
- [x] 404 and 500 pages render correctly in production
- [x] Responsive on mobile (including narrow phones), tablet, and desktop

---

## Bugs Found & Fixed

Documented in detail, in the spirit of showing genuine problem-solving
rather than a suspiciously clean project history.

| # | Bug | Cause | Fix |
|---|---|---|---|
| 1 | Cat form required two submit clicks to save | Assigning the canvas blob to a hidden file input via `DataTransfer`, then calling `form.submit()`, is unreliable across browsers | Rewrote submission to use `fetch()` with the blob attached directly to `FormData` |
| 2 | Page crashed with `SyntaxError: Identifier 'canvas' has already been declared` | Error-handling code tried to inject the server's re-rendered HTML via `document.write()`, but the live page's own script already had `const canvas` declared in the same scope | Removed `document.write()` entirely; errors are now read safely via `DOMParser`, which never executes scripts |
| 3 | Creating a cat silently failed with a generic, unhelpful message | The error box only rendered messages for `name`/`personality`; failures on `coat_color` or `drawing_image` had nowhere to display | Added explicit error rendering for every form field, not just two of them |
| 4 | `Select a valid choice. 'dusty_rose' is not one of the available choices` | The model's `COAT_COLOR_CHOICES` was renamed to match a new theme, but the template's swatch `data-value` attributes were never updated to match | Synced the template's swatch values to the model's actual current choices |
| 5 | Two color swatches were visually identical / near-identical | Two colors accidentally shared the same hex value during a palette update | Replaced with 8 genuinely distinct hues |
| 6 | Editing a cat started with a blank canvas, risking overwriting the original artwork, or failing validation entirely | The edit form never loaded the cat's existing image onto the canvas | Preload the existing drawing via a cross-origin `<img>` + `drawImage()` before the user interacts with the canvas |
| 7 | Drawing was offset from the cursor on mobile after making the canvas responsive | Pointer coordinates were read in CSS pixels but the canvas's internal resolution stayed fixed at 400×400, with no scale correction | Added a scale factor (`canvas.width / rect.width`) to the pointer-position calculation |
| 8 | Cats disappeared entirely (not just squeezed) once more than ~7 were in the manor on mobile | Fixed-size sprites inside a container with `overflow: hidden` caused any cats that didn't fit to be clipped rather than reflowed | Made the cat row horizontally scrollable as a safety net regardless of screen width or cat count |
| 9 | The 👑 Cat of the Day crown got clipped after the above fix | Setting `overflow-x: auto` implicitly links `overflow-y`, clipping the crown's negative vertical offset | Added top padding to the row and repositioned the crown to sit within it instead of poking above it |
| 10 | Cat drawings appeared cropped (usually missing the top) in Gallery/My Cats thumbnails | A fixed-height thumbnail box forced `object-fit: cover` to crop a square image into a non-square shape | Changed thumbnails to `aspect-ratio: 1/1` with `object-fit: contain`, guaranteeing the whole drawing is always visible and centered |
| 11 | The "Pet today" button stayed clickable after being pressed until the page was refreshed | The button was only disabled *after* the server responded, so rapid or repeated clicks (or reopening the same cat's popup) could fire again before that update landed | Disable immediately on click, and persist the "already petted" state onto the cat's own DOM element so reopening its popup reflects reality without a refresh |
| 12 | The Favorite (🐾) count reset to 0 when reopening the same cat's popup | The count was only ever read from a page-load snapshot, never updated after a successful AJAX toggle | Persist the live count and reacted state onto the DOM element after each toggle, and pass real `reacted_cat_ids` from the view on page load |
| 13 | Modal footer buttons wrapped awkwardly, with one floating alone on its own line | No consistent flex-wrap/centering rule on the modal footer | Added explicit `flex-wrap`, `justify-content: center`, and shortened button labels so all buttons share one row cleanly at any width |
| 14 | "Back to the manor" button appeared left-aligned instead of centered | `.icon-btn` is `display: flex` (block-level), so a parent `text-align: center` had no effect on it | Wrapped the link in a centered container and set the link itself to `display: inline-flex` |
| 15 | Several pages broke or looked squeezed on mobile phones | Templates used `col-md-*`/`col-lg-*` without a base `col-*` class, so Bootstrap applied no width rule at all below the `md` breakpoint | Added base `col-12`/`col-6` classes so every column has a defined width on small screens |
| 16 | "Small" buttons (`.btn-sm`) rendered at full size | A global `.btn` rule set padding/font-size that, due to equal CSS specificity and load order, overrode Bootstrap's smaller `.btn-sm` variant | Added an explicit `.btn-sm` override |
| 17 | The "Personality" label appeared near the bottom of its textarea instead of above it | Neither the label nor the textarea had `display: block`, so both sat on the same inline-level line box and were baseline-aligned | Added `display: block` to `.form-label` |
| 18 | The drawing canvas stayed locked near 400px wide even on tablet/desktop | Only `max-width: 100%` was set (which caps size but doesn't grow it) | Added an explicit `width: 100%` so the canvas actually fills wider containers |
| 19 | Production crashed with `TemplateSyntaxError: 'static' takes at least one argument` | An explanatory code comment literally contained the text `{% static %}`, and Django's template engine scans for `{% %}` tags everywhere in a file including inside comments | Rewrote the comment to describe the tag in words instead of using its literal syntax |
| 20 | Every click handler on the scene page silently stopped working | A duplicate `<script>` tag was accidentally left in the template, breaking the whole script block | Removed the duplicate tag |
| 21 | Production showed `OperationalError: no such table: cats_cat` | Heroku's Postgres add-on was never attached, so the app fell back to an empty, ephemeral SQLite database; migrations had also never been run remotely | Attached `heroku-postgresql`, then ran `migrate` against the production database |
| 22 | `DEBUG` was temporarily hardcoded to `True` in production during a debugging session | Manually set while diagnosing an issue and not reverted immediately | Reverted to reading from the `DEBUG` environment variable  `DEBUG = os.environ.get('DEBUG', 'False') == 'True'` so it's driven entirely by Heroku config vars and never needs manual toggling on future deploys |
| 23 | A temporary `/test-error/` route (used to verify the custom 500 page) was still live after testing | Forgotten cleanup step | Removed the route and its view before final submission |
| 24 | The entire `venv/` folder and `db.sqlite3` were committed to GitHub | `.gitignore` didn't exist yet at the time of the first commit | Added `.gitignore`, then used `git rm -r --cached` to untrack them without deleting local files |
| 25 | The site background/favicon returned 404 in production | An uploaded image kept its original extension (e.g. `.jpeg`) while the template referenced a different one (e.g. `.png`) | Renamed the file to match exactly what the template requested |
| 26 | Browser console showed a Bootstrap `aria-hidden` accessibility warning on every modal close | Bootstrap applies `aria-hidden="true"` to the modal before moving focus away from whatever element (usually the close button) still had it | Explicitly blur the focused element on the modal's `hide.bs.modal` event, before Bootstrap applies `aria-hidden` |
| 27 | Cats could be saved with a completely blank canvas | No validation existed, client or server side, requiring an actual drawing | Added client-side tracking of whether a real stroke has been made, with a clear on-page warning blocking submission until something is drawn |
| 28 | `UnorderedObjectListWarning` on the homepage; cats could theoretically shift between pages or be skipped/duplicated across page loads | `SceneView`'s queryset uses `.annotate()`, which doesn't reliably preserve the `Cat` model's default `Meta.ordering`, leaving `Paginator` working against an effectively unordered queryset | Added an explicit `.order_by('-created_on')` after the `.annotate()` call; covered by a regression test that creates more cats than one page holds and asserts deterministic ordering |
| 29 | `scene.html` would fail to render at all (`TemplateSyntaxError: Unclosed tag`) | A `{% if user.is_authenticated %}...{% else %}...{% endif %}` block in the modal footer was missing its `{% endif %}` | Added the missing `{% endif %}` |
| 30 | W3C HTML Validator: "Empty heading" warning on `<h5 id="catModalName"></h5>` | The modal's title heading starts empty in the server-rendered HTML and is only filled in by JavaScript after a cat is clicked, which validators flag as empty content | Gave the element placeholder text ("Cat details"); later changed the element itself (see bug 32) |
| 31 | W3C HTML Validator: "This document has heading elements but none of them has a computed heading level of 1" | The scene page had no `<h1>` at all | Added a visually-hidden `<h1>` at the top of the content block using Bootstrap's `visually-hidden` utility class, so it's available to screen readers/SEO without changing the visual design |
| 32 | W3C HTML Validator: "The heading `h5`... follows the heading `h1`..., skipping 3 heading levels" | Adding the `<h1>` (bug 31) meant the modal's `<h5>` title now jumped straight from level 1 to level 5 in the page's heading outline | Changed the modal title from `<h5>` to `<p>`, since Bootstrap's `modal-title` is a CSS class, not a required heading tag by removing it from the heading outline entirely rather than trying to patch the levels |
| 33 | W3C HTML Validator: "The `aria-labelledby` attribute must not be specified on any `div` element unless the element has a `role` value other than..." | Adding `aria-labelledby="catModalName"` to the modal `<div>` (to properly associate its accessible name after bug 32) isn't valid on a `div`, which has an implicit ARIA role of `generic` | Added `role="dialog"` to the modal `<div>`, which is what Bootstrap's own accessibility docs recommend for modals anyway, making `aria-labelledby` valid and giving assistive tech proper context that the element is a dialog |
| 34 | Petting every cat once with a single account crowned a random cat as "Cat of the Day," and that winner changed on every page refresh | `cat_of_the_day` was chosen with `order_by('-today_pet_count', '?')` a random tie-break re-rolled on every request, so a genuine tie never produced a stable (or meaningful) winner | Replaced with a `get_cat_of_the_day()` helper that only crowns a cat when it has *strictly* more pets than the runner-up; ties now correctly show no spotlight banner instead of a flickering random pick |
| 35 | Chrome DevTools Lighthouse (Accessibility, `/cat/new/`): "No label associated with a form field" on the Name and Personality inputs | The `<label>` elements had no `for` attribute pointing at the corresponding input's `id`, so screen readers couldn't announce which label describes which field | Added `for="{{ form.name.id_for_label }}"` / `for="{{ form.personality.id_for_label }}"` to properly associate each label with its Django-generated input `id` |
| 36 | Console warning on every page except the homepage: "resource was preloaded using link preload but not used within a few seconds" | `base.html` unconditionally preloaded the manor scene background image in every page's `<head>`, but that image is only actually used on the homepage. Every other page (Gallery, My Cats, Create a Cat, login, signup) downloaded it early and never used it, wasting bandwidth on mobile especially | Removed the universal preload from `base.html`; `scene.html` already has its own scoped copy in its `extra_css` block for the one page that actually needs it |
| 37 | Lighthouse mobile Performance scores of 74–87 across several pages, with "Render-blocking requests" (1,500–2,600ms estimated savings) and "Improve image delivery" flagged on every page | Bootstrap CSS and Google Fonts were loaded as standard blocking `<link rel="stylesheet">` tags from external CDNs, delaying first paint until both downloaded; cat drawing images were served at their original Cloudinary format/quality with no automatic optimization | Added `rel="preconnect"` hints plus the preload+swap pattern for both external stylesheets in `base.html` (render-blocking savings dropped to ~150ms on the homepage); added a `cld_optimize` template filter applying Cloudinary's `f_auto,q_auto` transformation to every cat image across `scene.html`, `gallery.html`, `my_cats.html`, `cat_detail.html`, and `cat_form.html`. Mobile Performance rose from 74→85 (homepage), 87→98 (gallery), 81→97 (my cats) |
| 38 | Code Institute's PEP8 Python Linter flagged dozens of `E501 line too long` and `W292 no newline at end of file` issues across nearly every Python file | The project's own flake8 config used a relaxed 99-character line limit, but the official CI linter enforces strict 79-character PEP8; several files also lost their trailing newline during earlier edits | Wrapped every flagged line across `models.py`, `views.py`, `urls.py`, `tests.py`, and `settings.py` using Django's standard multi-line argument style; added trailing newlines throughout; added a project-level `.flake8` config so local checks catch the same issues going forward |
| 39 | `cats/apps.py` had its class body completely unindented (`default_auto_field` and `name` at column 0 instead of indented under the class) | A terminal heredoc command used to patch the file lost its leading whitespace when copy-pasted, silently producing invalid Python | Since `AppConfig` subclasses are loaded via `INSTALLED_APPS` at Django startup, this would have crashed the entire application on next deploy caught and fixed by rewriting the file directly in the editor and verifying indentation with `cat -e` |
| 40 | The Cat of the Day crown and spotlight banner didn't update after petting a cat, even when that pet changed who was winning only a manual page refresh showed the correct state | `cat_of_the_day` is computed server-side once per page load; the AJAX pet request updates the database but never re-renders that part of the page | After a successful pet, the page now reloads automatically (with a short delay so the 💗 float animation is still visible first), guaranteeing the crown and banner always reflect the latest state |
| 36 | Console warning on every page except the homepage: "resource was preloaded using link preload but not used within a few seconds" | `base.html` unconditionally preloaded the manor scene background image in every page's `<head>`, but that image is only actually used on the homepage — every other page (Gallery, My Cats, Create a Cat, login, signup) downloaded it early and never used it, wasting bandwidth on mobile especially | Removed the universal preload from `base.html`; `scene.html` already has its own scoped copy in its `extra_css` block for the one page that actually needs it |

---

## Deployment

This project is deployed on Heroku, running on the **Heroku-24 stack**
(deliberately not upgraded to Heroku-26 the newer stack offers no
functional benefit here, and upgrading close to submission would add
unnecessary risk for no benefit; this refers to Heroku's underlying
OS/runtime image, not the Django version, which runs identically on either).

### To deploy your own version

1. Create a Heroku app: `heroku create your-app-name`
2. Attach Postgres: `heroku addons:create heroku-postgresql:essential-0`
3. Set config vars:
   ```
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name
   heroku config:set CLOUDINARY_API_KEY=your-api-key
   heroku config:set CLOUDINARY_API_SECRET=your-api-secret
   ```
4. Push and deploy: `git push heroku main`
5. Run migrations: `heroku run python manage.py migrate`
6. Create a superuser: `heroku run python manage.py createsuperuser`

Full step-by-step local setup (from an empty folder to a running server) is
documented in [SETUP.md](SETUP.md).

---

## Credits

- This project was built as a Milestone 3 submission for the
  [Code Institute](https://codeinstitute.net/) Full Stack Software
  Development diploma.
- General coding patterns and problem-solving approaches were informed by
  Code Institute's course material and walkthrough projects, official
  Django and Bootstrap documentation, MDN Web Docs, W3Schools, and
  Stack Overflow discussions encountered while debugging.
- Where a specific, named technique was adapted directly from a
  source (rather than general knowledge), it's credited inline via a
  comment above the code, for example, the CSS preload+swap pattern
  in `base.html` cites web.dev's "Defer non-critical CSS" guide.
- Images (logo and background illustrations) were compressed using
  [TinyPNG](https://tinypng.com/).
- Python code checked for PEP8 compliance using Code Institute's
  [PEP8 Python Linter](https://pep8ci.herokuapp.com/).
- Background illustrations and logo: original artwork created by Monica Feis for this
  project.
- Design and development: Monica Feis.
