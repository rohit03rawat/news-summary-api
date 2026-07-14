from flask import Flask

app = Flask(__name__)

@app.get("/")
def health():
    return "Celery worker is alive!"

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)