from flask import Flask
from routes import data_collection_bp
from flask_cors import CORS 


app = Flask(__name__)
CORS(app)

# Blueprint regisztrálása
app.register_blueprint(data_collection_bp)

@app.route("/")
def home():
    return "Welcome to the Weather API Service!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
