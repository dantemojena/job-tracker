"""
app.py - Main Flask application for Job Application Tracker.
Provides routes for CRUD operations on companies, jobs, applications,
contacts, plus a dashboard and job match feature.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import json
from database import (
    get_all_companies, get_company, add_company, update_company, delete_company,
    get_all_jobs, get_job, add_job, update_job, delete_job,
    get_all_applications, get_application, add_application, update_application, delete_application,
    get_all_contacts, get_contact, add_contact, update_contact, delete_contact,
    get_dashboard_stats, get_job_matches
)

app = Flask(__name__)
app.secret_key = 'job-tracker-secret-key-change-me'


# ============================================
# DASHBOARD
# ============================================
@app.route('/')
def dashboard():
    stats = get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)


# ============================================
# COMPANIES ROUTES
# ============================================
@app.route('/companies')
def companies_list():
    companies = get_all_companies()
    return render_template('companies.html', companies=companies)


@app.route('/companies/add', methods=['GET', 'POST'])
def companies_add():
    if request.method == 'POST':
        data = {
            'company_name': request.form['company_name'],
            'industry': request.form.get('industry', ''),
            'website': request.form.get('website', ''),
            'city': request.form.get('city', ''),
            'state': request.form.get('state', ''),
            'notes': request.form.get('notes', '')
        }
        if not data['company_name']:
            flash('Company name is required.', 'error')
            return render_template('company_form.html', company=data, action='Add')
        add_company(data)
        flash('Company added successfully!', 'success')
        return redirect(url_for('companies_list'))
    return render_template('company_form.html', company={}, action='Add')


@app.route('/companies/edit/<int:company_id>', methods=['GET', 'POST'])
def companies_edit(company_id):
    if request.method == 'POST':
        data = {
            'company_name': request.form['company_name'],
            'industry': request.form.get('industry', ''),
            'website': request.form.get('website', ''),
            'city': request.form.get('city', ''),
            'state': request.form.get('state', ''),
            'notes': request.form.get('notes', '')
        }
        if not data['company_name']:
            flash('Company name is required.', 'error')
            return render_template('company_form.html', company=data, action='Edit')
        update_company(company_id, data)
        flash('Company updated successfully!', 'success')
        return redirect(url_for('companies_list'))
    company = get_company(company_id)
    if not company:
        flash('Company not found.', 'error')
        return redirect(url_for('companies_list'))
    return render_template('company_form.html', company=company, action='Edit')


@app.route('/companies/delete/<int:company_id>', methods=['POST'])
def companies_delete(company_id):
    delete_company(company_id)
    flash('Company deleted.', 'success')
    return redirect(url_for('companies_list'))


# ============================================
# JOBS ROUTES
# ============================================
@app.route('/jobs')
def jobs_list():
    jobs = get_all_jobs()
    # Parse requirements JSON for display
    for job in jobs:
        try:
            req = job.get('requirements')
            if isinstance(req, str):
                job['requirements_list'] = json.loads(req)
            elif isinstance(req, list):
                job['requirements_list'] = req
            else:
                job['requirements_list'] = []
        except (json.JSONDecodeError, TypeError):
            job['requirements_list'] = []
    return render_template('jobs.html', jobs=jobs)


@app.route('/jobs/add', methods=['GET', 'POST'])
def jobs_add():
    companies = get_all_companies()
    if request.method == 'POST':
        # Convert comma-separated skills into a JSON array string
        skills_input = request.form.get('requirements', '')
        skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]
        data = {
            'company_id': request.form.get('company_id') or None,
            'job_title': request.form['job_title'],
            'job_type': request.form.get('job_type', 'Full-time'),
            'salary_min': request.form.get('salary_min') or None,
            'salary_max': request.form.get('salary_max') or None,
            'job_url': request.form.get('job_url', ''),
            'date_posted': request.form.get('date_posted') or None,
            'requirements': json.dumps(skills_list)
        }
        if not data['job_title']:
            flash('Job title is required.', 'error')
            return render_template('job_form.html', job=data, companies=companies, action='Add')
        add_job(data)
        flash('Job added successfully!', 'success')
        return redirect(url_for('jobs_list'))
    return render_template('job_form.html', job={}, companies=companies, action='Add')


@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
def jobs_edit(job_id):
    companies = get_all_companies()
    if request.method == 'POST':
        skills_input = request.form.get('requirements', '')
        skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]
        data = {
            'company_id': request.form.get('company_id') or None,
            'job_title': request.form['job_title'],
            'job_type': request.form.get('job_type', 'Full-time'),
            'salary_min': request.form.get('salary_min') or None,
            'salary_max': request.form.get('salary_max') or None,
            'job_url': request.form.get('job_url', ''),
            'date_posted': request.form.get('date_posted') or None,
            'requirements': json.dumps(skills_list)
        }
        if not data['job_title']:
            flash('Job title is required.', 'error')
            return render_template('job_form.html', job=data, companies=companies, action='Edit')
        update_job(job_id, data)
        flash('Job updated successfully!', 'success')
        return redirect(url_for('jobs_list'))
    job = get_job(job_id)
    if not job:
        flash('Job not found.', 'error')
        return redirect(url_for('jobs_list'))
    # Convert requirements JSON to comma string for the form
    try:
        req = job.get('requirements')
        if isinstance(req, str):
            req = json.loads(req)
        if isinstance(req, list):
            job['requirements_str'] = ', '.join(req)
        else:
            job['requirements_str'] = ''
    except (json.JSONDecodeError, TypeError):
        job['requirements_str'] = ''
    return render_template('job_form.html', job=job, companies=companies, action='Edit')


@app.route('/jobs/delete/<int:job_id>', methods=['POST'])
def jobs_delete(job_id):
    delete_job(job_id)
    flash('Job deleted.', 'success')
    return redirect(url_for('jobs_list'))


# ============================================
# APPLICATIONS ROUTES
# ============================================
@app.route('/applications')
def applications_list():
    applications = get_all_applications()
    return render_template('applications.html', applications=applications)


@app.route('/applications/add', methods=['GET', 'POST'])
def applications_add():
    jobs = get_all_jobs()
    if request.method == 'POST':
        cover = True if request.form.get('cover_letter_sent') else False
        # Build interview data JSON from form fields
        interview_round = request.form.get('interview_round', '')
        interview_type = request.form.get('interview_type', '')
        interview_scheduled = request.form.get('interview_scheduled', '')
        interview_data = None
        if interview_round or interview_type or interview_scheduled:
            interview_data = json.dumps({
                'round': interview_round,
                'type': interview_type,
                'scheduled': interview_scheduled
            })
        data = {
            'job_id': request.form.get('job_id') or None,
            'application_date': request.form['application_date'],
            'status': request.form.get('status', 'Applied'),
            'resume_version': request.form.get('resume_version', ''),
            'cover_letter_sent': cover,
            'interview_data': interview_data
        }
        if not data['application_date']:
            flash('Application date is required.', 'error')
            return render_template('application_form.html', app=data, jobs=jobs, action='Add')
        add_application(data)
        flash('Application added successfully!', 'success')
        return redirect(url_for('applications_list'))
    return render_template('application_form.html', app={}, jobs=jobs, action='Add')


@app.route('/applications/edit/<int:application_id>', methods=['GET', 'POST'])
def applications_edit(application_id):
    jobs = get_all_jobs()
    if request.method == 'POST':
        cover = True if request.form.get('cover_letter_sent') else False
        interview_round = request.form.get('interview_round', '')
        interview_type = request.form.get('interview_type', '')
        interview_scheduled = request.form.get('interview_scheduled', '')
        interview_data = None
        if interview_round or interview_type or interview_scheduled:
            interview_data = json.dumps({
                'round': interview_round,
                'type': interview_type,
                'scheduled': interview_scheduled
            })
        data = {
            'job_id': request.form.get('job_id') or None,
            'application_date': request.form['application_date'],
            'status': request.form.get('status', 'Applied'),
            'resume_version': request.form.get('resume_version', ''),
            'cover_letter_sent': cover,
            'interview_data': interview_data
        }
        if not data['application_date']:
            flash('Application date is required.', 'error')
            return render_template('application_form.html', app=data, jobs=jobs, action='Edit')
        update_application(application_id, data)
        flash('Application updated successfully!', 'success')
        return redirect(url_for('applications_list'))
    application = get_application(application_id)
    if not application:
        flash('Application not found.', 'error')
        return redirect(url_for('applications_list'))
    # Parse interview_data for form
    try:
        idata = application.get('interview_data')
        if isinstance(idata, str):
            idata = json.loads(idata)
        if isinstance(idata, dict):
            application['interview_round'] = idata.get('round', '')
            application['interview_type'] = idata.get('type', '')
            application['interview_scheduled'] = idata.get('scheduled', '')
        else:
            application['interview_round'] = ''
            application['interview_type'] = ''
            application['interview_scheduled'] = ''
    except (json.JSONDecodeError, TypeError):
        application['interview_round'] = ''
        application['interview_type'] = ''
        application['interview_scheduled'] = ''
    return render_template('application_form.html', app=application, jobs=jobs, action='Edit')


@app.route('/applications/delete/<int:application_id>', methods=['POST'])
def applications_delete(application_id):
    delete_application(application_id)
    flash('Application deleted.', 'success')
    return redirect(url_for('applications_list'))


# ============================================
# CONTACTS ROUTES
# ============================================
@app.route('/contacts')
def contacts_list():
    contacts = get_all_contacts()
    return render_template('contacts.html', contacts=contacts)


@app.route('/contacts/add', methods=['GET', 'POST'])
def contacts_add():
    companies = get_all_companies()
    if request.method == 'POST':
        data = {
            'company_id': request.form.get('company_id') or None,
            'contact_name': request.form['contact_name'],
            'title': request.form.get('title', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'linkedin_url': request.form.get('linkedin_url', ''),
            'notes': request.form.get('notes', '')
        }
        if not data['contact_name']:
            flash('Contact name is required.', 'error')
            return render_template('contact_form.html', contact=data, companies=companies, action='Add')
        add_contact(data)
        flash('Contact added successfully!', 'success')
        return redirect(url_for('contacts_list'))
    return render_template('contact_form.html', contact={}, companies=companies, action='Add')


@app.route('/contacts/edit/<int:contact_id>', methods=['GET', 'POST'])
def contacts_edit(contact_id):
    companies = get_all_companies()
    if request.method == 'POST':
        data = {
            'company_id': request.form.get('company_id') or None,
            'contact_name': request.form['contact_name'],
            'title': request.form.get('title', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'linkedin_url': request.form.get('linkedin_url', ''),
            'notes': request.form.get('notes', '')
        }
        if not data['contact_name']:
            flash('Contact name is required.', 'error')
            return render_template('contact_form.html', contact=data, companies=companies, action='Edit')
        update_contact(contact_id, data)
        flash('Contact updated successfully!', 'success')
        return redirect(url_for('contacts_list'))
    contact = get_contact(contact_id)
    if not contact:
        flash('Contact not found.', 'error')
        return redirect(url_for('contacts_list'))
    return render_template('contact_form.html', contact=contact, companies=companies, action='Edit')


@app.route('/contacts/delete/<int:contact_id>', methods=['POST'])
def contacts_delete(contact_id):
    delete_contact(contact_id)
    flash('Contact deleted.', 'success')
    return redirect(url_for('contacts_list'))


# ============================================
# JOB MATCH FEATURE
# ============================================
@app.route('/job-match', methods=['GET', 'POST'])
def job_match():
    results = None
    user_skills = ''
    if request.method == 'POST':
        user_skills = request.form.get('skills', '')
        skills_list = [s.strip() for s in user_skills.split(',') if s.strip()]
        if skills_list:
            results = get_job_matches(skills_list)
        else:
            flash('Please enter at least one skill.', 'error')
    return render_template('job_match.html', results=results, user_skills=user_skills)


# ============================================
# RUN APPLICATION
# ============================================
if __name__ == '__main__':
    app.run(debug=True)
