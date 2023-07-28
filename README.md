REST APIs with Python, Flask, Docker, Flask-Smorest, and Flask-SQLAlchemy

## How to work with this repository:

- Clone repository to your machine
- Navigate to the root folder of the project
- Create a virtual environment
- docker build -t flask-smorest-api .
- docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api
- flask db init -> flask db migrate -> flask db upgrade
- https://www.postman.com/galactic-shadow-150186/workspace/api/folder/24410479-2e60bb53-bda5-4ad2-8a67-e0e3cbfc2cdc
