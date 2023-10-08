
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form, responses
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
import instagramscraper as isp
import relation_to_json as rel

import json

def read_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_item(request: Request):
    filename = {'name': 'relations2.json'}
    return templates.TemplateResponse("graph.html", {"request": request,
                                                       'filename': filename})


@app.get("/Communities")
async def homepage(request: Request):
    filename = {'name': 'relations2.json'}
    return templates.TemplateResponse("graph.html", {"request": request,
                                                     'filename': filename})


@app.get("/influence")
async def homepage(request: Request):
    filename = {'name': 'relations2.json'}
    return templates.TemplateResponse("graph.html", {"request": request,
                                                     'filename': filename})


@app.get("/tagshow")
async def homepage(request: Request):
    filename = {'name' : 'tagralation3.json'}
    return templates.TemplateResponse("tagshow.html", {"request": request,
                                                       'filename' : filename})

@app.get("/tagshowcluster")
async def homepage(request: Request):
    filename = {'name': 'tag_relations_louvain3.json'}
    return templates.TemplateResponse("tagshow.html", {"request": request,
                                                              'filename' : filename})



@app.get("/showtagwords", response_class=HTMLResponse)
async def read_item(request: Request):
    twoword = read_json_file('trendtags/trendtag2word15_5.json')
    trend = read_json_file('trendtags/trendtags_15.json')
    oneword = read_json_file('trendtags/trendtagword15_5.json')
    return templates.TemplateResponse("displaydic.html", {"request": request,
                                                          "twoword": twoword,
                                                          "trend": trend,
                                                          "oneword": oneword,
                                                          })


@app.get("/showtagsentiment", response_class=HTMLResponse)
async def read_item(request: Request):
    tagsent = read_json_file('trendtags/trendtagsentiment_15.json')
    trend = read_json_file('trendtags/trendtags_15.json')
    return templates.TemplateResponse("displaytagsent.html", {"request": request,
                                                          "tagsent": tagsent,
                                                          "trend" : trend})

@app.get("/linkpredict")
async def homepage(request: Request):
    linkp = read_json_file('trendtags/similarity_30.json')
    return templates.TemplateResponse("link.html", {"request": request,
                                                              "linkp": linkp})



app.mount("/static", StaticFiles(directory="assets\css"), name="static")

app.mount("/js", StaticFiles(directory="assets\js"), name="js")

app.mount("/images", StaticFiles(directory="assets\imgs"), name="images")
app.mount("/userimage", StaticFiles(directory="instagramuser"), name="userimage")

app.mount("/statichtml", StaticFiles(directory="02 visual"), name="statichtml")



@app.get("/form")
async def homepage(request: Request):
    '''
        #Currently not used
        HTML form with fields 'name' , 'gender' , 'age'
        and with pressing the button POST them
    '''
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/form")
async def form_submit(request: Request, name: str = Form(...), gender: str = Form(...), age: int = Form(...)):
    '''
        #Currently not used
        recive 'name' , 'gender' , 'age' from the HTML and return JSON
    '''
    form_data = {"name": name, "gender": gender, "age": age}
    return form_data



import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)