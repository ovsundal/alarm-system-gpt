# Alarm System GPT

### Build the project
`docker-compose build`

### Run the project
`docker-compose up`

### To run tests and linter:
`docker-compose run --rm app sh -c "python manage.py test && flake8"`

### To run a migration: 
`docker-compose run --rm app sh -c "python manage.py makemigrations"`

#### If package errors on docker-compose up, try 
`docker-compose up --build`

### View the API documentation
http://localhost:8000/api/docs/

### Chroma
To recreate the vector database for embeddings, simply delete the app/Chroma folder. To add new data sources, add the 
pdfs to the app/chat/services/background-knowledge folder and add them to the loader in FindInformationTool 
_setup_and_feed_database() method.