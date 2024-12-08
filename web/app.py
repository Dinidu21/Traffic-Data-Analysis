from flask import Flask, request, render_template

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Traffic Data Analysis Web App!"

if __name__ == '__main__':
    app.run(debug=True)
