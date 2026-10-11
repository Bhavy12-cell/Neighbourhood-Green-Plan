from google import genai

client = genai.Client(api_key="AQ.Ab8RN6JcH70E2cEr-L60PWQCtjiXW0AVNuNYvO8hmJ7Vnaux9A")
for m in client.models.list():
    if "gemma" in m.name.lower():
        print(m.name)