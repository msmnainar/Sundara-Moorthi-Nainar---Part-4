import requests
import json

# ============================================
# BASE URL (CHANGE IF USING NGROK)
# ============================================
BASE_URL = "https://xxxx.ngrok.io"

# ============================================
# TEST 1: HEALTH CHECK ✅
# ============================================
def test_health():
    print("\n🔹 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    except Exception as e:
        print("❌ Health check failed:", e)


# ============================================
# TEST 2: SINGLE PREDICTION ✅
# ============================================
def test_single_prediction():
    print("\n🔹 Testing /predict endpoint...")

    payload = {
        "recency": 75,
        "frequency": 2,
        "monetary": 2400,
        "ticket_count": 3,
        "avg_sentiment": -0.2
    }

    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print("Status Code:", response.status_code)

        if response.status_code == 200:
            print("Prediction Result:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ Error:", response.text)

    except Exception as e:
        print("❌ Prediction failed:", e)


# ============================================
# TEST 3: BATCH PREDICTION ✅
# ============================================
def test_batch_prediction():
    print("\n🔹 Testing /batch_predict endpoint...")

    payload = [
        {
            "recency": 80,
            "frequency": 1,
            "monetary": 1500,
            "ticket_count": 2,
            "avg_sentiment": -0.3
        },
        {
            "recency": 20,
            "frequency": 5,
            "monetary": 5000,
            "ticket_count": 0,
            "avg_sentiment": 0.6
        }
    ]

    try:
        response = requests.post(f"{BASE_URL}/batch_predict", json=payload)
        print("Status Code:", response.status_code)

        if response.status_code == 200:
            print("Batch Prediction Result:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ Error:", response.text)

    except Exception as e:
        print("❌ Batch prediction failed:", e)


# ============================================
# RUN ALL TESTS ✅
# ============================================
if __name__ == "__main__":
    print("🚀 Running API Tests...")

    test_health()
    test_single_prediction()
    test_batch_prediction()

    print("\n✅ All tests completed")