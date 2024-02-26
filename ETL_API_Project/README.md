# ETL and API Project

## Overview

This project demonstrates a Flask-based API and an ETL (Extract, Transform, Load) pipeline, illustrating my capabilities as a Data Engineer. While the scope of the pipeline is intentionally concise due to time constraints—thus not encompassing all potential edge cases—it effectively showcases my workflow and potential productivity.

## Tools Used

- **Flask Framework**: For creating the API server.
- **SQLAlchemy ORM**: Utilized with Flask for database interactions.
- **Pandas**: Employed for dataframe operations and handling file I/O.
- **Black**: Integrated for code formatting to ensure readability and consistency.
- **Pylint**: Used for linting to maintain code quality and standards.

## Installation and Usage

### Prerequisites

- Ensure Python is installed on your system.
- A virtual environment is recommended for project dependencies management.

### Setup

1. Clone the repository to your local machine.
2. Navigate to the project's root directory.
3. Create and activate a virtual environment:
   **For Mac:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   **For Windows:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask server to initialize the database:
   ```bash
   python -m api.app
   ```
   This command creates the `ae.db` database file and initializes the database schema.

2. Ensure you have the necessary CSV files in the `data/raw` directory for data seeding.

3. Execute the ETL process to populate the database:
   ```bash
   python -m etl.load
   ```
   This step processes the CSV files and seeds the database with the extracted information.

4. Access the API endpoints using a tool like Postman or CURL to interact with the data.

## API Endpoints

- **GET `/conditions`**: Fetches a list of all conditions. Returns the conditions data as JSON.
- **GET `/labs`**: Retrieves a list of all laboratory results. Returns the labs data as JSON.
- **GET `/lifestyle`**: Obtains a list of all lifestyle entries. Returns the lifestyle data as JSON.
- **GET `/rx`**: Gathers a list of all prescriptions. Returns the prescriptions data as JSON.
- **GET `/rx/<int:person_id>`**: Fetches prescriptions for a specific person by their ID. Returns the relevant prescriptions data as JSON.
- **GET `/tests`**: Retrieves a list of all tests. Returns the tests data as JSON.
- **GET `/person/<int:person_id>`**: Obtains all data (conditions, labs, lifestyle, prescriptions, tests) for a specific person by their ID. Returns a comprehensive dataset for the person as JSON.
- **GET `/person/<int:person_id>/details`**: Fetches detailed information for a specific person, including prescription status for alpha blockers, latest hemoglobin levels, and the number of visits in the last six months. Returns detailed person data as JSON.