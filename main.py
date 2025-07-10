from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# Allow requests from any origin (for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test endpoint to check if CORS is working
@app.get("/test-cors")
async def test_cors():
    return {"message": "CORS is working!"}

# Endpoint to polish an email using OpenAI's GPT model
@app.post("/polish-email")
async def polish_email(request: Request):
    data = await request.json()
    original_email = data.get("email", "")

    if not original_email:
        raise HTTPException(status_code=400, detail="Missing email content")

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional email editor."},
                {"role": "user", "content": f"Please polish this email:\n\n{original_email}"}
            ]
        )
        polished_email = response.choices[0].message.content

        return {"polished_email": polished_email}
    except Exception as e:
        print("OpenAI API error:", e)
        raise HTTPException(status_code=500, detail="OpenAI API call failed")
