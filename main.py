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

@app.post("/polish-email")
async def polish_email(request: Request):
    data = await request.json()
    original_email = data.get("email", "")
    tone = data.get("tone", "neutral")
    instructions = data.get("instructions", "")

    if not original_email:
        raise HTTPException(status_code=400, detail="Missing email content")

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        system_prompt = "You are a helpful email editor. Please improve the clarity and tone of emails as requested."
        user_prompt = f"Please rewrite the following email with a {tone} tone."
        if instructions:
            user_prompt += f" Additionally, {instructions}."
        user_prompt += f"\n\nEmail:\n{original_email}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        polished_email = response.choices[0].message.content
        return {"polished_email": polished_email}

    except Exception as e:
        print("OpenAI API error:", e)
        raise HTTPException(status_code=500, detail="OpenAI API call failed")
