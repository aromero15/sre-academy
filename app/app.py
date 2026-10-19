from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.get("/api/data")
def data():
    return jsonify({"message": "Hola desde GitHub Actions"}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
