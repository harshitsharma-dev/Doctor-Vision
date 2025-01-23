from flask import Flask, render_template, request, jsonify
from inference_sdk import InferenceHTTPClient

import os
from groq import Groq

# Initialize the Flask application
app = Flask(__name__)
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="gOIqsmnuwcSvDkVrVBd6"
)

# Initialize the Groq client with the provided API key
client = Groq(api_key="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")

def validate_question(question):
    
    return True

def query_groq(question):
    """Query Groq Llama3-8b for a response related to water and sanitation infrastructure pricing."""
    # Validate if the question is within the specified domain
    if validate_question(question):
        # Add specific instructions in the system prompt
        messages = [
            {
                "role": "system",
                "content": "You are an AI doctor named Doctor Vision, answer like doctor"
            },
            {
                "role": "user",
                "content": question
            }
        ]

        # Create a chat completion with Groq API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
        )

        # Return the generated response
        return chat_completion.choices[0].message.content

    # If the question is not valid, return a rejection message
    return "I only answer questions related to water and sanitation infrastructure pricing."

# Routes to Render Pages
  # Render index.html as the homepage


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Return the local file URL
        return jsonify({"url": f"http://localhost:5000/{UPLOAD_FOLDER}/{file.filename}"}), 200

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





from flask import Flask, request, jsonify, render_template
from inference_sdk import InferenceHTTPClient

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def analyze_and_return_results():
    if 'file' not in request.files:
        return render_template('bids.html', error="No file part"), 400

    file = request.files['file']
    if file.filename == '':
        return render_template('bids.html', error="No selected file"), 400

    try:
        # Save the uploaded file to a local directory
        filename = file.filename
        upload_path = r"C:\Users\harsh\OneDrive\Documents\NewOne\uploads\\" + filename
        file.save(upload_path)

        # Initialize the inference client
        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key="gOIqsmnuwcSvDkVrVBd6"
        )

        # Perform inference on the uploaded file
        result = CLIENT.infer(upload_path, model_id="pneumonia-kefdw/1")

        # Extract relevant data from the result (customize this based on your result structure)
        predictions = result.get("predictions", [])
        confidence_scores = [pred.get("confidence") for pred in predictions]
        print(predictions)
        # Render results in the template
        return render_template('bids.html', predictions=predictions, confidence_scores=confidence_scores)

    except Exception as e:
        # Handle any exceptions and render error in the template
        return render_template('bids.html', error=f"An error occurred: {str(e)}"), 500


@app.route('/diagnostics')
def project():
    return render_template('project.html')

@app.route('/research')
def bids():
    return render_template('bids.html')

@app.route('/Finances')
def finances():
    return render_template('Finances.html')

@app.route('/audit')
def audit():
    return render_template('Audit.html')

# Chatbot API Endpoint
@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_question = request.form['question']
        response = query_groq(user_question)
        return jsonify(response=response)
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        return jsonify(response="Sorry, there was an error processing your request."), 500

@app.route('/')
def index():
    return render_template('index.html')

# Run the Flask Application
if __name__ == "__main__":
    app.run(debug=True)
