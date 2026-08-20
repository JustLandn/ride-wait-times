# ride-wait-times

## Virtual environment

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Deactivate when done:

```bash
deactivate
```

## Notifications

Each visitor enters their own ntfy topic in the app's text field, kept only
in their browser session — no shared config needed. Leave it blank to skip
push alerts and just see the in-app toast.
