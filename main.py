from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

VT = os.environ.get('VERIFY_TOKEN')
if not VT:
    VT = 'mi_token_secreto_123'
VERIFY_TOKEN = VT

WT = os.environ.get('WHATSAPP_TOKEN')
if not WT:
    WT = ''
WHATSAPP_TOKEN = WT

PID = os.environ.get('PHONE_NUMBER_ID')
if not PID:
    PID = ''
PHONE_NUMBER_ID = PID

@app.get('/')
def home():
    return {'status': 'Bot prendido'}

@app.get('/webhook')
def verify_webhook(request: Request):
    q = request.query_params
    mode = q.get('hub.mode')
    token = q.get('hub.verify_token')
    challenge = q.get('hub.challenge')
    ok1 = (mode == 'subscribe')
    ok2 = (token == VERIFY_TOKEN)
    if ok1 and ok2:
        return int(challenge)
    return {'error': 'Token invalido'}

@app.post('/webhook')
async def webhook(req: Request):
    data = await req.json()
    print(data)
    try:
        entry = data['entry'][0]
        change = entry['changes'][0]
        value = change['value']
        if 'messages' in value:
            msg = value['messages'][0]
            num = msg['from']
            txt = msg['text']['body']
            print(num, txt)
            out = 'Hola! Recibi: ' + txt
            send_message(num, out)
    except Exception as e:
        print(e)
    return {'ok': True}

def send_message(to, text):
    if not WHATSAPP_TOKEN:
        print('Falta token')
        return
    if not PHONE_NUMBER_ID:
        print('Falta phone id')
        return
    url = 'https://graph.facebook.com/'
    url = url + 'v21.0/'
    url = url + PHONE_NUMBER_ID
    url = url + '/messages'
    head = {}
    head['Authorization'] = 'Bearer ' + WHATSAPP_TOKEN
    head['Content-Type'] = 'application/json'
    body = {}
    body['messaging_product'] = 'whatsapp'
    body['to'] = to
    body['type'] = 'text'
    body['text'] = {'body': text}
    r = requests.post(url, headers=head, json=body)
    print(r.text)

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port)
