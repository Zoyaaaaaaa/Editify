from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
import os
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_image(filename, option):
    print(f"The operation is {option}")
    img_path = os.path.join("static", "uploads", filename)
    output_pdf_path = os.path.join("static", "uploads", filename + ".pdf")

    img = cv2.imread(os.path.join("static", "uploads", filename))
    if option == "cgray":
        img_processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif option == "canny":
        img_processed = cv2.Canny(img, 100, 200)
    elif option == "resize":
        img_processed = cv2.resize(img, (300, 300))
    elif option == "blur":
        img_processed = cv2.GaussianBlur(img, (5, 5), 0)
    elif option == "webp":  
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), img, [cv2.IMWRITE_WEBP_QUALITY, 100])
        return 
    elif option == "pdf":
        img_path = os.path.join("static", "uploads", filename)
        output_pdf_path = os.path.join("static", "uploads", filename + ".pdf")
    elif option == "threshold":
        ret, img_processed = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    elif option == "flip":
        img_processed = cv2.flip(img, 1)
    else:
        flash("Invalid option")
        return
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), img_processed)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/edit", methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        option = request.form['option']  
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            convert_image(filename, option)
            flash(f"Your image has been edited successfully! Click <a href='{url_for('static', filename=f'uploads/{filename}')}'>here</a>")
            return redirect(url_for('hello_world'))

    flash("Error: Invalid request method")
    return redirect(url_for('hello_world'))


if __name__ == "__main__":
    app.run(debug=True)
