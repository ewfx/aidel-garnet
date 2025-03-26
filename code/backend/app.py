import requests
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Load Hugging Face NLP Model for Named Entity Recognition (NER)
nlp = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

# Function to classify entity type based on keywords
def classify_entity(entity_name):
    entity_name = entity_name.lower()

    if any(keyword in entity_name for keyword in ["holdings", "trust", "offshore", "fund", "management"]):
        return "Shell Company"
    elif any(keyword in entity_name for keyword in ["capital", "partners", "investment"]):
        return "Investment Firm"
    elif any(keyword in entity_name for keyword in ["foundation", "association", "charity", "nonprofit"]):
        return "NGO"
    elif "bank" in entity_name:
        return "Financial Institution"
    elif any(keyword in entity_name for keyword in ["corp", "inc", "ltd", "llc"]):
        return "Corporation"
    
    return "Unknown"

# Function to check OFAC Sanctions List
def check_sanctions_list(entity):
    url = "https://scsanctions.un.org/resources/xml/en/consolidated.xml"
    response = requests.get(url, timeout=5)
    return entity.lower() in response.text.lower() if response.status_code == 200 else False

# Function to check SEC Registration
def check_sec_registration(entity):
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?company={entity}&count=1&action=getcompany"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=5)
    return "No matching companies" not in response.text

# Function to fetch Wikipedia summary
def get_wikipedia_summary(entity):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{entity}"
    response = requests.get(url, timeout=5)
    return response.json().get("extract", "No summary available.") if response.status_code == 200 else "No data available."

# Updated Risk Calculation Logic
def calculate_risk_score(entity_data):
    risk_score = 0
    reasons = []

    # Increase risk if entity is on sanctions list
    if entity_data["on_sanctions_list"]:
        risk_score += 50
        reasons.append(f"{entity_data['name']} is on the OFAC sanctions list.")

    # Increase risk if entity is NOT SEC registered
    if not entity_data["sec_registered"]:
        risk_score += 20
        reasons.append(f"{entity_data['name']} is not registered with the SEC.")

    # Increase risk if Wikipedia mentions controversy or fraud
    if "controversy" in entity_data["wikipedia_summary"].lower() or "fraud" in entity_data["wikipedia_summary"].lower():
        risk_score += 30
        reasons.append(f"Wikipedia mentions controversy or fraud for {entity_data['name']}.")

    # Increase risk if entity is classified as a Shell Company or Offshore Entity
    if entity_data["type"] in ["Shell Company", "Offshore Entity"]:
        risk_score += 60  # Higher weight for Shell Companies & Offshore Entities
        reasons.append(f"{entity_data['name']} is flagged as a {entity_data['type']}.")

    # Ensure Risk Score is never 0 for identified entities
    if risk_score == 0:
        risk_score = 10  # Assign a minimum baseline risk score if no risk factors are detected

    # Cap risk score at 100
    final_risk_score = round(min(risk_score / 100, 1), 2)

    return {
        "risk_score": final_risk_score,
        "confidence_score": 0.95,
        "reasons": ", ".join(set(reasons)) if reasons else "No significant risk detected"
    }

@app.route("/analyze_transaction", methods=["POST"])
def analyze_transaction():
    data = request.json
    transaction_id = data.get("transaction_id")
    transaction_text = data.get("details", "")

    # Extract only organization names, not full text
    extracted_entities = {
        ent["word"] for ent in nlp(transaction_text) if "entity_group" in ent and ent["entity_group"] == "ORG"
    }

    entity_types, supporting_evidence, reasons = [], set(), set()
    max_risk_score, max_confidence_score = 0, 0

    for entity in extracted_entities:
        entity_type = classify_entity(entity)
        entity_data = {
            "name": entity,
            "type": entity_type,
            "on_sanctions_list": check_sanctions_list(entity),
            "sec_registered": check_sec_registration(entity),
            "wikipedia_summary": get_wikipedia_summary(entity),
        }

        risk_result = calculate_risk_score(entity_data)
        max_risk_score = max(max_risk_score, risk_result["risk_score"])
        max_confidence_score = max(max_confidence_score, risk_result["confidence_score"])

        entity_types.append(entity_type)
        supporting_evidence.update(["Wikidata", "OFAC", "SEC EDGAR"])
        reasons.update(risk_result["reasons"].split(", "))

    return jsonify({
        "Transaction_ID": transaction_id,
        "Extracted_Entities": ", ".join(extracted_entities),
        "Entity_Type": ", ".join(entity_types),
        "Risk_Score": max_risk_score,
        "Supporting_Evidence": ", ".join(supporting_evidence),
        "Confidence_Score": max_confidence_score,
        "Reason": ", ".join(reasons)
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)

