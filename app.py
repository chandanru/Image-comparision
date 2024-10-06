from flask import Flask, request, render_template
from skimage.metrics import structural_similarity as ssim
import cv2
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def compare_images(image1_path, image2_path):
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
    
    if image1 is None or image2 is None:
        raise FileNotFoundError("One of the images was not found or is not a valid image format")
    
    score, _ = ssim(image1, image2, full=True)
    return score * 100

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploader_file():
    if 'file1' not in request.files or 'file2' not in request.files:
        return 'No file part'
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    file1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
    file2_path = os.path.join(UPLOAD_FOLDER, file2.filename)
    
    file1.save(file1_path)
    file2.save(file2_path)
    
    try:
        similarity = compare_images(file1_path, file2_path)
        return f'Similarity: {similarity:.2f}%'
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
