import re

def extract_efficient_metadata(question, answer):

    combined_text = f"{question} {answer}".lower()

    specialties_pattern = r'\b(cardiology|dermatology|neurology|pediatrics|gynecology|orthopedics|psychiatry)\b'
    specialties = list(set(re.findall(specialties_pattern, combined_text)))

    categories = []
    if any(word in combined_text for word in ['urgent', 'emergency', 'immediately', 'severe']):
        categories.append('urgent')
    if any(word in combined_text for word in ['chronic', 'long-term', 'years']):
        categories.append('chronic')
    if any(word in combined_text for word in ['pregnancy', 'pregnant', 'birth']):
        categories.append('pregnancy')

    age_match = re.search(r'\b(\d+)[- ](?:year|yr|y)[- ](?:old|o)\b', combined_text)
    age = int(age_match.group(1)) if age_match else None

    metadata = {
        "specialties": ", ".join(specialties) if specialties else None,
        "categories": ", ".join(categories) if categories else None,
        "age": age,
        "source": "HealthCareMagic"
    }

    return {k: v for k, v in metadata.items() if v is not None}

