# Editify

At Editify, I utilized cutting-edge technologies to create a seamless image editing platform. Our project is developed using OpenCV and Flask, both recognized for their efficiency and versatility. OpenCV equips us with a rich library of computer vision and image processing algorithms, enabling advanced editing features like grayscale conversion, edge detection, resizing, and blurring. Flask serves as the backbone, providing a lightweight and flexible framework for building dynamic web services. Together, these technologies form the core of Editify, empowering users to unleash their creativity effortlessly.

This Flask web application allows users to upload images, perform various image processing operations, and optionally convert images to PDF or WebP format.

## Features

- **Image Upload:** Upload images in formats such as JPEG, PNG, GIF, etc.
- **Image Processing:** Apply a variety of image processing operations, including:
  - Grayscale conversion
  - Edge detection (Canny)
  - Resizing
  - Blurring
  - Thresholding
  - Flipping
  - Rotating
  - Contrast adjustment
  - HDR merging
  - Brightness adjustment
  - Saturation adjustment
  - Sharpening
  - Histogram equalization
  - Sepia tone transformation
  - Adding watermarks
- **Image Conversion:** Convert images to PDF or WebP formats.
- **Feedback:** Flash messages provide feedback on successful operations or errors.

## Requirements

Ensure you have the following installed:

- Python 3.x
- Flask
- OpenCV (opencv-python)
- ReportLab (reportlab)

You can install the dependencies using pip:

```bash
pip install Flask opencv-python reportlab
```

## Usage

### Clone the Repository

```bash
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

### Set Up the Environment

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

Activate the virtual environment:

On Windows:

```bash
venv\Scripts\activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

### Run the Application

```bash
python app.py
```

Access the application in your web browser at [http://localhost:5000](http://localhost:5000).

### Upload an Image

1. Click on the "Choose File" button, select an image file, and click "Upload".

### Select an Operation

1. Choose an operation from the dropdown menu (e.g., grayscale, resize, blur).

### Adjust Intensity (if applicable)

1. For operations like brightness or saturation, adjust the intensity using the slider.

### Apply the Operation

1. Click on the "Apply" or "Process" button.

### View or Download the Result

1. After processing, view or download the processed image or converted PDF/WebP file.

---

By following these steps, you can easily set up and use the Editify platform to perform advanced image editing and conversion operations.
