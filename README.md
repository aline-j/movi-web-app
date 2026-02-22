# 🎬 MovieApp

MovieApp is a simple Flask web application for managing users and their favorite movies.  
Movie data is automatically fetched from the **OMDb API**.  
The application supports full **CRUD functionality**, **flash messages** for user feedback, and uses an **SQLite database** for persistence.

---

## 🚀 Features

- 👤 Create and view users
- 🎞️ Add movies to a user (via OMDb API)
- ✏️ Update movie titles
- 🗑️ Delete movies
- 🔔 Flash messages for success, warning, and error feedback
- 💾 Persistent storage using SQLite
- 🎨 Simple UI with HTML, Jinja2, and CSS

---

## 🛠️ Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- OMDb API
- HTML / Jinja2
- CSS

---

## Setup

⚠️ **IMPORTANT:** Before starting, the following environment variables must be set:
- `OMDB_API_KEY`
- `FLASH_KEY`

### 1. Obtain your OMDb API key

• Go to omdbapi.com
• Register for free and receive your API key
• Max. 1,000 requests/day (free)

### 2. Clone repository

```bash
git clone <repo-url>
cd movi-web-app
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set OMDb API Key as Environment Variable

Using a .env file (recommended):

1. Install python-dotenv: `pip install python-dotenv`

2. Create a .env file in the project folder:
   OMDB_API_KEY=your_omdb_api_key_here
   FLASH_KEY=your_secret_key_here

### 5. Start application

```bash
python app.py
```

