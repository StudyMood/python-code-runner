from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Python Code Runner Server is Running"

@app.route("/run", methods=["POST"])
def run_code():
    data = request.json
    code = data.get("code", "")
    user_input = data.get("input", "")

    with open("temp.py", "w", encoding="utf-8") as f:
        f.write(code)

    try:
        result = subprocess.run(
            ["python", "temp.py"],
            input=user_input,
            capture_output=True,
            text=True,
            timeout=5
        )

        # 🔥 ONLY LAST OUTPUT LINE (MOST SAFE)
        lines = [line for line in result.stdout.splitlines() if line.strip()]

        final_output = lines[-1] if lines else ""

        return jsonify({
            "output": final_output,
            "error": result.stderr
        })

    except Exception as e:
        return jsonify({
            "output": "",
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)
