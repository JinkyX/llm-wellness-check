# Main Flask application entry point
from flask import Flask, request, render_template, send_file
from app.model_loader import load_model
from app.utils import process_csv
import os

app = Flask(__name__)
model = load_model()  # Load the local Mistral 7B Instruct model

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            upload_path = os.path.join("uploaded", file.filename)
            file.save(upload_path)
            output_file = process_csv(upload_path, model)
            return send_file(output_file, as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)