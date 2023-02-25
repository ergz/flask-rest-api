Single-database configuration for Flask.


## Run locally

to run this locally you will need to run the docker container and mount the 

`docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-rest-api sh -c "flask run --host 0.0.0.0"`

here is what each of the flags above do:

* `-d` run in dettached
* `-p` map port from:to
* `-w` set working dir
* `-v` mount volume 

