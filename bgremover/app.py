from flask import Flask, render_template, request, jsonify
from rembg import remove
from PIL import Image
import io
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remove", methods=["POST"])
def remove_background():

    try:
        file = request.files["image"]
        bg_color = request.form.get("bgcolor", "#ffffff")

        unique_name = str(uuid.uuid4())

        input_path = os.path.join(
            UPLOAD_FOLDER,
            unique_name + ".png"
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            unique_name + ".png"
        )

        file.save(input_path)

        with open(input_path, "rb") as f:
            input_data = f.read()

        output_data = remove(input_data)

        fg = Image.open(
            io.BytesIO(output_data)
        ).convert("RGBA")

        color = bg_color.lstrip("#")

        rgb = tuple(
            int(color[i:i+2], 16)
            for i in (0, 2, 4)
        )

        bg = Image.new(
            "RGBA",
            fg.size,
            rgb + (255,)
        )

        bg.paste(
            fg,
            (0, 0),
            fg
        )

        bg.save(output_path)

        return jsonify({
            "success": True,
            "image_url":
            "/static/output/" +
            unique_name +
            ".png"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
