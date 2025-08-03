# config.py - Remote desktop configuration
# List up to 10 clients
REMOTE_SERVERS = [
    {"id": "Client 1", "host": "192.168.29.133", "port": 5000},
    {"id": "Client 2", "host": "192.168.1.102", "port": 5000},
    # add more up to Client 10...
]

# Shared secret for REST calls
API_KEY = "YourSecureApiKeyHere"
API_ENDPOINT = "http://192.168.29.133:5000/trade"

