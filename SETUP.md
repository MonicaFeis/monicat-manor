# 🛠️ SETUP.md Running MoniCat Manor Locally

This guide takes you from an empty folder to a fully working local copy of
MoniCat Manor. It assumes basic familiarity with the terminal and Git.

---

## Prerequisites

- **Python 3.9+**
- **pip**
- **Git**
- A free **[Cloudinary](https://cloudinary.com/)** account. The project
  uses Cloudinary for image storage in *every* environment (including
  local development), so this is required, not optional. Sign up and
  grab your Cloud Name, API Key, and API Secret from your Cloudinary
  dashboard.

You do **not** need PostgreSQL installed locally without a `DATABASE_URL`
environment variable set, the project automatically falls back to a local
SQLite database file.

---

## 1. Clone the repository

```
git clone https://github.com/MonicaFeis/monicat-manor.git
cd monicat-manor
```

## 2. Create and activate a virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

On Windows (Command Prompt):
```
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal prompt once it's active.

## 3. Install dependencies

```
pip install -r requirements.txt
```

## 4. Set up environment variables

Create a file called `.env` in the project root (same folder as
`manage.py`) with the following:

```
SECRET_KEY=your-own-random-secret-key
DEBUG=True
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

| Variable | Required? | Notes |
|---|---|---|
| `SECRET_KEY` | Recommended | Any long random string works for local dev. Never reuse a production key. |
| `DEBUG` | Recommended | Set to `True` locally so you get full error pages instead of the custom 500 page. |
| `CLOUDINARY_CLOUD_NAME` | **Required** | From your Cloudinary dashboard. |
| `CLOUDINARY_API_KEY` | **Required** | From your Cloudinary dashboard. |
| `CLOUDINARY_API_SECRET` | **Required** | From your Cloudinary dashboard. Treat this like a password. Never commit it. |
| `DATABASE_URL` | Optional | Only needed if you want to connect to a real PostgreSQL database instead of the local SQLite fallback. |

`.env` is already listed in `.gitignore`  never commit it.

## 5. Run migrations

```
python3 manage.py migrate
```

## 6. Create a superuser (for Django admin access)

```
python3 manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

## 7. Run the development server

```
python3 manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser. The Django admin is at
**http://127.0.0.1:8000/admin/**, using the superuser credentials from
step 6.

---

## Running the test suite

```
python3 manage.py test cats
```

This runs the full automated test suite (model and view tests). Test runs
use a temporary local file storage override, so they never upload images
to your real Cloudinary account.

---

## Troubleshooting

**`OperationalError: no such table`**
Migrations haven't been applied yet. Run `python3 manage.py migrate`.

**Images fail to upload / `drawing_image` errors on save**
Double-check your three `CLOUDINARY_*` variables in `.env` a typo or
missing value is the most common cause.

**`ModuleNotFoundError` for a package that should be installed**
Confirm your virtual environment is active (you should see `(venv)` in
your prompt) and re-run `pip install -r requirements.txt`.

**Styles look broken / missing**
Run `python3 manage.py collectstatic` if you're testing with `DEBUG=False`
locally with `DEBUG=True`, Django serves static files automatically and
this step isn't needed.

---

## Deploying your own version

See the [Deployment](README.md#deployment) section of the main README for
Heroku-specific setup and config vars.