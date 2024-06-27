import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, field_validator, Field


class Params(BaseModel):
    language: str

app = FastAPI()


@app.post(
    '/set-params/',
    # context_callback=my_context_callback,
)
async def set_params(params: Params):
    pass


if __name__ == '__main__':
    uvicorn.run(app)