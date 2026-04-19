import requests
import json
import os

def test_improvements():
    url_review = "http://localhost:8000/review"
    url_report = "http://localhost:8000/review/report"
    
    # Code with security issue (hardcoded password)
    insecure_code = """
def connect_db():
    password = "hardcoded_password_123"
    print(f"Connecting with {password}")
    """
    
    payload = {
        "code": insecure_code,
        "language": "python",
        "filename": "insecure.py"
    }
    
    print("1. Testing Security Scanning...")
    try:
        response = requests.post(url_review, json=payload)
        response.raise_for_status()
        result = response.json()
        
        security_issues = [i for i in result['issues'] if i['category'] == 'Security']
        if security_issues:
            print("   SUCCESS: Security issues found:")
            for issue in security_issues:
                print(f"   - {issue['description']}")
        else:
            print("   FAILURE: No security issues found (Bandit might not be working).")
            
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n2. Testing PDF Report Generation...")
    try:
        response = requests.post(url_report, params={"format": "pdf"}, json=payload)
        response.raise_for_status()
        
        with open("report.pdf", "wb") as f:
            f.write(response.content)
            
        if os.path.exists("report.pdf") and os.path.getsize("report.pdf") > 0:
            print("   SUCCESS: PDF report downloaded (report.pdf).")
        else:
            print("   FAILURE: PDF file is empty or missing.")
            
    except Exception as e:
        print(f"   ERROR: {e}")

if __name__ == "__main__":
    test_improvements()
