# Planetarium Service API

API service for planetarium management written on Django Rest Framework (DRF).


### Install using GitHub

Install PostgresSQL and create db

    ```
    git clone https://github.com/anastmishchuk/planetarium-api-service.git
    cd planetarium-api-service
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

**Set up environment variables:**

    Create a `.env` file in the root directory of your project and 
    add the following environment variables:

    ```
    DB_HOST=<your db hostname>
    DB_NAME=<your db name>
    DB_USER=<your db username>
    DB_PASSWORD=<your db user password>
    SECRET_KEY=<your secret key>
    ```

**Apply the database migrations:**

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

**Create a superuser:**

    ```
    python manage.py createsuperuser
    ```

**Run the development server:**

    ```
    python manage.py runserver
    ```

### Usage

#### Authentication

API uses token-based authentication. Obtain a token by logging in to `/api/user/token/` with your credentials.

#### Features

- JWT authenticated
- Admin panel: /admin/
- Documentation: /api/doc/swagger/
- Managing reservations and tickets
- Creating astronomy shows with show themes
- Creating planetarium domes
- Adding show sessions
- Filtering astronomy shows and show sessions

### Running the tests

To run the tests, use the following command:

```bash
python manage.py test

