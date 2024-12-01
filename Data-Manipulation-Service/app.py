from flask import Flask
from routes import data_manipulation_bp
from flask_cors import CORS 


app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])


app.register_blueprint(data_manipulation_bp)

@app.route("/")
def home():
    return "This is the API of ML model"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
