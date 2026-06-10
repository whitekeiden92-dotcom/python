# Task Manager

A simple Python task management system with both a command-line interface and a web UI.

## Run CLI

```bash
python main.py
```

## Run Web Interface

Install dependencies:

```bash
pip install -r requirements.txt
```

Then start the app:

```bash
python main.py web
```

Open the app in your browser at:

```text
http://127.0.0.1:5000
```

> Important: do not open `templates/index.html` directly from the file system or from another dev server port. The web interface must be served by Flask on the same origin.
