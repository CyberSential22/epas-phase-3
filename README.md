# Automated Event Planner and Approval System - Phase 3

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue?logo=postgresql&logoColor=white)
![Git](https://img.shields.io/badge/Git-Latest-orange?logo=git&logoColor=white)
![AI-Assisted](https://img.shields.io/badge/AI--Assisted-Gemini-brightgreen)

## 📝 Executive Summary
The **Automated Event Planner and Approval System (EPAS)** is designed to digitize the institutional workflows at JNU Jaipur. It replaces traditional paper-based approval processes with a transparent, efficient digital system (as per Section 3.2).

**Phase 3** of this project specifically introduces **Secure Authentication and Role-Based Access Control (RBAC)**, ensuring that only authorized users can create, review, and approve events based on their institutional roles.

## 🚀 Phase 3 Scope
This repository contains the "Authentication and RBAC Module", which includes:
- **User Registration & Life Cycle**: Integrated with JNU Jaipur department logic.
- **Secure Login/Logout**: Session-based authentication using **Flask-Login**.
- **Password Hashing**: Secure storage using **Werkzeug's** PBKDF2 hashing.
- **Role-Based Access Control (RBAC)**: Custom decorators (`@student_required`, `@faculty_required`, etc.) to enforce permissions.
- **Enhanced Database Schema**: Inclusion of the `User` and `AuditLog` models for tracking institutional actions and security events.

## 🛠️ Tech Stack
- **Backend**: Python 3.8+, Flask 2.x
- **Frontend**: Jinja2 Templates, HTML5, CSS3, JavaScript
- **Database Architecture**: PostgreSQL (via Supabase)
- **Deployment**: Render (Backend), Vercel (Frontend Proxy)
- **ORM**: SQLAlchemy

## 💻 Installation Guide

### Prerequisites
- Python 3.8 or higher
- Git

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/CyberSential22/epas-phase-3.git
   cd epas-phase-3
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Create a `.env` file in the root directory (do not commit this):
   ```env
   SECRET_KEY=your_secure_random_key
   DATABASE_URL=postgresql://user:pass@host:port/dbname
   FLASK_ENV=development
   ```

5. **Run Locally**:
   ```bash
   python run.py
   ```

## 📂 Project Structure
```text
epas-phase-3/
├── app/
│   ├── blueprints/      # Authentication & Event Routes
│   ├── forms/           # WTForms for Login & Registration
│   ├── models/          # User, Event, and AuditLog Models
│   ├── static/          # CSS, JS, and Images
│   ├── templates/       # HTML Jinja2 Templates
│   ├── utils/           # IP Logging & Custom Decorators
│   └── __init__.py      # App Factory & Middleware Integration
├── instance/            # Local Database (SQLite)
├── migrations/          # Database Migration Scripts
├── requirements.txt     # Project Dependencies
├── run.py               # Entry Point
└── vercel.json          # Deployment Proxy Config
```

## 🌐 Deployment Overview
- **Target Architecture**:
  - **Frontend Proxy**: Vercel (for high availability and CDN).
  - **Backend Host**: Render (hosting the Flask application).
  - **Database**: Supabase (PostgreSQL managed instance).

## 🤝 Acknowledgments
- **Project Team**: Kashif Shaikh, Aditya Gond, Yaduvansh Singh Ranawat (JNU Jaipur).
- **Project Guide**: Ms. Saumya.
- **Ethical AI Usage**: In accordance with Section 6.5, AI-assisted tools were utilized for research and debugging, while the core design and institutional logic remain the original work of the students.

## ⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.
