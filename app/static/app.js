const chat = document.getElementById("chat");
const form = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const resetButton = document.getElementById("reset");

const sessionId = localStorage.getItem("vlm_session_id") || crypto.randomUUID();
localStorage.setItem("vlm_session_id", sessionId);

function addMessage(role, content) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role}`;
  bubble.textContent = content;
  chat.appendChild(bubble);
  chat.scrollTop = chat.scrollHeight;
}

async function sendMessage(text) {
  addMessage("user", text);
  messageInput.value = "";

  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message: text }),
  });

  if (!response.ok) {
    const data = await response.json();
    addMessage("assistant", `Error: ${data.detail || response.statusText}`);
    return;
  }

  const data = await response.json();
  addMessage("assistant", data.response);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = messageInput.value.trim();
  if (!text) return;
  sendMessage(text);
});

resetButton.addEventListener("click", async () => {
  await fetch("/reset", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message: "reset" }),
  });
  chat.innerHTML = "";
});
