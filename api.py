from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.routing import Route, Mount
import uvicorn


templates = Jinja2Templates(directory='templates')




async def homepage(request):
    if request.method == 'GET':
        template = "index.html"
        context = {"request": request, "files_uploaded":0}
        return templates.TemplateResponse(template, context)
    elif request.method == 'POST':
        form = await request.form()
        print(form)
        print(form.getlist('file'))
        successful_uploads = 0
        for uploadFile in form.getlist('file'):
            print(uploadFile.filename)
            print(uploadFile.content_type)
            with open('uploads/'+uploadFile.filename,'wb') as f:
                f.write(await uploadFile.read())
                successful_uploads += 1



        template = "index.html"
        context = {"request": request, "files_uploaded":successful_uploads}
        return templates.TemplateResponse(template, context)


routes = [Route('/',endpoint=homepage,methods=['GET','POST']),
          Mount('/static', StaticFiles(directory='statics'), name='static')]
app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run("api:app", host='0.0.0.0', port=80, reload='true')
