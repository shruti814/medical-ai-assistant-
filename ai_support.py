CONDITION_RULES={
    "Common Cold":["cold","cough","fever"],
    "Viral Fever":["fever","fatigue","body pain"],
    "Migraine":["headache","nausea"],
    "Food Poisoning":["vomiting","nausea","stomach pain"]
}
DANGER=["chest pain","shortness of breath","severe bleeding","loss of consciousness"]

SEVERITY_RULES = {
    "HIGH": ["chest pain", "shortness of breath", "loss of consciousness"],
    "MEDIUM": ["high fever", "vomiting", "severe pain"],
    "LOW": ["fever", "headache", "cold", "cough"]
}

def ai_medical_support(symptoms):
    severity = "Moderate"

    possible_conditions = []
    medicines = []

    if "fever" in symptoms:
        possible_conditions.append("Viral Fever")
        medicines.append("Paracetamol")

    if "headache" in symptoms:
        possible_conditions.append("Migraine")
        medicines.append("Ibuprofen")

    return {
        "severity": severity,
        "possible_conditions": possible_conditions,
        "medicines": medicines
    }

if __name__ == "__main__":
    test_symptoms = ["fever", "headache"]
    print(ai_medical_support(test_symptoms))