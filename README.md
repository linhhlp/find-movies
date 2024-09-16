# Find Movies with AI

This is a semantic search service for movies based on a query. For example, "great fictional beautiful animals." should return a list of movies such as "Madagascar 3: Europe's Most Wanted", "Zoology" and so on.

This is based on the Vector Search provided by DataStax on its Cassandra database.

The plot of a movie was converted into a vector (embedding vector) and stored in the database which was customized with an index to calculate the nearest distance between vectors.

The converting service is provided by CO.HERE.

When a user inputs a query, the string is converted into a vector and used to find the closest search in the database.

## Detail of Work

The details of the conversion and lookup functions are provided here https://github.com/linhhlp/Machine-Learning-Applications/tree/main/Text-2-Vect-Vector-Search

## Database

The database used in this application is uploaded to Kaggle: https://www.kaggle.com/datasets/linhhlp/35k-movies-with-embedded-plots-to-vectors

## Credentials

To provide credentials to the services of CO.HERE AI and Cassandra by DataStax, the credentials must be stored in the `cred.py` file.
There is a template file called `cred-template.py` that contains the examples of credentials. Rename this template file to `cred.py` after that.

## Containerization

With the provided Dockerfile, the container can be built with Docker.

```bash
$ docker image build -t "find_movies" .

$ docker run -d -p 80:80 find_movies
```

## Logging

To investigate the app and the usage of users, I made a simple logging tool to save a basic data into Cassandra. If you do not want it, just remove it from `app.py`

## Demo 

The service is running on: [findmovies.linhhlp.com/](https://findmovies.linhhlp.com/)

The service was deployed on AWS Lambda using [zappa](https://github.com/zappa/Zappa). The process of deployment is very simple and straightforward with `zappa`. However, there are some issues with Zappa including do not upload zip files. 

## Deploy to a Domain with AWS Lambda

Follow this guide for more information: https://github.com/zappa/Zappa#deploying-to-a-domain-with-aws-certificate-manager
