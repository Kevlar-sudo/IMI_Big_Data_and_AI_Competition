# IMI_Big_Data_and_AI_Competition

---

This project is designed to analyze transactional data and host a web application to interact with the processed results.

## Features
- **Data Analysis**: Analyze transactional data for anomalies, outliers, and trends.
- **Web Application**: Interactive interface to view and manage transaction data.
- **Reproducible Environment**: Virtual environment for consistent dependency management.

---

## Prerequisites
Ensure you have the following installed:
- Python 3.7 or later
- `pip` (Python package installer)

## Install Packages:
- pip install -r requirements.txt

## Run App:
To Run the web-app, in terminal type:
- python database.py*
- python user_table.py*
- python app.py 

*: You will need to first run the database inserter python script(s) to be able to run critical functions of the application, you do not have to rerun these scripts everytime you want to run the app (only the first time and when you want to clear the databases)


## Access App:
In Browser:
- go to the link, should be http://127.0.0.1:5000/ by default



# Project Structure
.
├── app.py                     # Main web application script
├── code.ipynb                 # Jupyter notebook for data analysis
├── csv_files/                 # Folder containing input CSV files
├── templates/                 # HTML templates for the web app
├── static/                    # Static files for the web app
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── venv/                      # Virtual environment (ignored in version control)
└── mydatabase.db              # SQLite database file
