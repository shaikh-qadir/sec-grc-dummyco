from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Simulated product list
PRODUCTS = [
    {"id": 1, "name": "AI Widget", "price": 19.99},
    {"id": 2, "name": "Smart Gadget", "price": 29.99},
]

@app.route("/")
def home():
    return "<h1>Welcome to DummyCo, Inc.!</h1><p>Your AI-powered storefront.</p>"

@app.route("/products")
def products():
    return jsonify(PRODUCTS)

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_message = data.get("message", "")
    answer = "Hello! I am DummyCo's AI assistant. How can I help you?"
    # Vulnerable: renders user input directly
    response_html = render_template_string(f"<p>User said: {user_message}</p><p>{{answer}}</p>")
    return response_html

if __name__ == "__main__":
    app.run(debug=True)