import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "Status": "Success",
        "Message": "Guerrout"
    }

if __name__ == '__main__':
    uvicorn.run(f"main:app", host="127.0.0.1", port=8888, reload=True)