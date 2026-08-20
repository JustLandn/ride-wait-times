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

## Secrets

The ntfy topic URL is read from Streamlit secrets, not hardcoded. Copy the
example file and fill in your own topic:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

On Streamlit Community Cloud, set `NTFY_TOPIC_URL` under the app's
**Settings → Secrets** instead of committing a secrets.toml file.
