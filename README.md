
# Archane.ai

## Project Description  

This repository contains an experimental prototype inspired by the **PIANO (Parallel Information Aggregation via Neural Orchestration)** architecture, proposed in *[Project Sid: Many-agent simulations toward AI civilization](https://arxiv.org/pdf/2411.00114)*.  

The goal is to explore how **LLM-based autonomous agents** can:  
- **Think and act in parallel** through concurrent modules (cognition, planning, memory, social interaction, skill execution).  
- Maintain **coherence** across multiple output streams (actions, language, behaviors) via a centralized *Cognitive Controller*.  


## Getting Started

This guide will walk you through setting up the Archane.ai project locally using Docker and Django.

### Prerequisites

- Docker and Docker Compose installed on your machine.
- Basic knowledge of Django and Docker.

### Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-repo/Archane.git
   cd Archane
   ```

2. **Set Up Environment Variables**

   Create the necessary environment files in the `docker/environments/` directory:

   - `django.env` for Django settings.
   - `postgres.env` for PostgreSQL settings.

   Example `django.env`:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
   ```

   Example `postgres.env`:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=postgres
   ```

3. **Build and Run the Docker Containers**

   Use the `docker-compose.yml` file to build and start the services:

   ```bash
   docker-compose up --build
   ```

   This will:
   - Build the Django application.
   - Set up the PostgreSQL database.
   - Run migrations and collect static files.
   - Start the Django development server.

4. **Access the Application**

   Once the containers are up and running, you can access the Django application at:

   ```bash
   http://localhost:8000
   ```

### Development Mode
1. **Start postgres**

   For development, you can use the `dev-docker-compose.yml` file to start only the PostgreSQL database:
   ```bash
   docker-compose -f dev-docker-compose.yml up
   ```
2. **Run Migrations Manually**

     ```bash
       cd src
       ./manage.py migrate
     ```

3. **Create a Superuser**

     ```bash
       ./manage.py createsuperuser
     ```

4. **Run Django**

   ```bash
   ./manage.py runserver
   ```

5. **Access the Application**

   Once the containers are up and running, you can access the Django application at:

   ```bash
   http://localhost:8000
   ```
### Stop the Containers

  ```bash
    docker-compose down
   ```
or in development mode
   ```bash
    docker-compose -f dev-docker-compose.yml  down
   ```
### Troubleshooting

- Ensure that the environment variables are correctly set in the `.env` files.
- Check Docker logs for any errors:

  ```bash
  docker-compose logs -f
  ```

For more information, refer to the [Django documentation](https://docs.djangoproject.com/) and [Docker documentation](https://docs.docker.com/).
