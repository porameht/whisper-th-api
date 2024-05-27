from fastapi import FastAPI, File, UploadFile
import requests
from .few_shot_learning import FewShotLearning
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

API_URL = "https://c5taw1ujfkmge21a.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer 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",
    "Content-Type": "audio/flac"
}

few_shot = FewShotLearning(model_name="gpt-3.5-turbo")

def query(audio_file):
    response = requests.post(API_URL, headers=headers, data=audio_file)
    return response.json()

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    audio_data = await file.read()
    response = query(audio_data)
    command = few_shot.few_shot_prompt(response.get('text'))
    return {"text": command}
