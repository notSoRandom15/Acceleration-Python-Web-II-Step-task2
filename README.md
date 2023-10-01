# Test-Task
# Acceleration-Python-Web-II-Step-task
Acceleration / Python / Web II Step task


- [How to Run the Project](#how-to-run-the-project)
- [User Authentication](#user-authentication)
- [Docker](#docker)
- [.dockerignore](#dockerignore)
- [docker-compose.yml](#docker-composeyml)
- [Database](#database)
- [Crispy Bootstrap](#crispy-bootstrap)
- [Django Debug](#django-debug)
- [Search and Filters](#search-and-filters)
- [UUID](#uuid)


1. Install all the dependencies from the `requirements.txt` file by running the following Docker command: ```docker-compose up -d --build```

Start the container by typing: ```docker-compose up -d```

make migrations to run the project: ```docker-compose exec web python manage.py migrate```

User Authentication: 
For user authentication, we use django-allauth because it is easy to customize and very simple. It is also considered safe due to thorough testing.

We use AbstractUser as our custom user model. This model behaves identically to the default user model, but it allows for future customization.

Docker:
We have a Dockerfile in place to create and run a custom Docker image for our project.

.dockerignore
The .dockerignore file specifies certain files and directories that should not be included in the Docker image.

docker-compose.yml
The docker-compose.yml file is used to run the Docker container for our project.

Database
We use PostgreSQL as the database, which is a widely adopted choice for database management.

Crispy Bootstrap
We utilize Django Crispy Forms to enhance the styling of forms in our templates.

Django Debug
We employ django-debug-toolbar to assist in solving the n+1 problem and debugging the application.

Search and Filters
Search functionality is implemented using class-based views and querysets.
Filtering is achieved using the Django Filter API.
UUID
Instead of using just integer primary keys (int:pk), we use UUIDs for added security and safety.
