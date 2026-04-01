"""
database.py - Database connection and helper functions for Job Application Tracker.
Handles all MySQL interactions using mysql-connector-python.
"""

import mysql.connector
from mysql.connector import Error

# ============================================
# Database Configuration
# ============================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',   # <-- Change this to your MySQL password
    'database': 'job_tracker'
}


def get_db():
    """Create and return a new database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def close_db(conn):
    """Safely close a database connection."""
    if conn and conn.is_connected():
        conn.close()


# ============================================
# COMPANY Functions
# ============================================
def get_all_companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    close_db(conn)
    return companies


def get_company(company_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies WHERE company_id = %s", (company_id,))
    company = cursor.fetchone()
    close_db(conn)
    return company


def add_company(data):
    conn = get_db()
    cursor = conn.cursor()
    sql = """INSERT INTO companies (company_name, industry, website, city, state, notes)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (data['company_name'], data.get('industry', ''),
              data.get('website', ''), data.get('city', ''),
              data.get('state', ''), data.get('notes', ''))
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    close_db(conn)
    return new_id


def update_company(company_id, data):
    conn = get_db()
    cursor = conn.cursor()
    sql = """UPDATE companies SET company_name=%s, industry=%s, website=%s,
             city=%s, state=%s, notes=%s WHERE company_id=%s"""
    values = (data['company_name'], data.get('industry', ''),
              data.get('website', ''), data.get('city', ''),
              data.get('state', ''), data.get('notes', ''), company_id)
    cursor.execute(sql, values)
    conn.commit()
    close_db(conn)


