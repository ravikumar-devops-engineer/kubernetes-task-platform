from flask import Flask,jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/api/tasks")
def tasks():
    return jsonify([
        {"id": 1, "title": "Learn kubernetes", "status": "completed"},
        {"id": 2, "title": "Build DevOps project", "status": "in-progress"},
        {"id": 3, "title": "Deploy with Helm", "status": "Pending"}
    ])

@app.route("/")
def home():
    return jsonify({
        "application": "kubernetes Task Platform",
        "version": "1.0"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)