import requests

url = "http://localhost:11434/api/generate"
payload = {
    "model": "mistral:7b-instruct-q4_K_M",
    "prompt": "Quel est le sens de la vie ?",
    "stream": False
}

try:
    response = requests.post(url, json=payload, timeout=15)
    print("✅ Status:", response.status_code)
    print("🧠 Réponse JSON:", response.json())
except requests.exceptions.RequestException as e:
    print("❌ Erreur de requête:", e)
