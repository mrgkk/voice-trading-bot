# command_parser.py - Parses voice commands
import re

def parse_command(text: str):
    """
    Parses:
      - buy gold 0.5 for all clients
      - sell gold 1 for client 3
      - exit all
      - exit client 2
    Returns dict: {
      action: "buy"/"sell"/"exit",
      volume: float (only for buy/sell),
      target: "all" or client id string
    }
    """
    text = text.lower().strip()
    # EXIT commands
    m = re.match(r'exit(?: for)?(?: all clients| all)?', text)
    if m:
        return {'action': 'exit', 'target': 'all'}

    m = re.match(r'exit(?: for)? client (\d+)', text)
    if m:
        return {'action': 'exit', 'target': f"Client {m.group(1)}"}

    # BUY/SELL commands
    m = re.match(r'(buy|sell) gold\s+([0-9]*\.?[0-9]+)(?:\s+for\s+(all clients|all|client\s+\d+))?', text)
    if m:
        action = m.group(1)
        volume = float(m.group(2))
        tgt = m.group(3) or "Client 1"
        tgt = tgt.replace("clients", "").replace("all", "all").strip()
        if tgt.lower().startswith("client"):
            tgt = tgt.title()  # e.g. "Client 3"
        else:
            tgt = "all"
        return {'action': action, 'volume': volume, 'target': tgt}

    return None
