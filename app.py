import os
import requests
import json
from flask import Flask, request, jsonify, render_template_string

API_KEY = "AIzaSyBZSS942Zn7FP_nBctj57LOhah5jUXNhbc"  # replace with your Gemini API key

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {"Content-Type": "application/json"}

def ask_gemini(prompt):
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "No response"
    else:
        return f"Error {response.status_code}: {response.text}"

# Flask App
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Gemini Chatbot</title>
</head>
<body style="font-family: Arial; margin: 20px;">
    <h2>Gemini Chatbot</h2>
    <div id="chatbox" style="border:1px solid #ccc; padding:10px; height:300px; overflow-y:scroll;"></div>
    <input type="text" id="userInput" style="width:80%;" placeholder="Type a message...">
    <button onclick="sendMessage()">Send</button>

    <script>
        async function sendMessage() {
            let input = document.getElementById("userInput");
            let chatbox = document.getElementById("chatbox");
            let userText = input.value;
            if (!userText) return;

            chatbox.innerHTML += "<b>You:</b> " + userText + "<br>";
            input.value = "";

            let response = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({message: userText})
            });

            let data = await response.json();
            chatbox.innerHTML += "<b>Gemini:</b> " + data.reply + "<br>";
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    reply = ask_gemini(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
