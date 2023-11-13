import signal
import requests
from flask import Flask, request

app = Flask(__name__)
bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
admin_chat_id = "YOUR_ADMIN_CHAT_ID"
user_chat_ids = set()
banned_users = set()

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    requests.post(url, json=params)

def forward_message(from_chat_id, message_id):
    for chat_id in user_chat_ids:
        url = f"https://api.telegram.org/bot{bot_token}/forwardMessage"
        params = {"chat_id": chat_id, "from_chat_id": from_chat_id, "message_id": message_id}
        requests.post(url, json=params)

def handle_shutdown(signum, frame):
    print("Received signal {}, shutting down gracefully...".format(signum))
    # Perform any necessary cleanup or save state before shutting down
    exit(0)

# Register the signal handler
signal.signal(signal.SIGTERM, handle_shutdown)

@app.route(f"/{bot_token}", methods=["POST"])
def handle_updates():
    update = request.get_json()

    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        user_id = message["from"]["id"]

        if user_id in banned_users:
            return "You are banned."

        if "text" in message:
            text = message["text"]

            if text.startswith("/ban"):
                banned_users.add(user_id)
                send_message(chat_id, "You have been banned.")
            elif text.startswith("/broadcast"):
                broadcast_text = text.split("/broadcast ", 1)[1]
                for user in user_chat_ids:
                    send_message(user, broadcast_text)
            else:
                forward_message(chat_id, message["message_id"])

        elif "photo" in message:
            # Handle media messages
            forward_message(chat_id, message["message_id"])

        if chat_id != admin_chat_id:
            user_chat_ids.add(chat_id)

    return "OK"

if __name__ == "__main__":
    app.run(port=5000)
