import re

def mask_pii(text):
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