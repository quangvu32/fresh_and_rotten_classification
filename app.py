from flask import Flask, render_template, request, redirect, url_for, session
import os
import gdown
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.secret_key = 'fresh_and_rotten'

file_id = "1QOnKsLohZo2eulFOknQimHjx_t_95O_j"
model_path = "static/model2.h5"  


def download_model():
   
    download_url = f"https://drive.google.com/uc?id={file_id}"
    
    # Check if the model file already exists
    if not os.path.exists(model_path):
        print("Model not found, downloading...")
        
        gdown.download(download_url, model_path, quiet=False)
        print("Model downloaded successfully!")
    else:
        print("Model already exists, skipping download.")


download_model()

model_predict = load_model(model_path)

def predict_fruit(filepath):
    img = image.load_img(filepath, color_mode="rgb", target_size=(150, 150), interpolation="nearest")
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    prediction = model_predict.predict(img_array)[0][0]
    label = 'Fresh Fruit' if prediction < 0.5 else 'Rotten Fruit'
    confidence = (1.0 - prediction) if label == 'Fresh Fruit' else prediction
    return label, round(confidence * 100, 2)




@app.route('/', methods=['GET', 'POST'])
def index():
    results = session.get('results', [])
    selected_images = []  # Store selected images

    results = []
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('file')  # multiple files uploads
        if not files or files[0].filename == '':
            return redirect(request.url)
        
        results = []
        uploaded_files = []
        for file in files:
            if file:
                # Save uploaded file
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                uploaded_files.append(filename)

                # Add to selected images 
                selected_images.append(filename)
                print(selected_images)

                # Perform prediction
                label, confidence = predict_fruit(filepath)

                # Append result
                results.append({
                    'filename': filename,
                    'label': label,
                    'confidence': confidence
                })
        
        

    if request.method == 'GET':
        uploaded_files = session.get('uploaded_files', [])
        # After showing results, delete the uploaded images from folder
        if uploaded_files:
            upload_folder = app.config['UPLOAD_FOLDER']
            for filename in uploaded_files:
                file_path = os.path.join(upload_folder, filename)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        print(f"Deleted file {filename}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
        
            # After deletion, clear session data
            session.pop('uploaded_files', None)

    

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
