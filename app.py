from flask import Flask, render_template, request
from keras.models import load_model
from werkzeug.utils import secure_filename 
from PIL import Image, ImageOps
import numpy as np
import os

app = Flask(__name__)

# Load the Keras model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

def model_predict(image_path,model,class_names):
    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    # Open and preprocess the image
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]
    
    return class_name[2:],confidence_score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method =='POST':
        f=request.files['file']
        uploads_folder=os.path.join(app.root_path,'uploads')
        os.makedirs(uploads_folder,exist_ok=True)
        file_path=os.path.join(uploads_folder, secure_filename(f.filename))
        f.save(file_path)
        
        a,b=model_predict(file_path,model,class_names)
        print(a,b)
        if a=='ECZEMA':
            return render_template('eczema.html')
        if a=='MELANOMA':
            return render_template('melanoma.html')
        if a=='ATOPIC DERMATITIS':
            return render_template('atopic.html')
        if a=='BASIL CELL CARCINOMA':
            return render_template('basil.html')
        if a=='MELANOCYTIC NEVI':
            return render_template('nevi.html')
    return render_template('benign.html')
if __name__ == '__main__':
    app.run(debug=True)
 