# User Profile API

This repository contains a Python-based microservice for managing user profiles. Built with Flask and Connexion, it provides a RESTful API for handling users, roles, locations, activities, and saved trails. The application uses SQLAlchemy for database operations with a Microsoft SQL Server and Marshmallow for data serialization. It is fully containerized using Docker.

## Features

- **User Management**: Complete CRUD (Create, Read, Update, Delete) operations for user profiles.
- **Role-Based Access Control (RBAC)**: Differentiates between `general user` and `administrator` roles, with specific endpoints restricted to administrators.
- **Authentication**: Session-based login and logout functionality to secure endpoints.
- **Data Management**: Full CRUD capabilities for related data models including `Roles`, `Activities`, and `Locations`.
- **User Preferences**: Users can manage their list of favorite activities and saved trails.
- **Audit Logging**: A trigger-like mechanism logs the creation of new users for administrative review.
- **Interactive API Documentation**: Utilizes Swagger UI for a user-friendly interface to explore and test the API endpoints.
- **Containerization**: Includes a `Dockerfile` for easy setup and deployment.

## Technology Stack

- **Backend**: Python, Flask, Connexion
- **Database**: Microsoft SQL Server (via `pyodbc`)
- **ORM / Serialization**: SQLAlchemy, Marshmallow
- **API Specification**: OpenAPI 3.0 (Swagger)
- **Containerization**: Docker

## Getting Started

### Prerequisites

- Python 3.9+ and `pip`
- Docker
- A running instance of Microsoft SQL Server

### Database Setup

1.  **Configure Connection**: Before running the application, you must update the database connection string in `config.py`. Modify the `SQLALCHEMY_DATABASE_URI` to include your SQL Server's details (server, database, username, password).

    ```python
    # config.py
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mssql+pyodbc:///?odbc_connect="
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=your_server_address;"
        "DATABASE=your_database_name;"
        "UID=your_username;"
        "PWD=your_password;"
        "TrustServerCertificate=yes;"
        "Encrypt=yes;"
    )
    ```

2.  **Initialize Database**: The repository includes scripts to build and seed the database. Run the main build script to create the `CW2` schema, all necessary tables, and populate them with initial test data.

    ```bash
    python database_Builders/build_database.py
    ```
    This will create test users, including administrators, which are needed to access protected endpoints.

### Local Installation (Without Docker)

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/jorjitdasoria/cw2.git
    cd cw2
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**:
    ```bash
    python app.py
    ```
    The application will be available at `http://localhost:8000`.

### Running with Docker

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/jorjitdasoria/cw2.git
    cd cw2
    ```

2.  **Update Configuration**: Ensure you have updated the database connection string in `config.py` as described in the **Database Setup** section. This is a required step before building the image.

3.  **Build the Docker Image**:
    ```bash
    docker build -t user-profile-api .
    ```

4.  **Run the Docker Container**:
    ```bash
    docker run -p 8000:8000 user-profile-api
    ```
    The application will be available at `http://localhost:8000`.

## Usage

Once the application is running, you can interact with the API.

-   **API Home**: A simple welcome page is available at `http://localhost:8000/`.
-   **Swagger UI**: The interactive API documentation is available at `http://localhost:8000/api/ui`. This interface allows you to view all available endpoints, see their required parameters, and test them directly from your browser.

### Authentication

Several endpoints require authentication. To use them, you must first log in using the `/api/login` endpoint with the credentials of an existing user (e.g., one of the test users created by `build_database.py`). This will create a session cookie that authorizes subsequent requests.

-   **Example Admin User**: `email: ada@example.com`, `password: secure_password_1`
-   **Example General User**: `email: tim@example.com`, `password: hashed_secret_password`

Administrator-only endpoints (e.g., creating/deleting users, managing locations) will return a `403 Forbidden` error if accessed by a general user or an unauthenticated user.

## API Endpoints

The API is structured around the following resources:

| Endpoint Path                         | Description                                            | Authentication       |
| ------------------------------------- | ------------------------------------------------------ | -------------------- |
| `/api/login`                          | Logs a user in and creates a session.                  | None                 |
| `/api/logout`                         | Logs a user out and clears the session.                | Required             |
| `/api/users`                          | Get all users or create a new user.                    | Admin for `POST`     |
| `/api/users/{user_id}`                | Read, update, or delete a specific user.               | Admin for `PUT/DELETE` |
| `/api/users/{user_id}/saved_trails`   | Get or add saved trails for a user.                    | Owner or Admin       |
| `/api/users/{user_id}/saved_trails/{trail_id}` | Remove a saved trail from a user's profile.   | Owner or Admin       |
| `/api/users/{user_id}/activities`     | Add a favorite activity to a user's profile.           | Owner or Admin       |
| `/api/users/{user_id}/activities/{activity_id}` | Remove a favorite activity from a user.      | Owner or Admin       |
| `/api/roles`                          | Get all roles or create a new one.                     | Admin for `POST`     |
| `/api/activities`                      | Get all activities or create a new one.                | Admin for `POST`      |
| `/api/locations`                      | Get all locations or create a new one.                 | Admin for `POST`     |
| `/api/user_logs`                      | Retrieve audit logs for user creation events.          | Admin Only           |

## Project Structure

```
.
├── Dockerfile                  # Defines the Docker container for the application.
├── app.py                      # Main Flask application entry point.
├── auth.py                     # Handles login/logout logic.
├── config.py                   # Application configuration (database, secret key).
├── models.py                   # SQLAlchemy database models and Marshmallow schemas.
├── requirements.txt            # Python dependencies.
├── swagger.yml                 # OpenAPI 3.0 specification for the API.
├── *.py                        # Modules containing business logic for each resource.
├── database_Builders/          # Scripts to build and seed the database.
│   ├── build_database.py       # Main script to create schema and populate all tables.
│   └── ...
└── templates/
    └── home.html               # Simple HTML landing page.
