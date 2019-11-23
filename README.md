# Wedding Photobooth

## Motivation
This was used as a simple upload server for wedding guests to send their photos to a computer connected to a photo printer.

## Tech Stack
This uses Starlette, a Python ASGI (Asynchronous Server Gateway Interface, the standard Python Asynchronous server interface) framework to render a HTML template providing a file upload function. Static assets are under the statics directory and Jinja2 is used for templating.

The API of Starlette is similar to Flask.

The form POSTs back the files and they are written to a designated folder.

Uvicorn is used to serve this site.

## Usage
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python api.py
```