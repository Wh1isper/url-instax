import os

from fastapi import FastAPI

PORT = int(os.environ.get("PORT", 7777))

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)  # noqa: S104
