#Stylight - PAM Challenge

The Challenge
-------------

> Create a simple HTTP API to insert, read and aggregate timeseries data.

The final API must respect the [Open API](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md) spec provided in `spec.yml`.

You are free to use any backend stack (language, server framework, libraries, datastore, etc.) you want, however we have a strong preference for Python as it our main backend language.

Ideally, the service should be as close to ready to run / deploy as possible:

- You should provide a way to start the API and any related process(es) with one single shell command. (Shell script, Python script, etc.).
- You can also provide a setup script or instructions for runtime and dependencies such as node+npm / python+pip as long it is not too complex (i.e. We will not manually setup & compile your custom http stack from scratch unless you package it).
- The software should run on Linux machines (ideally Mac OS as well but that's not strictly required)
- Feel free to use docker or similar technology to abstract any setup / dependency logic as you would in production

# HOW TO RUN
1. Clone the repo and do 
    2. pip install -r requirements.txt && python app.py
    3. pip install -r requirements.txt && ./gunicorn.sh

2. For docker fans
    2. docker pull ishanbhatt/stylight:dev
    3. docker run -dit --name stylight_dev -p 5200:5200 ishanbhatt/stylight:dev   
    
# Testing
Hit http://localhost:5200 to access all the apis(swagger urls)
You can also hit curl request to the same url.
 