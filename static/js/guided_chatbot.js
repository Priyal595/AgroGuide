const toggleBtn = document.getElementById("chatbot-toggle");
const wrapper = document.getElementById("chatbot-wrapper");
const closeBtn = document.getElementById("chatbot-close");

toggleBtn.addEventListener("click", () => {
    wrapper.classList.remove("hidden");
    loadCategories();
});

closeBtn.addEventListener("click", () => {
    wrapper.classList.add("hidden");
});

const messages = document.getElementById("chat-messages");
const options = document.getElementById("chat-options");

function addMessage(text, sender = "bot") {
  const div = document.createElement("div");
  div.className = sender;
  div.innerText = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function clearOptions() {
  options.innerHTML = "";
}

function addButton(text, onClick) {
  const btn = document.createElement("button");
  btn.innerText = text;
  btn.onclick = onClick;
  options.appendChild(btn);
}

function loadCategories() {
  clearOptions();
  addMessage("👋 Welcome! Please select the type of question you have:");
  fetch("/api/chatbot/categories/")
    .then(res => res.json())
    .then(data => {
      data.forEach(cat => {
        addButton(cat.toUpperCase(), () => loadQuestions(cat));
      });
    });
}

function loadQuestions(category) {
  clearOptions();
  addMessage(`Selected: ${category}`, "user");
  fetch(`/api/chatbot/questions/?category=${category}`)
    .then(res => res.json())
    .then(data => {
      data.questions.slice(0,5).forEach(q => {
        addButton(q, () => loadAnswer(category, q));
      });
    });
}

function loadAnswer(category, question) {
  clearOptions();
  addMessage(question, "user");
  fetch("/api/chatbot/answer/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ category, question })
  })
    .then(res => res.json())
    .then(data => {
      setTimeout(() => {
        addMessage(data.answer);
        data.related.forEach(r => {
          addButton(r, () => loadAnswer(category, r));
        });
        addButton("🔄 Switch Category", loadCategories);
      }, 400);
    });
}

loadCategories();