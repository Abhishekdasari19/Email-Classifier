# Email Classification with PII Masking

This project masks personal information from support emails and classifies them into categories like Billing, Technical, etc., using a trained machine learning model.

## 🚀 Features
- Regex-based PII masking (names, emails, cards, etc.)
- Naive Bayes classification on masked content
- FastAPI deployment ready for Hugging Face Spaces

## 📦 Setup
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

## 🌐 API Example
POST `/`
```json
{
  "email_body": "Hi my name is John Doe, my email is john@example.com and my issue is with billing."
}
```

## ✅ Output Format
```json
{
  "input_email_body": "...",
  "list_of_masked_entities": [...],
  "masked_email": "...",
  "category_of_the_email": "Billing Issues"
}
```