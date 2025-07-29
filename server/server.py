from flask import Flask, request, jsonify
import util
import util2
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Set up the upload folder for images
UPLOAD_FOLDER = r'C:\pro\static\uploads'  # Updated to the required path
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load saved models at server startup
util.load_saved_artifacts()
util2.load_image_model()

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    data = request.form
    total_sqft = float(data['total_sqft'])
    location = data['location']
    bhk = int(data['bhk'])
    bath = int(data['bath'])

    estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

    response = jsonify({
        'estimated_price': estimated_price
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'fileUpload' not in request.files:
        print("No file part")
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('fileUpload')
    if not files:
        print("No files selected")
        return jsonify({"error": "No files selected"}), 400

    image_paths = []
    predictions = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Saving file: {file_path}")  # Log file saving
            file.save(file_path)
            image_paths.append(f"/static/uploads/{filename}")  # Save only the relative path

            # Assuming util2.predict_damage returns damage predictions
            prediction = util2.predict_damage([file_path])  # Get prediction for this image
            print(f"Prediction for {filename}: {prediction}")  # Debugging line
            predictions.append({
                'image_url': f"/static/uploads/{filename}",
                'damage_prediction': prediction[0]['damage_prediction']  # Assuming the prediction is returned as a list
            })
        else:
            print("Invalid file type")
            return jsonify({"error": "Invalid file type"}), 400

    print("Returning predictions and image paths")
    return jsonify({
        "damage_predictions": predictions,
        "image_paths": image_paths  # Include relative image paths
    })


if __name__ == "__main__":
    print("Starting Python Flask Server...")
    app.run(debug=True, host="0.0.0.0", port=5000)
