from flask import Flask, render_template, request, jsonify
from chatbot_model import get_bot_response
from db_config import get_db_connection

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    bot_reply = get_bot_response(user_message)

    # Save chat to db
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_logs (user_message, bot_response) VALUES (%s, %s)",
        (user_message, bot_reply)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
