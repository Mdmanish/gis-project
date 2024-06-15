# Django GIS Application

This Django project implements a Geographic Information System (GIS) with spatial database capabilities using Django's built-in GIS features and the Django REST Framework for API endpoints.

## Installation

To run this project locally, follow these steps:

1. Clone the repository
	```
	git clone <repository-url>
	```

2. Navigate to the project directory:

    ```bash
    cd project-directory
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Run migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Run below command to transform the data from csv file to database

	```
	python manage.py load_locations
	```

8. Start the development server:

    ```bash
    python manage.py runserver
    ```

## Endpoints

### User Management

- `POST /register/`: Register a new user.
  - Payload:
    ```json
    {
      "username": "newuser",
      "email": "newuser@example.com",
      "password": "password123"
    }
    ```
- `POST /login/`: Login an existing user.
  - Payload:
    ```json
    {
      "username": "existinguser",
      "password": "existingpassword"
    }
    ```

### Location Management

- `GET /api/locations/`: List all locations.
- `POST /api/locations/`: Create a new location.
  - Payload:
    ```json
    {
      "name": "New Location",
      "description": "Description of the new location",
      "coordinates": {
        "type": "Point",
        "coordinates": [longitude, latitude]
      }
    }
    ```
- `GET /api/locations/<int:pk>/`: Retrieve a specific location.
- `PUT /api/locations/<int:pk>/`: Update a specific location.
  - Payload (partial update):
    ```json
    {
      "name": "New Location",
      "description": "Description of the new location",
      "coordinates": {
        "type": "Point",
        "coordinates": [longitude, latitude]
      }
    }
    ```
- `DELETE /api/locations/<int:pk>/`: Delete a specific location.

### Boundary Management

- `GET /api/boundaries/`: List all boundaries.
- `POST /api/boundaries/`: Create a new boundary.
  - Payload:
    ```json
    {
      "name": "New Boundary",
      "area": {
        "type": "Polygon",
        "coordinates": [[
          [longitude1, latitude1],
          [longitude2, latitude2],
          [longitude3, latitude3],
          [longitude1, latitude1]
        ]]
      }
    }
    ```
- `GET /api/boundaries/<int:pk>/`: Retrieve a specific boundary.
- `PUT /api/boundaries/<int:pk>/`: Update a specific boundary.
  - Payload (partial update):
    ```json
    {
      "name": "New Boundary",
      "area": {
        "type": "Polygon",
        "coordinates": [[
          [longitude1, latitude1],
          [longitude2, latitude2],
          [longitude3, latitude3],
          [longitude1, latitude1]
        ]]
      }
    }
    ```
- `DELETE /api/boundaries/<int:pk>/`: Delete a specific boundary.

### Additional Functionality

- `POST /api/locations/distance/`: Calculate distance between two locations.
  - Payload:
    ```json
    {
      "location1_id": 1,
      "location2_id": 2
    }
    ```
- `POST /api/locations/within_boundary/`: Check if a location is within a specified boundary.
  - Payload:
    ```json
    {
      "location_id": 1,
      "boundary_id": 1
    }
    ```

### Frontend View

- `/`: Home page displaying locations, boundaries and UI for distance calculation and boundary checking feature.
