from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# Allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/polish-email")
async def polish_email(request: Request):
    data = await request.json()
    original_email = data.get("email", "")
    tone = data.get("tone", "neutral")
    instructions = data.get("instructions", "")
    mode = data.get("mode", "polish")

    if not original_email:
        raise HTTPException(status_code=400, detail="Missing email content")

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # pick system_prompt based on mode
        if mode == "suggest":
            system_prompt = (
                "You are an expert business communications coach. "
                "Rewrite the email to make it more effective, clear, and persuasive. "
                "You may change wording, sentence structure, or even suggest adding or removing content if it strengthens the message. "
                "Be confident and improve it as much as you can."
            )
        else:
            system_prompt = (
                "You are a helpful email editor. "
                "Please improve the clarity and tone of the following email without adding new ideas or suggesting changes beyond grammar and flow."
            )

        # user_prompt is the same for both modes
        user_prompt = (
            f"Rewrite the following email with a {tone} tone. "
            f"Make it as effective, clear, and persuasive as possible. "
            f"Do not hesitate to make significant changes if it improves the message."
        )

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
