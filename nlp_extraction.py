import re

#nlp= spacy.load("en_core_web_sm")

SYMPTOMS=["fever","headache","fatigue","cough","chest pain","cold",
          "nausea","vomiting","pain"]
MEDICINES=["paracetamol","asprin","ibuprofen","amoxicillin",
           "cetrizine"]

def extract_medical_info(text):
    text= text.lower()
    symptoms_found=[s for s in SYMPTOMS if s in text]
    medicines_found=[m for m in MEDICINES if m in text]

    return{
        "symptoms":list(set(symptoms_found)),
        "medicines":list(set(medicines_found))
    }

if __name__=="__main__":
    sample_text= "Patient has fever and nausea, prescribing amoxicillin."
    result= extract_medical_info(sample_text)
    print(result)