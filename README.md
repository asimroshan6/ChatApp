# 💬 ChatApp: Anonymous Real-Time Chat with AI

A modern, fast, and secure anonymous chat application built with **FastAPI**, **WebSockets**, and **SQLAlchemy**. This app allows users to create or join temporary rooms and interact with an integrated AI assistant.

---

## 🌟 Features

* **Real-time Messaging:** Low-latency communication powered by WebSockets
* **Anonymous Rooms:** Create or join rooms with a password. No permanent accounts required
* **AI Assistant:** Mention `/ai` in your message to get instant responses from a Groq-powered AI model
* **Message History:** Automatic retrieval of past messages when joining a room
* **Live Presence:** Real-time tracking of online users within a room
* **Self-Cleaning:** Automated cleanup of messages, users, and rooms once the last person disconnects
* **Secure:** Password hashing using `bcrypt` and session security via JWT (JSON Web Tokens)

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** SQLAlchemy (ORM) with SQLite (default)
* **Frontend:** Jinja2 Templates, Bootstrap 5, Vanilla JavaScript
* **Real-time:** WebSockets
* **AI:** Groq API (OpenAI-compatible client)
* **Security:** Passlib (bcrypt) & Python-jose (JWT)

---

## 📁 Project Structure

```text
ChatApp/
├── core/               # App configuration and environment settings
├── database/           # Models, session management, and DB connection
├── routers/            # API endpoints (WebSockets and HTTP)
├── services/           # Business logic (Auth, AI, Message Storage)
├── static/             # CSS and JavaScript files
├── templates/          # HTML files (Jinja2)
└── .env                # Environment variables (API keys, Secret keys)
```

---

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.9+
* A Groq API Key (Get one at [https://console.groq.com](https://console.groq.com))

---

### 2. Installation

1. Clone the repository:

```bash
git clone https://github.com/asimroshan6/ChatApp.git
cd ChatApp
```

1. Create a virtual environment and activate it:

```bash
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

1. Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy pydantic-settings python-jose passlib[bcrypt] openai
```

---

### 3. Environment Setup

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./chat.db
SECRET_KEY=your_super_secret_jwt_key
GROQ_API_KEY=your_groq_api_key_here
```

---

### 4. Running the App

```bash
uvicorn main:app --reload
```

> ⚠️ Ensure your `main.py` includes the routers you defined

Visit: [http://localhost:8000](http://localhost:8000)

---

## 🤖 Using the AI Assistant

In any chat room, simply type `/ai` followed by your question:

```text
You: /ai What is the capital of France?

🤖 AI: The capital of France is Paris.
```

---

## 🔒 Security & Data Policy

* **Passwords:** All room passwords are encrypted using `bcrypt` before storage
* **Session:** Users are authenticated via JWT tokens stored in the browser's `localStorage`
* **Volatility:** To maintain anonymity and save resources, room data (messages and users) is deleted from the database once the last user leaves the WebSocket session

---

## 🤝 Contributing

Contributions are welcome! Whether it's styling, bug fixes, or new features, feel free to fork and submit a PR.

---

## 👨‍💻 Author

### Developed by Asim Roshan
