# main.py - Voice command recognition and API trigger
import speech_recognition as sr
import requests
import logging
from command_parser import parse_command
from config import REMOTE_SERVERS, API_KEY

logging.basicConfig(
    filename='client.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def send_to_server(server, payload):
    url = f"http://{server['host']}:{server['port']}/trade"
    try:
        resp = requests.post(url, json=payload, timeout=10)
        logging.info(f"{server['id']} → {resp.status_code}: {resp.text}")
        print(f"[{server['id']}] {resp.status_code}: {resp.text}")
    except Exception as e:
        logging.error(f"{server['id']} error: {e}")
        print(f"[{server['id']}] ERROR: {e}")

def dispatch_command(cmd_data):
    targets = []
    if cmd_data['target'] == 'all':
        targets = REMOTE_SERVERS
    else:
        # find matching ID
        for s in REMOTE_SERVERS:
            if s['id'].lower() == cmd_data['target'].lower():
                targets = [s]
                break
    if not targets:
        print("No matching client found.")
        return

    payload = {
        "api_key": API_KEY,
        "action": cmd_data['action'],
        "symbol": "XAUUSD",
        "volume": cmd_data.get('volume', 0)
    }

    for srv in targets:
        send_to_server(srv, payload)

def listen_loop():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("🎙️ Say command (e.g. “buy gold 0.5 for all”) or “exit” to quit.")
    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            if 'exit' == text.strip():
                print("Exiting.")
                break
            cmd = parse_command(text)
            if cmd:
                dispatch_command(cmd)
            else:
                print("❌ Command not recognized.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Speech API error: {e}")

if __name__ == "__main__":
    listen_loop()
