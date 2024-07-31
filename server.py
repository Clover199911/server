from flask import Flask, request, send_file
import pyvips
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/process_card', methods=['POST'])
def process_card():
    data = request.json
    image_url = data['imageURL']
    condition = data['condition']
    group = data['group']

    # Download the image
    response = requests.get(image_url)
    image = pyvips.Image.new_from_buffer(response.content, "")

    # Resize the image
    image = image.resize(200 / image.width)

    if condition.lower() == 'pristine':
        overlay_filename = 'iotwpristine.png' if group.lower() == 'idol of the week' else 'pristine.png'
        overlay_path = f'pristine/{overlay_filename}'
        overlay = pyvips.Image.new_from_file(overlay_path)
        
        # Composite the overlay
        image = image.composite(overlay, 'over')

    # Convert to PNG
    output_buffer = BytesIO(image.write_to_buffer(".png"))
    output_buffer.seek(0)

    return send_file(output_buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
