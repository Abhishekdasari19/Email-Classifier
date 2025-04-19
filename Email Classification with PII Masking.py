#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import spacy
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report


# In[3]:


df = pd.read_csv("combined_emails_with_natural_pii.csv")
df.head()


# In[4]:


pii_patterns = {
    "full_name": r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "phone_number": r"\b\d{10}\b",
    "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
    "aadhar_num": r"\b\d{4} \d{4} \d{4}\b",
    "credit_debit_no": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])/?[0-9]{2,4}\b"
}


# In[5]:


def mask_pii(text):
    masked_text = text
    entities = []
    
    for label, pattern in pii_patterns.items():
        for match in re.finditer(pattern, text):
            entity_value = match.group()
            start, end = match.span()
            entities.append({
                "position": [start, end],
                "classification": label,
                "entity": entity_value
            })
            masked_text = masked_text.replace(entity_value, f"[{label}]")
    
    return masked_text, entities


# In[6]:


masked_emails = []
entities_list = []

for email in df["email"]:
    masked, entities = mask_pii(email)
    masked_emails.append(masked)
    entities_list.append(entities)

df["masked_email"] = masked_emails
df["masked_entities"] = entities_list


# In[7]:


X_train, X_test, y_train, y_test = train_test_split(
    df["masked_email"], df["type"], test_size=0.2, random_state=42
)


# In[8]:


clf_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

clf_pipeline.fit(X_train, y_train)

clf_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

clf_pipeline.fit(X_train, y_train)


# In[9]:


y_pred = clf_pipeline.predict(X_test)
print(classification_report(y_test, y_pred))


# In[10]:


def classify_email(email_body):
    masked_email, entities = mask_pii(email_body)
    category = clf_pipeline.predict([masked_email])[0]
    
    return {
        "input_email_body": email_body,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": category
    }


# In[11]:


sample_email = df["email"].iloc[0]
response = classify_email(sample_email)

print(json.dumps(response, indent=2))


# In[ ]:




