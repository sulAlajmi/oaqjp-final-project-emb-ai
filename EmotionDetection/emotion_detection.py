import requests
import json

def emotion_detector(text_to_analyze):
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(url, headers=headers, json=input_json)

    if response.status_code != 200:
        return {"error": f"Request failed with status code {response.status_code}"}

    response_json = response.json()

    #  Extract emotions correctly from the response
    emotion_data = response_json.get("emotionPredictions", [{}])[0].get("emotion", {})

    if not emotion_data:
        return {"error": "No emotion data found"}

    #  Extract required emotions
    required_emotions = ["anger", "disgust", "fear", "joy", "sadness"]
    formatted_emotions = {emotion: emotion_data.get(emotion, 0) for emotion in required_emotions}


    #  Find dominant emotion
    dominant_emotion = max(formatted_emotions, key=formatted_emotions.get)
    formatted_emotions["dominant_emotion"] = dominant_emotion

    return formatted_emotions