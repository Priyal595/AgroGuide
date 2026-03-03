const toggleBtn = document.getElementById("chatbot-toggle");
const wrapper = document.getElementById("chatbot-wrapper");
const closeBtn = document.getElementById("chatbot-close");

let chatbotInitialized = false;

toggleBtn.addEventListener("click", () => {
    wrapper.classList.remove("hidden");
    setTimeout(() => wrapper.classList.add("active"), 10);
    messages.innerHTML = "";
    options.innerHTML = "";

    loadCategories(); 
});

closeBtn.addEventListener("click", () => {
    wrapper.classList.remove("active");
    setTimeout(() => wrapper.classList.add("hidden"), 300);
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

<<<<<<< HEAD
function showTyping() {
    const typing = document.createElement("div");
    typing.className = "bot typing";
    typing.id = "typing-indicator";
    typing.innerText = "🤖 Typing...";
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;
}

=======
>>>>>>> 8e37daa (added links to certain Questions in the chatbox)
function addLink(title, url) {
    const linkDiv = document.createElement("div");
    linkDiv.className = "bot-link";

    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.target = "_blank";
    anchor.rel = "noopener noreferrer";
    anchor.innerText = "🔗 " + title;

    linkDiv.appendChild(anchor);
    messages.appendChild(linkDiv);
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
      showTyping();
      setTimeout(() => {
<<<<<<< HEAD
         const typingElement = document.getElementById("typing-indicator");
            if (typingElement) {
                typingElement.remove();
            }

            addMessage(data.answer);

    // Render links if present
    if (Array.isArray(data.links) && data.links.length > 0) {

        const sourceLabel = document.createElement("div");
        sourceLabel.className = "bot-source-label";
        sourceLabel.innerText = "📚 Sources:";
        messages.appendChild(sourceLabel);

        data.links.forEach(link => {
            addLink(link.title, link.url);
        });
    }

    data.related.forEach(r => {
        addButton(r, () => loadAnswer(category, r));
    });

    addButton("🔄 Switch Category", loadCategories);

}, 800);
    })
    .catch(error => {
        console.error("Error fetching answer:", error);
    });
}

=======
    addMessage(data.answer);

    // Render links if present
    if (Array.isArray(data.links) && data.links.length > 0) {

        const sourceLabel = document.createElement("div");
        sourceLabel.className = "bot-source-label";
        sourceLabel.innerText = "📚 Sources:";
        messages.appendChild(sourceLabel);

        data.links.forEach(link => {
            addLink(link.title, link.url);
        });
    }

    data.related.forEach(r => {
        addButton(r, () => loadAnswer(category, r));
    });

    addButton("🔄 Switch Category", loadCategories);

}, 400);
    });
}
>>>>>>> 8e37daa (added links to certain Questions in the chatbox)
