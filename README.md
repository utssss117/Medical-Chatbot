# Medical-Chatbot

A small Flask-based medical chatbot prototype that helps demonstrate conversational retrieval and prompt-driven responses over a local dataset. This repository contains the application code, basic templates, and helper modules used for development and experimentation.

## Features
- Simple web UI served from `app.py` and `templates/chat.html`.
- Helper modules in `src/` for prompt composition and processing.
- Data storage in the `data/` directory for local datasets and examples.

## Prerequisites
- Python 3.10+ (or a compatible 3.x environment)
- Recommended: conda or virtualenv to isolate dependencies

## Setup (recommended)
Open PowerShell and run:

```powershell
conda create -n medibot python=3.10 -y; conda activate medibot
pip install -r requirements.txt
```

If you don't use conda, create a virtual environment and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the app
From the repository root run:

```powershell
conda activate medibot
python app.py
```

Then open your browser at `http://127.0.0.1:5000/` (or the address printed by the app).

## Project Structure
- `app.py` — Flask application entrypoint and HTTP routes.
- `src/` — Python helper modules (`helper.py`, `prompt.py`) used by the app.
- `data/` — Local dataset files used by the prototype.
- `templates/` — HTML templates (`chat.html`) for the UI.
- `static/` — Static assets like `style.css`.
- `requirements.txt` — Python dependencies.
- `LICENSE` — Project license file.

## Notes & Troubleshooting
- If `python app.py` exits with an error, check the console traceback for missing packages and ensure the active environment has `pip install -r requirements.txt` run.
- The app expects any required keys or external service configs to be set as environment variables or defined in a local config if used. Search for references in `app.py` or `src/` when integrating external APIs.

## Contributing
- Fork the repo, create a branch for your feature, and open a pull request.
- Keep changes minimal and aligned with existing project style.

## License
This project includes a `LICENSE` file in the repository root.

---
If you'd like, I can also:
- Add a short `README` badge header (build/state) or
- Extend the Usage section with example chat transcripts or CLI options.
