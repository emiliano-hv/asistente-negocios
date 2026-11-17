from fastapi import FastAPI, Request
import os
import request

app = FastAPI()

VERIFY_TOKEN =
os.environ.get("VERIFY_TOKEN",
"mi_token_secreto_123")
WHATSAPP_TOKEN = 
os.environ.get("WHATSAPP_TOKEN","")
PHONE_NUMBRE_ID =
os.environ.get("PHONE_NUMBER_ID", "")

@app.get("/")
def home():
  return {"status": "Bot prendido"}

@app.get("/webhook")
def verify_webhook(request: Request):
  mode =
request.query_params.get("hub.mode")
  token =
request.query_params.get("hub.verify_token")
  challenge =
request.query_params.get("hub.challenge")
  if mode == "subscribe" and token ==
VERIFY_TOKEN:
        return int(challenge)
    return {"error": "Token invalido"}

@app.post("/webhook")
async def webhook(req: Request):
  data = await req.json()
  print(data)
  try:
    entry = data["entry"][0]
    change = entry["changes"][0]
    value = change["value"]
    if "messages" in value:
      msg = value["messages"][0]
      from_number = msg["from"]
      text = msg["text"]["body"]
      print (f"mensaje de {from_number}: {text}")
      send_message(from_number, f"Hola! Recibi tu mensaje: {text}")
  except Exception as e:
    print(f"Error: {e}")
    return {"ok": True}

def send_message(to, text):
  if not WHATSAPP_TOKEN or not
  PHONE_NUMBER_ID_:
    print("Falta WHATSAPP_TOKEN o PHONE_NUIMBER:ID")
    return
  url = f"https//graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
  headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "contentType": "application/json"}
  payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
  r = request.post(url,
  headers=headers, json=payload)
  print(r.text)

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0",
port=int(os.environ.get("PORT", 8000)))
