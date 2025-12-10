📘 Machine Test – Python Web Application

A simple full-stack web application developed as part of a machine test. The project uses Python (Flask/Django-like structure), HTML templates, and database connectivity to demonstrate core backend and frontend development skills.

📌 Project Overview

This repository contains a simple machine test project built using Python along with HTML templates for the user interface. The main goal of this project is to demonstrate:

Backend logic handling

Dynamic rendering of HTML pages

Form processing

Connecting and interacting with a database

Clean and understandable project structure

The project is lightweight and easy to set up, making it a good example of basic full-stack application development.

⭐ Features

Python backend application (home-app.py)

HTML templating system (templates/)

Database connection logic included (database-connect.txt)

Simple and clean routing

User input handling

Demonstrates backend–frontend integration

Beginner-friendly code structure

🛠 Tech Stack
Component	Technology
Backend	Python
Frontend	HTML, CSS
Templating	Jinja2-like HTML templates
Database	SQL-based (config in database-connect.txt)
Runtime	Python 3.x
📁 Project Structure
Karthik-P-Machine-Test/
│
├── home-app.py               # Main backend application
├── database-connect.txt      # Database configuration / connection details
│
└── templates/
       ├── index.html
       ├── home.html
       └── other-template-files.html

🚀 Installation

Follow the steps below to set up the project locally.

1. Clone the Repository
git clone https://github.com/Karthik-P05/Karthik-P-Machine-Test.git
cd Karthik-P-Machine-Test

2. Create a Virtual Environment (Recommended)
python -m venv venv

3. Activate the Virtual Environment

Windows:

venv\Scripts\activate


Linux / Mac:

source venv/bin/activate

4. Install Required Python Dependencies

If a requirements.txt exists:

pip install -r requirements.txt


If not, install Flask manually (if used):

pip install flask

⚙ Configuration
Database Setup

Check the file:

database-connect.txt


This may include:

Host

Port

Username

Password

Database name

Update the information according to your local environment.

▶ Running the Application

If it's a Flask application:

python home-app.py


You should see output like:

Running on http://127.0.0.1:5000


Open the URL in your browser.


If you want, I can create a screenshots section design too.

🔮 Future Improvements

Add login & authentication

Add form validations

Improve UI with CSS frameworks

Add CRUD operations

Include Docker support

Add automated tests

👤 Author

Karthik P
GitHub: Karthik-P05
