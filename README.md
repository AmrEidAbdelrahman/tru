# Egyptian National ID Validator API

## Overview
This project provides an API to validate and extract information from Egyptian national IDs. It uses Django, Django REST Framework, and API key authentication.

## Features
- Validate Egyptian national IDs
- Extract birthdate, governorate code, and gender
- API key authentication
- Rate limiting
- API call logging

## Running with Docker

1. **Build the Docker image:**
   ```sh
   docker build -t national-id-api .
   ```
2. **Run migrations:**
   ```sh
   docker run --rm -v $(pwd):/app national-id-api python manage.py migrate
   ```
3. **Create a superuser (optional, for admin):**
   ```sh
   docker run --rm -it -v $(pwd):/app national-id-api python manage.py createsuperuser
   ```
4. **Run the server:**
   ```sh
   docker run -p 8000:8000 -v $(pwd):/app national-id-api
   ```

## Running with Docker Compose

1. **Build and start the services:**
   ```sh
   docker-compose up --build
   ```
2. **Run migrations:**
   In a new terminal, run:
   ```sh
   docker-compose run web python manage.py migrate
   ```
3. **Create a superuser (optional, for admin):**
   ```sh
   docker-compose run web python manage.py createsuperuser
   ```
4. **Access the API:**
   Visit [http://localhost:8000/api/validate-id/](http://localhost:8000/api/validate-id/) or the admin at [http://localhost:8000/admin/](http://localhost:8000/admin/)

## API Usage
- Endpoint: `POST /api/validate-id/`
- Headers: `Authorization: Api-Key <your-api-key>`
- Body:
  ```json
  { "national_id": "29001011234567" }
  ```

## Notes
- API keys can be created via the Django admin at `/admin/`.
- All API calls are logged in the database. 
