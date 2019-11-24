from typing import Dict, Union
from starlette.applications import Starlette
from starlette.middleware.gzip import GZipMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.routing import Route, Mount
import aiofiles
import uvicorn


templates = Jinja2Templates(directory='templates')

DESTINATION_FOLDER = 'uploads/'
ALLOWED_MIME_TYPES = ['image/jpeg','image/pjpeg','image/heif','image/heic']

def index_template(context: Dict[str,Union[Request,int]]):
    template = "index.html"
    return templates.TemplateResponse(template, context)

async def homepage(request: Request) -> Response:
    if request.method == 'GET':
        context = {"request": request, "files_uploaded":0}

    elif request.method == 'POST':
        form = await request.form()
        successful_uploads = 0
        for uploadFile in form.getlist('file'):
            if uploadFile.content_type in ALLOWED_MIME_TYPES:
                async with aiofiles.open(DESTINATION_FOLDER+uploadFile.filename,'wb') as f:
                    await f.write(await uploadFile.read())
                    successful_uploads += 1

        context = {"request": request, "files_uploaded":successful_uploads}
    
    return index_template(context)

routes = [Route('/',endpoint=homepage,methods=['GET','POST']),
          Mount('/static', StaticFiles(directory='statics'), name='static')]
app = Starlette(debug=True, routes=routes)
app.add_middleware(GZipMiddleware)   

if __name__ == "__main__":
    uvicorn.run("api:app", host='0.0.0.0', port=80, reload='true')
