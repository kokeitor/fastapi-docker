from fastapi import FastAPI


app = FastAPI()


@app.get('/health')
def hello_world():
    return {'response': 'Hello World'}
