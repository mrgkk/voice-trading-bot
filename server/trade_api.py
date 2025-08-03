# trade_api.py - Flask app for MT5 execution
import configparser
import os
from flask import Flask, request, jsonify
import MetaTrader5 as mt5
import logging

app = Flask(__name__)
API_KEY = "YourSecureApiKeyHere"

# Setup logging
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Load config from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

MT5_LOGIN = int(config.get("MT5", "login"))
MT5_PASSWORD = config.get("MT5", "password")
MT5_SERVER = config.get("MT5", "server")
MT5_PATH = config.get("MT5", "path")

@app.route("/trade", methods=["POST"])
def trade():
    data = request.json or {}
    if data.get("api_key") != API_KEY:
        logging.warning("Unauthorized access attempt.")
        return jsonify({"error": "unauthorized"}), 403

    action = data.get("action")
    volume = float(data.get("volume", 0))
    symbol = data.get("symbol", "XAUUSD")

    if not mt5.initialize(path=MT5_PATH, login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
        logging.error(f"MT5 initialization failed: {mt5.last_error()}")
        return jsonify({"error": "MT5 init failed"}), 500

    result = None
    if action in ("buy", "sell"):
        order_type = mt5.ORDER_TYPE_BUY if action=="buy" else mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).ask if action=="buy" else mt5.symbol_info_tick(symbol).bid
        request_params = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "deviation": 10,
            "magic": 20250803,
            "comment": "VoiceCmd",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }
        result = mt5.order_send(request_params)
        logging.info(f"{action.upper()} {volume} {symbol} → {result.retcode}")
    elif action == "exit":
        positions = mt5.positions_get(symbol=symbol) or []
        for pos in positions:
            tp = pos.type
            close_type = mt5.ORDER_TYPE_SELL if tp==mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
            price = (mt5.symbol_info_tick(symbol).bid if close_type==mt5.ORDER_TYPE_SELL
                     else mt5.symbol_info_tick(symbol).ask)
            mt5.order_send({
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": pos.volume,
                "type": close_type,
                "position": pos.ticket,
                "price": price,
                "deviation": 10,
                "magic": 20250803,
                "comment": "VoiceExit",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC
            })
        logging.info("All positions closed.")
    else:
        logging.error("Invalid action.")
        return jsonify({"error": "invalid action"}), 400

    mt5.shutdown()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)