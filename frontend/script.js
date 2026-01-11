// const API = "http://127.0.0.1:8000";

// function showTab(tab) {
//   document.getElementById("generate").classList.add("hidden");
//   document.getElementById("history").classList.add("hidden");

//   document.querySelectorAll(".tabs button").forEach(b => b.classList.remove("active"));

//   document.getElementById(tab).classList.remove("hidden");
//   event.target.classList.add("active");

//   if (tab === "history") loadHistory();
// }

// async function generateQuiz() {
//   const url = document.getElementById("url").value;
//   const difficulty = document.getElementById("difficulty").value;
//   const num = document.getElementById("num_questions").value;

//   let endpoint = `${API}/generate-quiz?url=${encodeURIComponent(url)}&num_questions=${num}`;
//   if (difficulty) endpoint += `&difficulty=${difficulty}`;

//   const res = await fetch(endpoint, { method: "POST" });
//   const data = await res.json();

//   renderQuiz(data.quiz);
// }

// function renderQuiz(quiz) {
//   const container = document.getElementById("quiz-container");
//   container.innerHTML = "";

//   quiz.forEach(q => {
//     container.innerHTML += `
//       <div class="quiz-card">
//         <b>${q.question}</b>
//         <span class="badge">${q.difficulty}</span>
//         <ul>
//           ${q.options.map(o => `<li>${o}</li>`).join("")}
//         </ul>
//         <details>
//           <summary>Show Answer</summary>
//           <b>${q.answer}</b>
//           <p>${q.explanation}</p>
//         </details>
//       </div>
//     `;
//   });
// }

// async function loadHistory() {
//   const res = await fetch(`${API}/history`);
//   const data = await res.json();

//   const table = document.getElementById("history-table");
//   table.innerHTML = "";

//   data.forEach(row => {
//     table.innerHTML += `
//       <tr>
//         <td>${row.id}</td>
//         <td>${row.url}</td>
//         <td><button onclick="viewDetails(${row.id})">Details</button></td>
//       </tr>
//     `;
//   });
// }

// async function viewDetails(id) {
//   const res = await fetch(`${API}/history/${id}`);
//   const data = await res.json();

//   document.getElementById("modal-body").innerHTML = `
//     <h3>${data.title}</h3>
//     ${data.quiz.map(q => `
//       <div class="quiz-card">
//         <b>${q.question}</b>
//         <p><i>${q.answer}</i></p>
//       </div>
//     `).join("")}
//   `;

//   document.getElementById("modal").classList.remove("hidden");
// }

// function closeModal() {
//   document.getElementById("modal").classList.add("hidden");
// }


// frontend/script.js
const API = "http://127.0.0.1:8000";

document.getElementById("tab-generate").onclick = () => switchTab("generate");
document.getElementById("tab-history").onclick = () => switchTab("history");
document.getElementById("generateBtn").onclick = generateQuiz;
document.getElementById("closeModal").onclick = closeModal;

function switchTab(name) {
  document.getElementById("generate").classList.toggle("hidden", name !== "generate");
  document.getElementById("history").classList.toggle("hidden", name !== "history");
  document.getElementById("tab-generate").classList.toggle("active", name === "generate");
  document.getElementById("tab-history").classList.toggle("active", name === "history");
  if (name === "history") loadHistory();
}

async function generateQuiz() {
  const url = document.getElementById("url").value;
  const difficulty = document.getElementById("difficulty").value;
  const num = document.getElementById("num_questions").value || 5;

  if (!url) {
    showStatus("Please enter a Wikipedia URL", true);
    return;
  }

  showStatus("Generating quiz... (may take a few seconds)", false);

  try {
    let endpoint = `${API}/generate-quiz?url=${encodeURIComponent(url)}&num_questions=${num}`;
    if (difficulty) endpoint += `&difficulty=${encodeURIComponent(difficulty)}`;

    const res = await fetch(endpoint, { method: "POST" });
    const data = await res.json();
    if (!res.ok) {
      showStatus("Error: " + (data.detail || JSON.stringify(data)), true);
      return;
    }

    renderQuiz(data.quiz || []);
    showStatus("Quiz generated.", false);
  } catch (err) {
    showStatus("Network or server error: " + err.message, true);
  }
}

function showStatus(msg, isError=false) {
  const s = document.getElementById("status");
  s.textContent = msg;
  s.style.color = isError ? "red" : "green";
}

function renderQuiz(quiz) {
  const container = document.getElementById("quiz-container");
  container.innerHTML = "";
  if (!quiz || quiz.length === 0) {
    container.innerHTML = "<p>No questions returned.</p>";
    return;
  }

  quiz.forEach((q, idx) => {
    const card = document.createElement("div");
    card.className = "card";
    let html = `<h3>Q${idx+1}. ${escapeHtml(q.question)}</h3>`;
    html += `<div class="meta"><span class="badge">${escapeHtml(q.difficulty || "")}</span></div>`;
    html += "<ul>";
    if (Array.isArray(q.options)) {
      q.options.forEach(o => html += `<li>${escapeHtml(o)}</li>`);
    }
    html += "</ul>";
    html += `<details><summary>Show answer & explanation</summary><p><b>${escapeHtml(q.answer)}</b></p><p>${escapeHtml(q.explanation)}</p></details>`;
    card.innerHTML = html;
    container.appendChild(card);
  });
}

function escapeHtml(s){ return (s||"").replace(/[&<>"']/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' })[c]); }

// History
async function loadHistory() {
  const tbody = document.querySelector("#history-table tbody");
  tbody.innerHTML = "<tr><td colspan='3'>Loading...</td></tr>";
  try {
    const res = await fetch(`${API}/history`);
    const rows = await res.json();
    tbody.innerHTML = "";
    rows.forEach(r => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${r.id}</td><td>${escapeHtml(r.title || r.url)}</td><td><button onclick="viewDetails(${r.id})">Details</button></td>`;
      tbody.appendChild(tr);
    });
    if (rows.length === 0) tbody.innerHTML = "<tr><td colspan='3'>No history yet.</td></tr>";
  } catch(err) {
    tbody.innerHTML = `<tr><td colspan='3'>Error loading history: ${err.message}</td></tr>`;
  }
}

async function viewDetails(id) {
  try {
    const res = await fetch(`${API}/history/${id}`);
    const data = await res.json();
    if (!res.ok) {
      alert("Error: " + JSON.stringify(data));
      return;
    }
    let html = `<h2>${escapeHtml(data.title || data.url)}</h2>`;
    html += `<p><i>${escapeHtml(data.summary || "")}</i></p>`;
    html += `<h3>Quiz</h3>`;
    (data.quiz || []).forEach((q, i) => {
      html += `<div class="card"><h4>Q${i+1}. ${escapeHtml(q.question)}</h4><ul>`;
      (q.options || []).forEach(opt => html += `<li>${escapeHtml(opt)}</li>`);
      html += `</ul><p><b>Answer:</b> ${escapeHtml(q.answer)}<br/><b>Explanation:</b> ${escapeHtml(q.explanation)}</p></div>`;
    });
    html += `<h3>Related Topics</h3><ul>${(data.related_topics||[]).map(t=>`<li>${escapeHtml(t)}</li>`).join("")}</ul>`;
    document.getElementById("modal-content").innerHTML = html;
    document.getElementById("modal").classList.remove("hidden");
  } catch (err) {
    alert("Error loading details: " + err.message);
  }
}

function closeModal() {
  document.getElementById("modal").classList.add("hidden");
}
