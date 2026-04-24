# ServicePub

ServicePub is a comprehensive Django-based web application designed to digitize and streamline public administrative services. It provides a secure platform for citizens to request documents, track their status, and communicate with administrative agents, while offering agents a robust dashboard to manage, process, and finalize requests.

## Features

* Role-Based Access Control: Distinct interfaces and permissions for Citizens (Citoyen) and Administrative Agents (Agent).
* Request Management: Citizens can submit requests for various administrative services (e.g., passports, certificates).
* Document Upload & Processing: Secure upload of supporting documents by citizens and generation/upload of final official documents by agents.
* Real-time Tracking & Notifications: Status updates and internal notifications keep citizens informed about the progress of their requests.
* Payment Integration: Built-in flow for handling service fees and generating receipts.
* Admin Dashboard: Comprehensive statistics, agent management, and request overview for administrators.

## Technology Stack

* Backend: Python, Django 6.0
* Database: SQLite (configured for rapid deployment and testing)
* Frontend: HTML5, CSS3, JavaScript
* Server/Deployment: Gunicorn, WhiteNoise (for static file handling), Bash scripting for automated deployment tasks

## Local Development Setup

### Prerequisites
* Python 3.10 or higher
* pip (Python package installer)

### Installation

1. Clone the repository:
   git clone https://github.com/YOUR_USERNAME/servicepub-django.git
   cd servicepub-django

2. Create and activate a virtual environment:
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate

3. Install the dependencies:
   pip install -r requirements.txt

4. Run database migrations:
   python manage.py migrate

5. (Optional) Seed the database with test data:
   python seed_users.py
   python seed_services.py

6. Start the development server:
   python manage.py runserver

7. Access the application in your browser at: http://127.0.0.1:8000

## Deployment (Railway)

This project is pre-configured for seamless deployment on Railway.

1. Push your repository to GitHub.
2. Log in to Railway.app and create a new project.
3. Select "Deploy from GitHub repo" and choose this repository.
4. Railway will automatically detect the Procfile and Python environment.
5. In the Railway project settings, go to the "Variables" tab and add:
   * PORT: 8000
6. The `start.sh` script will automatically handle database migrations, static file collection, and database seeding upon startup.

## Project Structure

* accounts/: User authentication, profiles, and custom user models.
* demandes/: Core logic for submitting, viewing, and processing service requests.
* services/: Management of available administrative services and their tariffs.
* paiements/: Payment tracking and receipt generation.
* notifications/: Internal system alerts for status changes.
* public_pages/: Landing pages, FAQs, and general information.
* static/: CSS, JavaScript, and image assets.
* templates/: HTML templates organized by application.

## Security Notes

The application uses Django's built-in CSRF protection. If deploying to a custom domain, ensure you update the `CSRF_TRUSTED_ORIGINS` array in `servicepub/settings.py` to match your production URL.
