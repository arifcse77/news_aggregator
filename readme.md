# Django News Aggregator
A Django-based news aggregation system with REST API and web interface.

## Features

* RSS feed aggregation with automatic updates
* Topic extraction using OpenAI GPT-3.5 with spaCy fallback
* Named Entity Recognition
* REST API for accessing articles and sources
* Web dashboard for monitoring
* Celery-based background tasks
* Postgre

## Setup & Run project

### 1. Navigate to your project directory:
    cd news_aggregator

### 2. Create a virtual environment:
    python3 -m venv venv

### 3. Activate the virtual environment:
    source venv/bin/activate

### 4. Install the requirements:
    pip install -r requirements.txt 

### 5. Install spaCy's English language model:
    python -m spacy download en_core_web_sm

### 6. Make and apply migrations:
    python manage.py makemigrations
    python manage.py migrate   

### 7. Create a superuser:
    python manage.py createsuperuser

### 7. Start the development server:
    python manage.py runserver

### 8. In a separate terminal (with virtualenv activated), start Celery:
    celery -A news_aggregator worker -l info

### 9. In another terminal (with virtualenv activated), start Celery Beat:
    celery -A news_aggregator beat -l info


#### Now your Django news aggregator should be up and running! You can access:

* Admin interface at http://localhost:8000/admin/
* Dashboard at http://localhost:8000/
* API at http://localhost:8000/api/