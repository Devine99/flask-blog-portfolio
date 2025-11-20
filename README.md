# Devine's Blog - Flask Blog Application

A feature-rich, production-ready blog application built with Flask that allows users to read posts, register accounts, comment on content, and contact the site owner. Admin users can create, edit, and delete blog posts.

## 🌟 Features

### Core Functionality

* **Blog System:** Create, read, edit, and delete blog posts.
* **User Authentication:** Secure registration, login, and logout system.
* **Comment System:** Authenticated users can comment on posts.
* **Contact Form:** Secure contact system with email notifications.
* **Responsive Design:** Mobile-friendly Bootstrap 5 UI.

### Security Features

* **HTML Sanitization:** Uses `Bleach` to prevent XSS attacks in comments/posts.
* **Password Security:** Hashing with PBKDF2-SHA256.
* **CSRF Protection:** All forms include CSRF tokens.
* **Rate Limiting:** Contact forms limited to 5 requests per minute.
* **SQL Injection Prevention:** SQLAlchemy ORM usage.

### Advanced Features

* **Database Migrations:** Managed via Flask-Migrate (Alembic).
* **Caching:** Flask-Caching implemented for static pages.
* **Rich Text Editing:** Integrated CKEditor for writing posts.
* **Gravatar:** Automatic user avatars based on email.

## 🛠 Technology Stack

* **Backend:** Flask, SQLAlchemy, Gunicorn
* **Frontend:** Bootstrap 5, Jinja2, CKEditor
* **Database:** PostgreSQL (Production), SQLite (Development)
* **Extensions:** Flask-Login, Flask-Mail, Flask-Migrate, Flask-Limiter

## 📁 Project Structure

```text
blog-site/
├── app/                     # Main application package
│   ├── __init__.py          # App factory
│   ├── config.py            # Environment configuration
│   ├── extensions.py        # Flask extensions (DB, Mail, etc.)
│   ├── forms.py             # WTForms definitions
│   ├── models.py            # Database models
│   ├── routes.py            # View functions & logic
│   ├── utils.py             # Helper functions
│   ├── static/              # CSS, JS, and Images
│   └── templates/           # HTML Templates
├── migrations/              # Database migration versions
├── requirements.txt         # Dependencies
├── Procfile                 # Render deployment command
└── run.py                   # Application entry point


🚀 Installation & Local Setup

Prerequisites
    Python 3.10+
    Git

Step 1: Clone the Repository
    git clone [https://github.com/Devine99/blog-site.git](https://github.com/Devine99/blog-site.git)
    cd blog-site


Step 2: Create Virtual Environment
    python -m venv venv

    # Windows
    venv\Scripts\activate

    # Mac/Linux
    source venv/bin/activate


Step 3: Install Dependencies
    pip install -r requirements.txt


Step 4: Environment Configuration
    Create a .env file in the root directory:

    # Security
    SECRET_KEY=your-super-secret-key
    SECURITY_PASSWORD_SALT=your-salt-string

    # Database (Defaults to SQLite locally if not set)
    # DATABASE_URL=postgresql://user:pass@localhost/dbname

    # Email (Required for Contact Form)
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=your-email@gmail.com
    MAIL_PASSWORD=your-app-password


Step 5: Initialize Database
    Initialize the database and apply migrations:

    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade


Step 6: Run the Application
    python run.py

    The application will be available at http://localhost:8080



☁️ Deployment to Render.com
This project includes a Procfile and is configured for seamless deployment on Render.com.

Step 1. Push to GitHub: Commit your changes and push to your repository.


Step 2. Create Web Service:
    Log in to the Render Dashboard.
    Click New + and select Web Service.
    Connect your GitHub repository.
    Settings:
        Runtime: Python 3
        Build Command: pip install -r requirements.txt
        Start Command: gunicorn run:app


Step 3: Configure Environment Variables
    In the Render dashboard, go to the Environment tab and add the following keys:
    Key                         Value
    PYTHON_VERSION              3.11.5 (or your local version)
    SECRET_KEY                  (A long random string)
    SECURITY_PASSWORD_SALT      (A long random string)
    MAIL_USERNAME               (Your email address)
    MAIL_PASSWORD               (Your email app password)
    MAIL_SERVER                 smtp.gmail.com
    MAIL_PORT                   587
    MAIL_USE_TLS                true


Step 4. Add Database:
    On Render, click New + and select PostgreSQL.
    Create the database and copy the Internal Database URL.
    Return to your Web Service's Environment tab.
    Add a new variable:
        Key: DATABASE_URL
        Value: (Paste the Internal Database URL here)


Step 5: Final Database Setup
    Once the deployment is live (you may see "Healthy" in the logs), you need to create the tables in the live database:
        Go to the Shell tab in your Render Web Service.
        Run the upgrade command:
        flask db upgrade
        (Note: If this is the first time and migrations fail, you may need to run flask db init and flask db migrate inside the shell first, but usually upgrade is sufficient if the migration folder is in Git).


👤 User Roles
    Admin (User ID = 1): The first user registered (or the user with ID 1 in the database) is automatically granted Admin privileges. Admins can create, edit, and delete posts.
    Regular Users: Can register, log in, and comment on posts.


📞 Contact
    Developer: Devine Enukorah
    Twitter: @Bless001_
    GitHub: Devine99
    Email: enukorahdevine@gmail.com


📄 License
    This project is licensed under the MIT License.
