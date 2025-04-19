from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from utils import mask_pii

app = FastAPI()
model = joblib.load("saved_model.pkl")

class EmailRequest(BaseModel):
    email_body: str

@app.post("/")
def classify_email(req: EmailRequest):
    masked_email, entities = mask_pii(req.email_body)
    prediction = model.predict([masked_email])[0]
    return {
        "input_email_body": req.email_body,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": prediction
    }