-- Job Application Tracker Database Schema
-- Run this script to create the database and all tables

CREATE DATABASE IF NOT EXISTS job_tracker;
USE job_tracker;

-- ============================================
-- Table 1: companies
-- ============================================
CREATE TABLE IF NOT EXISTS companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    website VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    notes TEXT
);

-- ============================================
-- Table 2: jobs
-- ============================================
CREATE TABLE IF NOT EXISTS jobs (
    job_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    job_title VARCHAR(100) NOT NULL,
    job_type ENUM('Full-time', 'Part-time', 'Contract', 'Internship') DEFAULT 'Full-time',
    salary_min INT,
    salary_max INT,
    job_url VARCHAR(300),
    date_posted DATE,
    requirements JSON,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE SET NULL
);

-- ============================================
-- Table 3: applications
-- ============================================
CREATE TABLE IF NOT EXISTS applications (
    application_id INT PRIMARY KEY AUTO_INCREMENT,
    job_id INT,
    application_date DATE NOT NULL,
    status ENUM('Applied', 'Screening', 'Interview', 'Offer', 'Rejected', 'Withdrawn') DEFAULT 'Applied',
    resume_version VARCHAR(50),
    cover_letter_sent BOOLEAN DEFAULT FALSE,
    interview_data JSON,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE SET NULL
);

-- ============================================
-- Table 4: contacts
-- ============================================
CREATE TABLE IF NOT EXISTS contacts (
    contact_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    contact_name VARCHAR(100) NOT NULL,
    title VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    linkedin_url VARCHAR(200),
    notes TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE SET NULL
);

-- ============================================
-- Sample Data (optional - for testing)
-- ============================================
INSERT INTO companies (company_name, industry, website, city, state, notes) VALUES
('TechCorp', 'Technology', 'https://techcorp.example.com', 'Miami', 'FL', 'Great culture, remote-friendly'),
('DataCo', 'Data Analytics', 'https://dataco.example.com', 'Austin', 'TX', 'Fast-growing startup'),
('SecureNet', 'Cybersecurity', 'https://securenet.example.com', 'New York', 'NY', 'Fortune 500 company');

INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements) VALUES
(1, 'Software Developer', 'Full-time', 70000, 95000, 'https://techcorp.example.com/careers/dev', '2026-03-15', '["Python", "SQL", "Flask", "HTML", "CSS"]'),
(2, 'Data Analyst', 'Full-time', 60000, 80000, 'https://dataco.example.com/careers/analyst', '2026-03-20', '["Python", "SQL", "Tableau", "Excel"]'),
(1, 'Junior Web Developer', 'Internship', 35000, 45000, 'https://techcorp.example.com/careers/intern', '2026-03-25', '["HTML", "CSS", "JavaScript", "Flask"]'),
(3, 'Security Engineer', 'Full-time', 90000, 120000, 'https://securenet.example.com/careers/seceng', '2026-03-10', '["Python", "Linux", "Networking", "Firewalls"]');

INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data) VALUES
(1, '2026-03-16', 'Interview', 'v2.1', TRUE, '{"round": 2, "type": "Technical", "scheduled": "2026-04-05"}'),
(2, '2026-03-21', 'Applied', 'v2.0', FALSE, NULL),
(4, '2026-03-12', 'Screening', 'v2.1', TRUE, '{"round": 1, "type": "Phone Screen", "scheduled": "2026-04-02"}');

INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes) VALUES
(1, 'Alice Johnson', 'HR Manager', 'alice@techcorp.example.com', '305-555-0101', 'https://linkedin.com/in/alicejohnson', 'Met at career fair'),
(2, 'Bob Martinez', 'Lead Data Scientist', 'bob@dataco.example.com', '512-555-0202', 'https://linkedin.com/in/bobmartinez', 'Connected via LinkedIn'),
(3, 'Carol White', 'Recruiter', 'carol@securenet.example.com', '212-555-0303', 'https://linkedin.com/in/carolwhite', 'Reached out about security role');
