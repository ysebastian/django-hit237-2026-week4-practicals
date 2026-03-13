# django-hit237-2026-week4-practicals

## Project Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run database migrations

```bash
cd libraryhub
python manage.py migrate
```

### 4. Start the development server

```bash
python manage.py runserver
```

Open your browser at http://127.0.0.1:8000/