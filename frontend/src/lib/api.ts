const API = process.env.NEXT_PUBLIC_API;

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

export async function getMaps(): Promise<string[]> {
  const res = await fetch(`${API}/maps`);
  return res.json();
}

export async function selectMap(map: string) {
  return fetch(`${API}/map`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ map }),
  });
}

export async function getMapPreview(map: string) {
  const res = await fetch(`${API}/map-preview`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ map }),
  });

  return res.json();
}