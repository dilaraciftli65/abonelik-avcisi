from fastapi import FastAPI

app = FastAPI(title="Abonelik Avcısı")


@app.get("/")
def root():
    return {"mesaj": "Abonelik Avcısı çalışıyor"}