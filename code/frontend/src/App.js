import React, { useState } from "react";

function App() {
  const [transactionId, setTransactionId] = useState("");
  const [details, setDetails] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/analyze_transaction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transaction_id: transactionId, details }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "auto" }}>
      <h2>Transaction Risk Analysis</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Transaction ID:</label>
          <input
            type="text"
            value={transactionId}
            onChange={(e) => setTransactionId(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Transaction Details:</label>
          <textarea
            value={details}
            onChange={(e) => setDetails(e.target.value)}
            required
          ></textarea>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: "20px", padding: "10px", border: "1px solid #ccc" }}>
          <h3>Analysis Result</h3>
          <p><strong>Transaction ID:</strong> {result.Transaction_ID}</p>
          <p><strong>Extracted Entities:</strong> {result.Extracted_Entities}</p>
          <p><strong>Entity Type:</strong> {result.Entity_Type}</p>
          <p><strong>Risk Score:</strong> {result.Risk_Score}</p>
          <p><strong>Supporting Evidence:</strong> {result.Supporting_Evidence}</p>
          <p><strong>Confidence Score:</strong> {result.Confidence_Score}</p>
          <p><strong>Reason:</strong> {result.Reason}</p>
        </div>
      )}
    </div>
  );
}

export default App;

