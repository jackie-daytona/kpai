import requests

for i in range(5):
    response = requests.post("http://127.0.0.1:8000/evaluate")
    print(f"Run {i+1}: {response.json()}")