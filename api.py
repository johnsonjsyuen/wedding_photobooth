from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
import uvicorn

app = Starlette(debug=True)


@app.route('/')
async def homepage(request: Request):
    return JSONResponse({'hello': 'world'})


@app.route('/upload')
async def upload_photo(request: Request):
    body = await Request.body()
    with open('test', 'w') as f:
        f.write(body)
    return JSONResponse("wrote body to file")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8888, loop='uvloop', workers=4)
