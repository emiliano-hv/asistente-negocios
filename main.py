from fastapi import FastAPI, Request
import os

app = FastAPI()

@app.get("/")
def home():
  return {"status": "Bot prendido"}

@app.post("/webhook)
          async def webhook(req: Request):
          data = await req.json()
          print(data)
          return {"ok": True}

if __name__ == "__main__":
          import uvicorn
          uvicorn.run(app, host="0.0.0.0",
                     port=int(os.environ.get("PORT", 8000)))
