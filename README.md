# Job Application Tracker

A full-stack web application for tracking job applications, built with **MySQL**, **Python/Flask**, and **HTML/CSS**.

This application lets you manage companies, job listings, applications, and professional contacts all in one place. It also includes a **Job Match** feature that compares your skills against job requirements and ranks positions by match percentage.

---

## Features

- **Dashboard** — Overview of your job search with stats and recent activity
- **Companies** — Full CRUD (Create, Read, Update, Delete) for companies you're targeting
- **Jobs** — Track job listings with titles, salary ranges, and required skills (stored as JSON)
- **Applications** — Log every application with status tracking (Applied → Screening → Interview → Offer/Rejected/Withdrawn)
- **Contacts** — Keep track of recruiters, hiring managers, and professional connections
- **Job Match** — Enter your skills and instantly see which jobs match, ranked by percentage

---

## Tech Stack

| Layer      | Technology                      |
|------------|---------------------------------|
| Database   | MySQL 8.0+                      |
| Backend    | Python 3.x, Flask               |
| Frontend   | HTML5, CSS3                     |
| Connector  | mysql-connector-python          |

---

## Setup Instructions

### 1. Prerequisites

Make sure you have installed:

- **Python 3.8+** — [Download](https://www.python.org/downloads/)
- **MySQL 8.0+** — [Download](https://dev.mysql.com/downloads/mysql/)
- **Git** — [Download](https://git-scm.com/downloads)

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/job-tracker.git
cd job-tracker
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

Open MySQL Workbench or the MySQL command line and run the schema file:

```bash
mysql -u root -p < schema.sql
```

Or copy/paste the contents of `schema.sql` into MySQL Workbench and execute.

### 5. Configure Database Password

Open `database.py` and change the password on line 12:

```python
'password': 'YOUR_PASSWORD',   # <-- Change this to your MySQL password
```

### 6. Run the Application

```bash
python app.py
```

The app will start at **http://127.0.0.1:5000**. Open that URL in your browser.

---

## Project Structure

```
job_tracker/
├── app.py                  # Main Flask application (routes)
├── database.py             # Database connection and query functions
├── templates/              # HTML templates
│   ├── base.html           # Base layout with sidebar navigation
│   ├── dashboard.html      # Dashboard / statistics overview
│   ├── companies.html      # Companies list page
│   ├── company_form.html   # Add/Edit company form
│   ├── jobs.html           # Jobs list page
│   ├── job_form.html       # Add/Edit job form
│   ├── applications.html   # Applications list page
│   ├── application_form.html # Add/Edit application form
│   ├── contacts.html       # Contacts list page
│   ├── contact_form.html   # Add/Edit contact form
│   └── job_match.html      # Job Match feature page
├── static/
│   └── style.css           # Application stylesheet
├── schema.sql              # MySQL database creation script
├── AI_USAGE.md             # GenAI documentation
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

---

## Database Schema

The application uses **4 tables** with foreign key relationships:

- **companies** — Stores company info (name, industry, location, website)
- **jobs** — Linked to companies; includes a JSON `requirements` column for skills
- **applications** — Linked to jobs; tracks status with ENUM and interview data as JSON
- **contacts** — Linked to companies; stores recruiter/contact details

---

## How the Job Match Feature Works

1. The user enters their skills as a comma-separated list (e.g., "Python, SQL, Flask")
2. The app queries all jobs that have a `requirements` JSON array
3. For each job, it compares the user's skills against the requirements (case-insensitive)
4. It calculates a match percentage: `(matched skills / total required skills) × 100`
5. Results are sorted by percentage (highest first) and color-coded (green ≥ 75%, yellow ≥ 50%, red < 50%)
6. Missing skills are displayed so the user knows what to learn

---

## Author

Dante — Database Systems Course, Spring 2026
