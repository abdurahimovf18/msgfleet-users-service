import uvicorn

def main():
    uvicorn.run("src.users_service.main:app", host="127.0.0.1", port=8001, reload=True)
