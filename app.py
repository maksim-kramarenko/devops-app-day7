from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from DevOps app via Docker & CI/CD!"

if __name__ == "__main__":
    # слушаем на всех интерфейсах, порт 8000
    app.run(host="0.0.0.0", port=8000)
