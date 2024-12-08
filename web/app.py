from flask import Flask, render_template, request
import os

# Initialize the Flask application
app = Flask(__name__)

# Directory for uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to render the form
@app.route('/')
def home():
    return render_template('form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        file = request.files['file']

        if file:
            # Save the file to the 'uploads' folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Render the success message
            return render_template('success.html', message="File uploaded successfully!")

        else:
            return "No file selected"

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
