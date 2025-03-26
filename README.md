# 🛡️ Entity Risk Analysis System  

A machine learning-powered system for assessing the risk of financial transactions based on Named Entity Recognition (NER), public sanctions lists, and open data sources.

---

## 🚀 Features  
✅ **Extracts entities** from transaction details  
✅ **Classifies entities** (Corporation, NGO, Shell Company, etc.)  
✅ **Checks sanctions lists** (OFAC, SEC EDGAR, Wikipedia)  
✅ **Calculates risk score** based on entity type and regulatory status  
✅ **Displays results** in a React frontend  

---

## 🛠️ Tech Stack  
- **Backend:** Flask (Python)  
- **Frontend:** React.js  
- **ML Model:** Hugging Face NER  
- **Data Sources:** OFAC, SEC EDGAR, Wikipedia  

---

## 📥 Installation & Setup  

### ️1.  Clone the Repository**
```sh
git clone https://github.com/YOUR_USERNAME/aidel-garnet.git
cd aidel-garnet


##### 2. SETUP BACKEND


cd backend
python3 -m venv venv
source venv/bin/activate  # (Mac/Linux)
venv\Scripts\activate     # (Windows)
pip3 install -r requirements.txt

##### 3. START THE BACKEND

python3 app.py


### Backend runs at: http://127.0.0.1:5000/


##### $. SETUP THE FRONTEND

cd ../frontend
npm install
npm start


#### Frontend runs at: http://localhost:3000/

#### API USAGE

curl -X POST http://127.0.0.1:5000/analyze_transaction \
-H "Content-Type: application/json" \
-d '{"transaction_id": "TXN1001", "details": "Oceanic Holdings Ltd transferred $2,000,000 to an NGO in the Cayman Islands."}'


### EXAMPLE API RESPONSE

{
  "Transaction_ID": "TXN1001",
  "Extracted_Entities": "Oceanic Holdings Ltd, Quantum Holdings Ltd",
  "Entity_Type": "Shell Company, Offshore Entity",
  "Risk_Score": 0.95,
  "Supporting_Evidence": "OFAC, SEC EDGAR, Wikidata",
  "Confidence_Score": 0.97,
  "Reason": "Oceanic Holdings Ltd is flagged as a Shell Company. Quantum Holdings Ltd is flagged as an Offshore Entity."
}

