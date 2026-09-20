from app.main import app

if __name__ == "__main__":
    import uvicorn

    from config import API_HOST, API_PORT

    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=False)


