import requests
import json

def test_review():
    url = "http://localhost:8000/review"
    
    with open("bad_code.py", "r") as f:
        code = f.read()
        
    payload = {
        "code": code,
        "language": "python",
        "filename": "bad_code.py"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(json.dumps(result, indent=2))
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running?")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_review()
