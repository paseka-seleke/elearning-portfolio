pi# Paseka eLearning Website

A modern, professional website for eLearning, instructional design, LMS, virtual
training, and AI learning services. Built to run and grow inside PyCharm
Community Edition with free tools only.

The signature feature: visitors can step into a short sample course and answer a
knowledge check that is **scored by the backend** (FastAPI), not the browser.
This is the interactive foundation you can reuse for any mock learner experience.

## Tech stack (all free)

- **FastAPI + Uvicorn** : Python web backend and server
- **Jinja2** : server rendered HTML templates
- **HTMX + Alpine.js** : interactivity without a separate frontend build
- **Tailwind CSS (Play CDN)** : styling with zero build step
- **SQLite + SQLModel** : file based database, no server to install

## Run it in PyCharm Community

1. Open this folder in PyCharm (File, Open, select the `paseka` folder).
2. Create a virtual environment when PyCharm offers, or:
   - PyCharm: Settings, Project, Python Interpreter, Add, Virtualenv.
3. Install dependencies. In the PyCharm terminal:
   ```
   pip install -r requirements.txt
   ```
4. Run `run.py` (right click, Run 'run'), or in the terminal:
   ```
   uvicorn app.main:app --reload
   ```
5. Open http://127.0.0.1:8000

The database `paseka.db` is created and seeded automatically on first run.

## Project structure

```
paseka/
  run.py                  press Run in PyCharm to start
  requirements.txt
  paseka.db               created on first run (SQLite)
  app/
    main.py               FastAPI routes (pages + quiz scoring + contact)
    database.py           SQLite engine and session
    models.py             tables: SampleCourse, QuizQuestion, BlogPost, Lead
    seed.py               sample courses, quiz questions, blog posts
    data/content.py       all static copy: CV, services, frameworks, navigation
    templates/            Jinja2 HTML (base, pages, components, partials)
    static/               css and js
```

## Where to edit things

- **Your CV and contact details**: `app/data/content.py` (the `CV` and `SITE` blocks).
  Items written as `[Insert ...]` are placeholders to fill in.
- **Service page copy**: `app/data/content.py` (`SERVICE_PAGES`).
- **Sample courses and quiz questions**: `app/seed.py`. After editing, delete
  `paseka.db` and restart so it reseeds, or add records through code.
- **Blog posts**: `app/seed.py` (`BLOG_POSTS`).
- **Design tokens (colours, fonts)**: the Tailwind config block in
  `app/templates/base.html`.

## How the interactivity works

1. A visitor opens a sample course at `/samples/<slug>`.
2. Each knowledge check option is a button that HTMX posts to
   `/samples/<slug>/answer/<question_id>` with the chosen option.
3. FastAPI checks the answer against the database and returns a small HTML
   fragment showing the result and explanation. The answer key never reaches the
   browser early.
4. Alpine.js updates the progress bar and final score on the page.

Contact form submissions are saved to the `Lead` table in SQLite, so you have a
record of every enquiry.

## Going to production (still free or very cheap)

- Replace the Tailwind Play CDN with the free standalone Tailwind CLI to ship a
  single compiled CSS file (better performance, no external script).
- Deploy to a free tier: Render, Railway, Fly.io, or PythonAnywhere all run a
  FastAPI app. Use `uvicorn app.main:app` as the start command.
- For email on contact submissions, add a free SMTP service later. For now,
  enquiries are stored safely in the database.

## A note on the name

The brief and this build use **Paseka** throughout. If your profile uses a
different spelling, update `SITE["name"]` in `app/data/content.py` and the
heading in `app/templates/about.html`.
