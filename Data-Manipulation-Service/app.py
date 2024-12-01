from flask import Flask
from routes import data_manipulation_bp

app = Flask(__name__)

app.register_blueprint(data_manipulation_bp)

@app.route("/")
def home():
    return "This is the API of ML model"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
