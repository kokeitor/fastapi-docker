from fastapi import FastAPI
import pathlib
from pydantic import BaseModel


class requestModel(BaseModel):
    text: str


app = FastAPI()


@app.post('/')
def hello_world(request: requestModel):

    path = pathlib.Path(__file__).parent.absolute()
    file_path = path / 'data' / 'data.txt'
    print(file_path)
    print(request.text)
    with open(file_path, 'w') as f:
        f.write(request.text)
    return {'response': f'Text : {request.text}'}
