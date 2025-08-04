import requests
from config import REMOTE_SERVERS, API_KEY
from command_parser import parse_command

# Settings
#SERVER_URL = "http://192.168.29.133:5000/trade"  # Your Flask server
API_KEY = "YourSecureApiKeyHere"  # Match the value in your trade_api.py

def main():
    print("💬 Text Command Mode (type 'b', 's', or 'e' to exit; 'q' to quit)")

    while True:
        user_input = input("Enter command: ").strip().lower()

        if user_input == 'q':
            print("👋 Quitting text command bot...")
            break

        command = parse_command(user_input)
        if command:
            command["api_key"] = API_KEY

            # 🚀 Send to all configured remote servers
            for client in REMOTE_SERVERS:
                url = f"http://{client['host']}:{client['port']}/trade"
                print(f"➡️ Sending to {client['id']} → {url} → {command}")
                try:
                    response = requests.post(url, json=command, timeout=10)
                    print(f"✅ {client['id']} responded: {response.text}")
                except Exception as e:
                    print(f"❌ Error sending to {client['id']}: {e}")
        else:
            print("⚠️ Invalid command. Type 'b', 's', or 'exit'.")

if __name__ == "__main__":
    main()
