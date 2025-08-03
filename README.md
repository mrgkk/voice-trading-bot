# Voice-Controlled MT5 XAUUSD Trader

## Overview
Use voice commands from your laptop to execute XAUUSD trades on up to 10 remote MT5 instances.

## Features
- 🎙️ Voice-to-text using Google Speech API
- ⚙️ Command parsing for buy/sell/exit
- 🌐 REST API for remote trade execution
- 🔒 API-key authentication
- 🧪 Logging and error handling

## Setup

### 1. Clone & Structure
Create folders:
voice-trading-bot/
├── client/
├── server/
└── README.md

⚙️ Step-by-step Guide to Run Locally
1. 📌 Install Python 3.9+ (if not already)
Ensure you have Python 3.9+ installed. You can check using:

bash
Copy
Edit
python --version
2. 🛠️ Set Up the Server (MT5 API)
a. Open a terminal and go to the server/ folder:
bash
Copy
Edit
cd voice-trading-bot/server
b. Create a virtual environment (optional but recommended):
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
c. Install server dependencies:
bash
Copy
Edit
pip install -r requirements.txt
d. Run the server:
bash
Copy
Edit
python trade_api.py
You should see:

csharp
Copy
Edit
 * Running on http://127.0.0.1:5000
3. 🎤 Set Up the Client (Voice Recognition)
a. Open another terminal and go to the client/ folder:
bash
Copy
Edit
cd voice-trading-bot/client
b. Activate the same or a new virtual environment:
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
c. Install client dependencies:
bash
Copy
Edit
pip install -r requirements.txt
d. Configure config.py:
Edit the file:

python
Copy
Edit
API_ENDPOINT = "http://127.0.0.1:5000/trade"
e. Run the client:
bash
Copy
Edit
python main.py
You'll be prompted to speak a voice command like:

arduino
Copy
Edit
"buy gold 0.5" or "sell gold 1.0" or "exit"
📦 Example Voice Commands
Say one of the following when prompted:

"buy gold 0.5"

"sell gold 1.0"

"exit" (closes all XAUUSD positions)

🔍 Behind the Scenes
The client captures your voice, converts it to text, parses the command, and sends a REST API call to the local server.

The server receives the command and executes it on your local MetaTrader 5 terminal (make sure it’s open and logged in).

### Using solution using Remote machines
Below is a complete end-to-end setup guide for using the voice-to-MT5 trading solution with multiple remote desktops, as well as locally for testing. This includes:

✅ Local testing (already explained above)

🌐 Multi-client setup using Remote Desktops

🧠 Design overview

🛡️ Security tips

🧪 Voice commands to use

📁 Folder structure and files

🧠 Architecture Overview
scss
Copy
Edit
        🎙️ Voice Client (Local Laptop)
               │
        REST API Call (HTTP POST)
               ↓
        🌐 Remote Desktop(s) (MT5 Running)
      ┌──────────────┬──────────────┬──────────────┐
      │   Server A   │   Server B   │   Server C   │
      │ trade_api.py │ trade_api.py │ trade_api.py │
      │   + MT5      │   + MT5      │   + MT5      │
      └──────────────┴──────────────┴──────────────┘
🧪 Step 1: Test Locally (on one machine)
Refer to the previous answer to test the client and server on the same machine.

🌐 Step 2: Set Up Remote Desktop(s) to Receive Commands
Each remote desktop machine will run:

MetaTrader 5 terminal (logged in to broker account, with AutoTrading enabled).

trade_api.py server running with proper MetaTrader5 Python integration.

🖥️ On each Remote Machine:
a. ✅ Install Requirements
Install Python 3.9+

Install MT5 terminal

Open MT5 and make sure you're logged in and AutoTrading is enabled.

Run these commands:

bash
Copy
Edit
git clone https://github.com/mrgkk/voice-mt5-xauusd-trader.git
cd voice-trading-bot/server
pip install -r requirements.txt
b. 🛠️ Allow Port 5000 in Windows Defender
Open port 5000 for inbound TCP on Windows Firewall or any firewall software.

c. ▶️ Run the Flask Server
bash
Copy
Edit
python trade_api.py
Keep this running. It starts a REST API on:

bash
Copy
Edit
http://<remote-ip>:5000/trade
🎙️ Step 3: Set Up Client (Voice Control)
You can run the client (main.py) on your laptop.

a. Add Remote IPs to config.py (on your laptop):
python
Copy
Edit
# client/config.py
CLIENTS = [
    "http://192.168.1.101:5000/trade",
    "http://192.168.1.102:5000/trade",
    "http://192.168.1.103:5000/trade"
]
Replace 192.168.1.x with the actual public or private IPs of your remote desktops.

If you only want to trade for one:

python
Copy
Edit
CLIENTS = ["http://192.168.1.101:5000/trade"]
b. Use Voice Commands
In your terminal:

bash
Copy
Edit
cd client
python main.py
Speak a command when prompted:

"buy gold 1" → sends buy command with 1 lot to all clients.

"sell gold 0.5" → sends sell command with 0.5 lot.

"exit" → closes all XAUUSD positions on all clients.

✅ Sample Voice Commands
Voice Command	Action
"buy gold 1"	Opens 1 lot XAUUSD buy order
"sell gold 0.5"	Opens 0.5 lot XAUUSD sell
"exit"	Closes all XAUUSD positions
"buy gold 0.3 for all clients"	Trades on all configured clients

🔒 Security Tips
Use authentication tokens or IP whitelisting to secure the API (Flask middleware).

For public IPs, use HTTPS via reverse proxy (e.g., NGINX + Certbot).

Use VPN or SSH tunnel if possible between local and remote machines.