Find Movies with AI
=================================================

This is a semantic search service for movies based on a query. For example, "great fictional beautiful animals." should return a list of movies such as "Madagascar 3: Europe's Most Wanted", "Zoology" and so on.

This is based on the Vector Search provided by DataStax on its Cassandra database.

The plot of a movie was converted into a vector (embedding vector) and stored in the database which was customized with an index to calculate the nearest distance between vectors.

The converting service is provided by CO.HERE.

When a user inputs a query, the string is converted into a vector and used to find the closest search in the database.

More details will be updated soon once everything is settled.

Demo here: https://find-movies.com/