import re

def extract_efficient_metadata(question, answer):
    combined_text = f"{question} {answer}".lower()
    
    # Quick regex patterns for key categorization
    specialties_pattern = r'\b(cardiology|dermatology|neurology|pediatrics|gynecology|orthopedics|psychiatry)\b'
    specialties = list(set(re.findall(specialties_pattern, combined_text)))
    
    # Simple keyword-based categorization instead of complex NLP
    categories = []
    if any(word in combined_text for word in ['urgent', 'emergency', 'immediately', 'severe']):
        categories.append('urgent')
    if any(word in combined_text for word in ['chronic', 'long-term', 'years']):
        categories.append('chronic')
    if any(word in combined_text for word in ['pregnancy', 'pregnant', 'birth']):
        categories.append('pregnancy')
    
    # Extract age - single regex only
    age_match = re.search(r'\b(\d+)[- ](?:year|yr|y)[- ](?:old|o)\b', combined_text)
    age = int(age_match.group(1)) if age_match else None
    
    return {
        "specialties": specialties,
        "categories": categories,
        "age": age,
        "source": "HealthCareMagic"
    }