# Text-Based Browser Game (FastAPI)

**⚠️ Work in progress.** This is a pet project under active development. The game is not yet fully playable — mechanics are being implemented gradually.

A small text-based browser game with D&D mechanics built with **FastAPI**, SQLAlchemy, and Alembic.

## Requirements
- Python 3.12+
- pip (or pip3)

## Installation

1. **Download the project** as a ZIP archive from GitHub and extract it to any folder.

2. **Open a terminal** inside the extracted folder.

3. **Create a virtual environment**:
```
   python -m venv .venv
```

4. **Activate the virtual environment**:
   # On Windows:
```
   .venv\Scripts\activate
```
   # On Unix/MacOS:
```
   source .venv/bin/activate
```

5. **Install dependencies**:
```
   pip install -r requirements.txt
```

6. **Set up the database**:
```
   alembic upgrade head
```

## Running the Game

The game is ready to launch. Start the server with:
```
   python main.py
```
Then open `http://127.0.0.1:8000` in your browser.
