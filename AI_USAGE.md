# AI Usage Documentation

## Tools Used

- **Claude** (Anthropic) — Used for generating initial project structure, Flask route logic, database helper functions, HTML templates, and CSS styling
- **ChatGPT** (OpenAI, GPT-4) — Used for debugging MySQL connector issues and explaining JSON column usage in MySQL

## Key Prompts

1. "Build a Flask application for a job application tracker with CRUD operations for companies, jobs, applications, and contacts tables"
2. "Write a Python function that compares a user's skills against job requirements stored as a JSON array in MySQL and returns a match percentage"
3. "Create an HTML form template using Jinja2 that handles both add and edit modes for a company record"
4. "Help me debug this error: mysql.connector.errors.ProgrammingError when inserting into a table with ENUM columns"
5. "Write a SQL schema with 4 tables that use foreign keys, JSON columns, and ENUM types for a job tracker"
6. "Style a sidebar navigation layout with CSS that highlights the active page"

## What Worked Well

- AI generated the basic CRUD functions for all four tables very quickly, which saved a lot of time on repetitive boilerplate code
- The Job Match algorithm suggestion of normalizing skills to lowercase for case-insensitive comparison was a good approach I hadn't considered at first
- AI was great at explaining how MySQL handles JSON columns and how to parse them in Python using `json.loads()`
- Getting a complete CSS stylesheet with status badges, responsive layout, and a dashboard grid was much faster with AI than writing it from scratch
- The Jinja2 template inheritance pattern (base.html with blocks) was suggested by AI and it made the templates very clean and easy to manage

## What I Modified

- Changed all the database column names and table structure to match the exact schema from the project specification — the AI initially used slightly different naming conventions
- Added input validation that the AI didn't include (checking for required fields before inserting)
- Fixed the `get_job_matches()` function — the AI version didn't handle the case where `requirements` was already parsed as a list by the MySQL connector (not always a string)
- Modified the delete routes to use POST method with confirmation dialogs instead of the GET-based delete links the AI originally suggested (better security practice)
- Adjusted the form templates to properly handle the difference between "add" and "edit" modes, especially pre-populating fields from existing data
- Rewrote the CSS color scheme and spacing to match my own design preferences rather than the generic Bootstrap-like look the AI first gave me
- Added the interview_data JSON handling in the application form — the AI gave me a single text field but I broke it into separate fields for round, type, and scheduled date
- Added the sample data INSERT statements to schema.sql for testing — the AI only generated the CREATE TABLE statements initially

## Lessons Learned

- Always test AI-generated code line by line. The AI got the overall structure right but had small bugs, like not handling `None` values from optional form fields, that would have caused crashes at runtime
- AI is really good at boilerplate and repetitive patterns (writing 4 sets of CRUD functions, for example), but the business logic like the job matching algorithm needed me to think through the edge cases myself
- Asking the AI to "explain" its code helped me learn — I didn't just copy/paste, I made sure I understood the Flask routing, Jinja2 templating, and MySQL connector patterns before using them
- The AI sometimes generates outdated patterns. For example, it suggested using `@app.route('/delete/<id>')` with GET, but POST is the safer approach for destructive actions
- Using AI as a "first draft" tool and then refining the output myself was the most effective workflow. It let me focus my time on the harder parts like the Job Match feature and the UI design
