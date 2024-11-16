from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import json

app = Flask(__name__)

# Base paths for static files
TEMPLATE_PATH = 'static/templates/'
FONT_PATH = 'static/font/'
OUTPUT_PATH = 'static/output/greeting_card.jpg'

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to create the greeting card
@app.route('/create_card', methods=['POST'])
def create_card():
    textbox_data = request.form['textbox_data']
    template = request.form['template']

    # Load the template image
    template_path = TEMPLATE_PATH + template
    img = Image.open(template_path)

    # Load textbox data (position, text, font, and color)
    textboxes = json.loads(textbox_data)

    # Draw on the image
    draw = ImageDraw.Draw(img)

    # Define color map for text
    color_map = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "black": (0, 0, 0),
    }

    # Loop through the text boxes and draw them on the image
    for textbox in textboxes:
        text = textbox['text']
        font_family = textbox['fontFamily']
        color = textbox['color']
        left = int(float(textbox['left'].replace('px', '')))
        top = int(float(textbox['top'].replace('px', '')))
        font_size = int(textbox['fontSize'].replace('px', ''))

        font_path = FONT_PATH + font_family + '.ttf'

        try:
                        selected_font = ImageFont.truetype(font_path, font_size)
        except FileNotFoundError:
            return f"Font file '{font_path}' not found.", 404

        draw.text((left, top), text, font=selected_font, fill=color_map[color])

    # Save the generated image as JPG
    img = img.convert("RGB")  # Ensure the image is in RGB mode to save as JPG
    img.save(OUTPUT_PATH, "JPEG")

    return send_file(OUTPUT_PATH, mimetype='image/jpeg', as_attachment=True, download_name="greeting_card.jpg")

if __name__ == '__main__':
    app.run(debug=True)