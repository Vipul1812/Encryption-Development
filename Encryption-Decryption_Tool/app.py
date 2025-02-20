from flask import Flask, render_template, request
from cryptography.fernet import Fernet

app = Flask(__name__)

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        operation = request.form.get("operation")
        if operation == "Encrypt":
            key = generate_key()
            message = request.form.get("message")
            encrypted_message = encrypt_message(message, key)
            return render_template("index.html", encrypted_message=encrypted_message.decode(), key=key.decode(), operation=operation)
        elif operation == "Decrypt":
            key = request.form.get("key")
            encrypted_message = request.form.get("encrypted_message")
            try:
                decrypted_message = decrypt_message(encrypted_message.encode(), key.encode())
                return render_template("index.html", decrypted_message=decrypted_message, operation=operation)
            except Exception as e:
                return render_template("index.html", error=str(e), operation=operation)
    return render_template("index.html")

@app.errorhandler(405)
def method_not_allowed(e):
    return "Method Not Allowed", 405

if __name__ == "__main__":
    app.run(debug=True)
