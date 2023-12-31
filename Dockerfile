FROM ubuntu:latest
LABEL "Author"="Linh H"
LABEL version="1.0"
LABEL description="Find moives based on semantic search.\
  This demonstrates how to do vector search \
  with Astra DB in Cassandra"
RUN apt-get update \  
  && apt-get install -y python3.9 python3-pip \  
  && cd /usr/local/bin \  
  && ln -s /usr/bin/python3 python \  
  && pip3 install flask==2.0 gunicorn cassandra-driver db_dtypes cohere

COPY app.py utls.py cred.py secure-connect-movies-vector-search.zip.encrypt ./ 
COPY logtool.py ./ 
ADD templates templates
ADD static static

ENTRYPOINT ["gunicorn","app:app", "-b", "0.0.0.0:80"]