def delete_company(company_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM companies WHERE company_id = %s", (company_id,))
    conn.commit()
    close_db(conn)


# ============================================
# JOB Functions
# ============================================
def get_all_jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT j.*, c.company_name
             FROM jobs j
             LEFT JOIN companies c ON j.company_id = c.company_id
             ORDER BY j.date_posted DESC"""
    cursor.execute(sql)
    jobs = cursor.fetchall()
    close_db(conn)
    return jobs


def get_job(job_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT j.*, c.company_name
             FROM jobs j
             LEFT JOIN companies c ON j.company_id = c.company_id
             WHERE j.job_id = %s"""
    cursor.execute(sql, (job_id,))
    job = cursor.fetchone()
    close_db(conn)
    return job


def add_job(data):
    conn = get_db()
    cursor = conn.cursor()
    sql = """INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max,
             job_url, date_posted, requirements)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (data.get('company_id') or None, data['job_title'],
              data.get('job_type', 'Full-time'),
              data.get('salary_min') or None, data.get('salary_max') or None,
              data.get('job_url', ''), data.get('date_posted') or None,
              data.get('requirements', '[]'))
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    close_db(conn)
    return new_id


def update_job(job_id, data):
    conn = get_db()
    cursor = conn.cursor()
    sql = """UPDATE jobs SET company_id=%s, job_title=%s, job_type=%s,
             salary_min=%s, salary_max=%s, job_url=%s, date_posted=%s,
             requirements=%s WHERE job_id=%s"""
    values = (data.get('company_id') or None, data['job_title'],
              data.get('job_type', 'Full-time'),
              data.get('salary_min') or None, data.get('salary_max') or None,
              data.get('job_url', ''), data.get('date_posted') or None,
              data.get('requirements', '[]'), job_id)
    cursor.execute(sql, values)
    conn.commit()
    close_db(conn)


def delete_job(job_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
    conn.commit()
    close_db(conn)


# ============================================
# APPLICATION Functions
# ============================================
def get_all_applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT a.*, j.job_title, c.company_name
             FROM applications a
             LEFT JOIN jobs j ON a.job_id = j.job_id
             LEFT JOIN companies c ON j.company_id = c.company_id
             ORDER BY a.application_date DESC"""
    cursor.execute(sql)
    apps = cursor.fetchall()
    close_db(conn)
    return apps


def get_application(application_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT a.*, j.job_title, c.company_name
             FROM applications a
             LEFT JOIN jobs j ON a.job_id = j.job_id
             LEFT JOIN companies c ON j.company_id = c.company_id
             WHERE a.application_id = %s"""
    cursor.execute(sql, (application_id,))
    app = cursor.fetchone()
    close_db(conn)
    return app


def add_application(data):
    conn = get_db()
    cursor = conn.cursor()
    sql = """INSERT INTO applications (job_id, application_date, status,
             resume_version, cover_letter_sent, interview_data)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (data.get('job_id') or None, data['application_date'],
              data.get('status', 'Applied'), data.get('resume_version', ''),
              data.get('cover_letter_sent', False),
              data.get('interview_data') or None)
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    close_db(conn)
    return new_id


def update_application(application_id, data):
    conn = get_db()
    cursor = conn.cursor()
    sql = """UPDATE applications SET job_id=%s, application_date=%s, status=%s,
             resume_version=%s, cover_letter_sent=%s, interview_data=%s
             WHERE application_id=%s"""
    values = (data.get('job_id') or None, data['application_date'],
              data.get('status', 'Applied'), data.get('resume_version', ''),
              data.get('cover_letter_sent', False),
              data.get('interview_data') or None, application_id)
    cursor.execute(sql, values)
    conn.commit()
    close_db(conn)


def delete_application(application_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE application_id = %s", (application_id,))
    conn.commit()
    close_db(conn)


# ============================================
# CONTACT Functions
# ============================================
def get_all_contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT ct.*, c.company_name
             FROM contacts ct
             LEFT JOIN companies c ON ct.company_id = c.company_id
             ORDER BY ct.contact_name"""
    cursor.execute(sql)
    contacts = cursor.fetchall()
    close_db(conn)
    return contacts


def get_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT ct.*, c.company_name
             FROM contacts ct
             LEFT JOIN companies c ON ct.company_id = c.company_id
             WHERE ct.contact_id = %s"""
    cursor.execute(sql, (contact_id,))
    contact = cursor.fetchone()
    close_db(conn)
    return contact


def add_contact(data):
    conn = get_db()
    cursor = conn.cursor()
    sql = """INSERT INTO contacts (company_id, contact_name, title, email,
             phone, linkedin_url, notes)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    values = (data.get('company_id') or None, data['contact_name'],
              data.get('title', ''), data.get('email', ''),
              data.get('phone', ''), data.get('linkedin_url', ''),
              data.get('notes', ''))
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    close_db(conn)
    return new_id


def update_contact(contact_id, data):
    conn = get_db()
    cursor = conn.cursor()
    sql = """UPDATE contacts SET company_id=%s, contact_name=%s, title=%s,
             email=%s, phone=%s, linkedin_url=%s, notes=%s
             WHERE contact_id=%s"""
    values = (data.get('company_id') or None, data['contact_name'],
              data.get('title', ''), data.get('email', ''),
              data.get('phone', ''), data.get('linkedin_url', ''),
              data.get('notes', ''), contact_id)
    cursor.execute(sql, values)
    conn.commit()
    close_db(conn)


def delete_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE contact_id = %s", (contact_id,))
    conn.commit()
    close_db(conn)


# ============================================
# DASHBOARD Statistics
# ============================================
def get_dashboard_stats():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    stats = {}

    cursor.execute("SELECT COUNT(*) as count FROM companies")
    stats['total_companies'] = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM jobs")
    stats['total_jobs'] = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM applications")
    stats['total_applications'] = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM contacts")
    stats['total_contacts'] = cursor.fetchone()['count']

    # Applications by status
    cursor.execute("""SELECT status, COUNT(*) as count
                      FROM applications GROUP BY status ORDER BY count DESC""")
    stats['status_breakdown'] = cursor.fetchall()

    # Recent applications
    cursor.execute("""SELECT a.*, j.job_title, c.company_name
                      FROM applications a
                      LEFT JOIN jobs j ON a.job_id = j.job_id
                      LEFT JOIN companies c ON j.company_id = c.company_id
                      ORDER BY a.application_date DESC LIMIT 5""")
    stats['recent_apps'] = cursor.fetchall()

    close_db(conn)
    return stats


# ============================================
# JOB MATCH Functions
# ============================================
def get_job_matches(user_skills):
    """
    Compare user skills against job requirements.
    Returns jobs ranked by match percentage.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT j.*, c.company_name
             FROM jobs j
             LEFT JOIN companies c ON j.company_id = c.company_id
             WHERE j.requirements IS NOT NULL"""
    cursor.execute(sql)
    jobs = cursor.fetchall()
    close_db(conn)

    import json

    # Normalize user skills to lowercase for comparison
    user_skills_lower = [s.strip().lower() for s in user_skills if s.strip()]
    results = []

    for job in jobs:
        try:
            req = job['requirements']
            # Handle case where requirements is already a list (parsed by connector)
            if isinstance(req, str):
                req = json.loads(req)
            if isinstance(req, list):
                req_lower = [r.strip().lower() for r in req]
                matched = [s for s in user_skills_lower if s in req_lower]
                missing = [r for r in req if r.strip().lower() not in user_skills_lower]
                total = len(req_lower)
                match_count = len(matched)
                percentage = round((match_count / total) * 100) if total > 0 else 0

                results.append({
                    'job': job,
                    'match_percentage': percentage,
                    'matched_skills': match_count,
                    'total_skills': total,
                    'missing_skills': missing
                })
        except (json.JSONDecodeError, TypeError):
            continue

    # Sort by match percentage descending
    results.sort(key=lambda x: x['match_percentage'], reverse=True)
    return results
