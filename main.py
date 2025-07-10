@app.get("/test-cors")
async def test_cors():
    return {"message": "CORS is working!"}


# Trigger redeploy to apply CORS fix


from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Allow requests from your GitHub Pages domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/polish-email")
async def polish_email(request: Request):
    data = await request.json()
    original_email = data.get("email", "")

    if not original_email:
        raise HTTPException(status_code=400, detail="Missing email content")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional email editor."},
            {"role": "user", "content": f"Please polish this email:\n\n{original_email}"}
        ]
    )

    polished_email = response['choices'][0]['message']['content']
    return {"polished_email": polished_email}
