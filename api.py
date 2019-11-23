from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.routing import Route
import uvicorn


templates = Jinja2Templates(directory='templates')




async def homepage(request):
    if request.method == 'GET':
        template = "index.html"
        context = {"request": request}
        return templates.TemplateResponse(template, context)
    elif request.method == 'POST':
        form = await request.form()
        print(form)
        print(form.getlist('file'))
        for uploadFile in form.getlist('file'):
            print(uploadFile.filename)
            print(uploadFile.content_type)
            with open('uploads/'+uploadFile.filename,'wb') as f:
                f.write(await uploadFile.read())


        return JSONResponse("wrote body to file")

routes = [Route('/',endpoint=homepage,methods=['GET','POST'])]
app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run("api:app", host='0.0.0.0', port=80, reload='true')
