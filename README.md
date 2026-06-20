pi# Paseka-Seleke eLearning Portfolio

A modern, professional website for eLearning, instructional design, LMS, virtual
training, and AI learning services. Built to run and grow inside PyCharm
Community Edition with free tools only.

The signature feature: visitors can step into a short sample course and answer a
knowledge check that is **scored by the backend** (FastAPI), not the browser.
This is the interactive foundation you can reuse for any mock learner experience.

## Tech stack (all free)

- **FastAPI + Uvicorn** : Python web backend and server
- **Jinja2** : server rendered HTML templates
- **HTMX + Alpine.js** : interactivity without a separate frontend build (self-hosted, in app/static/js/vendor/)
- **Tailwind CSS** : precompiled to app/static/css/tailwind.css for speed. After
  adding new utility classes to a template, run `python build_tailwind.py`
  once to refresh it (downloads the standalone CLI on first run, no Node needed)
- **SQLite + SQLModel** : file based database, no server to install


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


