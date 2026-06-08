const API = "http://localhost:5000";

export async function startGame() {
  return fetch(`${API}/start`, { method: "POST" });
}

export async function stepGame() {
  return fetch(`${API}/step`, { method: "POST" });
}

export async function resetGame() {
  return fetch(`${API}/reset`, { method: "POST" });
}

export async function fetchState(mode: string) {
  const res = await fetch(`${API}/state/${mode}`);
  return res.json();
}

export async function sendAction(action: string) {
  return fetch(`${API}/action/${action}`, {
    method: "POST",
  });
}