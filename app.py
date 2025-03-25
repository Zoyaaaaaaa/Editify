from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import cv2
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_image(filename, option, intensity=1.0):
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError("Could not read the image file")
            
        if option == "cgray":
            img_processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif option == "canny":
            img_processed = cv2.Canny(img, 100, 200)
        elif option == "resize":
            img_processed = cv2.resize(img, (300, 300))
        elif option == "blur":
            img_processed = cv2.GaussianBlur(img, (5, 5), 0)
        elif option == "webp":
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.rsplit('.', 1)[0] + ".webp")
            cv2.imwrite(output_path, img, [cv2.IMWRITE_WEBP_QUALITY, 100])
            return filename.rsplit('.', 1)[0] + ".webp"
        elif option == "pdf":
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + ".pdf")
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.drawImage(img_path, 0, 0, width=letter[0], height=letter[1])
            c.save()
            return filename + ".pdf"
        elif option == "threshold":
            if len(img.shape) > 2:  # Convert to grayscale first if color image
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, img_processed = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        elif option == "flip":
            img_processed = cv2.flip(img, 1)
        elif option == "rotate":
            img_processed = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif option == "contrast":
            alpha = 2.0  # Contrast control (1.0-3.0)
            beta = 10    # Brightness control (0-100)
            img_processed = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        elif option == "hdr":
            exposures = [cv2.convertScaleAbs(img, alpha=0.5), img, cv2.convertScaleAbs(img, alpha=1.5)]
            merge_mertens = cv2.createMergeMertens()
            hdr = merge_mertens.process(exposures)
            img_processed = np.clip(hdr * 255, 0, 255).astype('uint8')
        elif option == "brightness":
            img_processed = cv2.convertScaleAbs(img, beta=intensity*50)  # Scale intensity appropriately
        elif option == "saturation":
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype('float32')
            hsv_img[:, :, 1] = np.clip(hsv_img[:, :, 1] * intensity, 0, 255)
            img_processed = cv2.cvtColor(hsv_img.astype('uint8'), cv2.COLOR_HSV2BGR)
        elif option == "sharpen":
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            img_processed = cv2.filter2D(img, -1, kernel)
        elif option == "hist_eq":
            if len(img.shape) > 2:  # Color image
                img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
                img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
                img_processed = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
            else:  # Grayscale image
                img_processed = cv2.equalizeHist(img)
        elif option == "sepia":
            kernel = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
            img_processed = cv2.transform(img, kernel)
        elif option == "watermark":
            watermark_text = "Sample Watermark"
            font = cv2.FONT_HERSHEY_SIMPLEX
            img_processed = cv2.putText(img, watermark_text, (10, img.shape[0] - 10), 
                                      font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            flash("Invalid option")
            return filename
        
        if option not in ["webp", "pdf"]:
            processed_filename = f"processed_{filename}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
            success = cv2.imwrite(output_path, img_processed)
            if not success:
                raise ValueError("Failed to save processed image")
            return processed_filename
            
    except Exception as e:
        flash(f"Error processing image: {str(e)}")
        return filename

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/edit", methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    option = request.form.get('option')
    intensity = float(request.form.get('intensity', 1.0))
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            processed_filename = convert_image(filename, option, intensity)
            if option in ["webp", "pdf"]:
                flash(f"Your file has been converted to {option.upper()}! <a href='{url_for('static', filename=f'uploads/{processed_filename}')}'>Click here to download</a>")
            else:
                flash(f"Your image has been edited successfully! <a href='{url_for('static', filename=f'uploads/{processed_filename}')}'>Click here to view</a>")
        except Exception as e:
            flash(f"Error processing image: {str(e)}")
            os.remove(file_path)  # Clean up the uploaded file
        
        return redirect(url_for('home'))
    
    flash("Error: Invalid file type")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)