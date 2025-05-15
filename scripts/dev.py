import uvicorn

def main():
    uvicorn.run("src.auto_mailing_backend.main:app", host="127.0.0.1", port=8000, reload=True)
