from flask import Flask

app = Flask(__name__)


@app.route("/trigger", methods=["GET"])
def trigger():
    print("Received trigger from ESP32")
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)