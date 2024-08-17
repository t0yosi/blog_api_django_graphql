

# Django - GraphQl Blog Api

## Overview

    ####dqlBlog is a web application built using Django and GraphQL, designed for [brief description of the project purpose]. This README provides instructions for setting up the project, an overview of its architecture, and details on the assumptions and decisions made during development.

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Django 4.x
- Graphene-Django
- PostgreSQL (for production), SQLite (for development)

### Installation

1. **Clone the Repository**

   ```sh```

        git clone https://github.com/t0yosi/blog_api_django_graphql.git
        
        cd backend

2.  **Create a Virtual Environment**

    ```sh```

        python -m venv venv

3. **Activate the Virtual Environment**

    On Windows:

    ```sh```

        venv\Scripts\activate

    On macOS/Linux:

    ```sh```

        source venv/bin/activate

4. **Install Dependencies**

    ```sh```

        pip install -r requirements.txt

5. **Set Up the Database**

    No additional setup required; SQLite is used by default.


6. **Apply Migrations**

    ```sh```

        python manage.py migrate

    Create a Superuser (optional)

    ```sh```

        python manage.py createsuperuser

    Run the Development Server

    ```sh```

        python manage.py runserver

    Access the Application

        Open your browser and navigate to http://127.0.0.1:8000/ to see the application in action.

        Open your browser and navigate to http://127.0.0.1:8000/graphql/ to use the graphql playground.

7. ***Running Tests***

    To run the test suite, execute:

    ```sh```

        python manage.py test




***Architecture***
    Components

        Django: Used for the web framework and ORM. Handles routing, views, and models.
        Graphene-Django: Provides GraphQL integration for querying and mutating data.
        PostgreSQL: (Optional) Used as the production database. SQLite is used by default for development.

        Models

            Author: Represents authors with a one-to-one relationship with Django's User model. Contains name, email, and bio.
            Post: Represents blog posts. Linked to Author through a foreign key.
            Comment: Represents comments on blog posts. Linked to Post through a foreign key.

    GraphQL

        Queries: Allows fetching of Author, Post, and Comment data. Supports filtering and pagination.
        Mutations: Supports creating, updating, and deleting Author, Post, and Comment instances. Includes authentication for certain mutations.

***Assumptions and Decisions***

    Authentication: JWT authentication is used for securing mutations that modify data. Ensure you have set up JWT tokens in your GraphQL configuration.
    Database: SQLite is used by default for development due to its simplicity. For production, PostgreSQL is recommended due to better performance and features.
    Testing: Tests are written using Django’s built-in test framework. Ensure your test database is set up correctly.
    Environment: The project is designed to be run in a virtual environment to manage dependencies and isolate the project environment.