# recipe-app-api
Recipe API project

### Build the project
`docker-compose build`

### Run the project
`docker-compose up`

### To run tests and linter:
`docker-compose run --rm app sh -c "python manage.py test && flake8"`

### To run a migration: 
`docker-compose run --rm app sh -c "python manage.py makemigrations"`

### View the API documentation
http://localhost:8000/api/docs/