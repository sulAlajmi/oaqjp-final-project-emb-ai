"""
server.py: This file defines the Flask web application that processes text
and evaluates the dominant emotion using the emotion_detector function.
The application listens for POST requests at the '/emotionDetector' endpoint.

It returns a response with the emotion analysis results or an error message
if the input is invalid.
"""

from flask import Flask, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_endpoint():
    """
    Endpoint to receive a statement and process it for emotion analysis.

    The function checks if the statement is valid, calls the emotion_detector function,
    and returns the response with the processed emotion analysis.

    Returns:
        json: The response containing the processed emotions and dominant emotion
              or an error message if input is invalid.
    """
    # Get the statement from the POST request
    data = request.get_json()
    statement = data.get("statement")

    if not statement:
        return jsonify({"error": "No statement provided"}), 400

    # Call the emotion_detector function to process the statement
    result = emotion_detector(statement)

    if "error" in result:
        return jsonify(result), 400

    # Check if dominant_emotion is None (for blank entries)
    if result.get("dominant_emotion") is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    # Prepare the output format as specified (split long line to comply with PEP 8)
    emotion_output = (
        "For the given statement, the system response is "
        + ', '.join([
            f"'{key}': {value}" for key, value in result.items() if key != 'dominant_emotion'
        ])
        + f". The dominant emotion is {result['dominant_emotion']}."
    )

    # Return the formatted string as part of the JSON response
    return jsonify({"response": emotion_output})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
