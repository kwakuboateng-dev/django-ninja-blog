# Django Ninja Blog API Project

Welcome to the **Django Ninja Blog API** project! This project is a CRUD-based blogging API built using **Django** and **Django Ninja**, designed for simplicity, performance, and extensibility. Below, you'll find a comprehensive guide on setting up, running, and interacting with this project.

## Table of Contents

- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Environment Variables](#4-environment-variables)
- [Database Migrations](#database-migrations)
- [Running the Server](#running-the-server)
- [User Management](#user-management)
- [Generating Sample Data](#generating-sample-data)
- [Using the API](#using-the-api)
- [Scripts and Automation](#scripts-and-automation)
  - [Commands Overview](#commands-overview)
- [Project Structure](#project-structure)
- [Logging Configuration](#logging-configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Project Overview

The **Django Ninja Blog API** provides endpoints for managing blog posts and comments. It features user authentication, JWT-based token handling, and structured logging. It also includes management commands for easily generating sample data for testing and development.

---

## Requirements

Before setting up the project, ensure that your system meets the following requirements:

- **Python**: Version 3.8 or higher.
- **Django**: Version 5.1.2.
- **Virtual Environment**: Recommended for isolating dependencies.
- **Pip**: For package management and dependency installation.
- **PostgreSQL** (optional): Can use SQLite if preferred.

---

## Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/kwakuboateng-dev/django-ninja-blog.git
cd django-ninja-blog
```

### 2. Create a Virtual Environment

Create and activate a virtual environment to isolate project dependencies.

```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies

Install all required packages using `pip`.

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the source directory (`src`) and add the following:

```bash
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True  # Set to False in production
DATABASE_URL=your_database_url  # Leave empty for SQLite
CORS_ALLOWED_ORIGINS=your_cors_allowed_origins  # Comma-separated list
```

---

## Database Migrations

Handle database schema changes with the following commands:

### 1. Apply Database Migrations

Set up the database schema by making and applying migrations.

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Running the Server

Start the Django development server to make the API available for use.

```bash
python manage.py runserver
```

Once the server is running, the API will be available at:

**URL**: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

API Docs will be available at:

**URL**: [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)

---

## User Management

Manage users using Django's built-in admin interface and custom management commands.

### Create a Superuser

Create an admin user to access the Django admin panel.

```bash
python manage.py createsuperuser
```

### Create Sample Users

Generate 10 sample users for testing purposes.

```bash
python manage.py create_sample_users
```

---

## Generating Sample Data

You can generate sample blog posts and comments for testing purposes using custom management commands.

### Create Sample Blog Posts

Generate a specified number of sample blog posts using existing users.

```bash
python manage.py create_sample_posts 10
```

### Create Sample Comments

Generate a specified number of sample comments for existing blog posts.

```bash
python manage.py create_sample_comments 10
```

---

## Using the API

### Authentication

Obtain JWT tokens for user authentication.

```bash
rav login
```

### API Endpoints

#### Authentication

- **POST** `/api/token/pair`: Obtain JWT tokens for authentication.

#### Blog Posts Endpoints

- **POST** `/api/posts/`: Create a new blog post.
- **GET** `/api/posts/`: List all blog posts (supports pagination).
- **GET** `/api/posts/{post_id}`: Retrieve a specific blog post.
- **PUT** `/api/posts/{post_id}`: Update an existing blog post.
- **DELETE** `/api/posts/{post_id}`: Delete a blog post.

#### Comments Endpoints

- **POST** `/api/comments/`: Create a new comment on a blog post.
- **GET** `/api/comments/post/{post_id}`: List comments for a specific post (supports pagination).
- **GET** `/api/comments/{comment_id}`: Retrieve a specific comment.
- **PUT** `/api/comments/{comment_id}`: Update an existing comment.
- **DELETE** `/api/comments/{comment_id}`: Delete a comment.

---

## Scripts and Automation

This project uses a custom `rav.yaml` file for script automation. Below are some useful commands:

### Commands Overview

- **Initialize Project**:
  ```bash
  rav init
  ```
- **Install Dependencies**:
  ```bash
  rav installs
  ```
- **Run Server**:
  ```bash
  rav server
  ```
- **Make Migrations**:
  ```bash
  rav makemigrations
  ```
- **Migrate Database**:
  ```bash
  rav migrate
  ```
- **Create Superuser**:
  ```bash
  rav su
  ```
- **Generate Sample Posts**:
  ```bash
  rav posts
  ```
- **Generate Sample Comments**:
  ```bash
  rav comments
  ```
- **Clean Project**:
  ```bash
  rav clean
  ```
- **List All Commands**:
  ```bash
  rav list
  ```

## Logging Configuration

Logs are stored in `logs/BlogApi.log`. You can configure logging settings in the `settings.py` file.

### File Logging

- **Logs API requests and errors** to `logs/BlogApi.log`.

### Console Logging

- **Logs to the console** for easier debugging during development.

---

## Contributing

We welcome contributions! Follow these steps to contribute to the project:

1. **Fork** the project.
2. **Create** your feature branch:
   ```bash
   git checkout -b my-new-feature
   ```
3. **Commit** your changes:
   ```bash
   git commit -am 'Add some feature'
   ```
4. **Push** to the branch:
   ```bash
   git push origin my-new-feature
   ```
5. **Submit** a pull request.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or feedback, please reach out to **Nana B** on Twitter at [@koboateng](https://twitter.com/koboateng).

---

End of Documentation.
