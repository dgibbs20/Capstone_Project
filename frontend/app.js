const API = "http://127.0.0.1:8000";

async function listTransactions() {
  try {
    const res = await fetch(`${API}/transactions`);
    if (!res.ok) throw new Error("List fetch failed");
    const data = await res.json();
    const tbody = document.querySelector("#txTable tbody");
    tbody.innerHTML = "";
    for (const tx of data) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${new Date(tx.created_at).toLocaleString()}</td>
        <td>${tx.description}</td>
        <td>${tx.merchant}</td>
        <td>$${Number(tx.amount).toFixed(2)}</td>
        <td>${tx.payment_method}</td>
        <td><span class="pill">${tx.category}</span></td>
      `;
      tbody.appendChild(tr);
    }
  } catch (e) {
    console.error(e);
  }
}

document.getElementById("txForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const result = document.getElementById("result");
  result.textContent = "";
  result.className = "result";

  const payload = {
    description: document.getElementById("description").value.trim(),
    merchant: document.getElementById("merchant").value.trim(),
    amount: Number(document.getElementById("amount").value),
    payment_method: document.getElementById("payment_method").value
  };

  try {
    const res = await fetch(`${API}/transactions`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      result.textContent = "Error saving transaction.";
      result.className = "result error";
      return;
    }
    const data = await res.json();
    result.textContent = `Predicted: ${data.category}`;
    result.className = "result ok";
    await listTransactions();
    e.target.reset();
  } catch (err) {
    console.error(err);
    result.textContent = "Network error.";
    result.className = "result error";
  }
});

listTransactions();