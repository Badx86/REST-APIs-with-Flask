# REST_APIs_with_Flask
Build professional REST APIs with Python, Flask, Docker, Flask-Smorest, and Flask-SQLAlchemy


docker build -t flask-smorest-api .
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api
https://www.postman.com/galactic-shadow-150186/workspace/api/folder/24410479-2e60bb53-bda5-4ad2-8a67-e0e3cbfc2cdc