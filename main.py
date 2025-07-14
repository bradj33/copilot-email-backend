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

        system_prompt = (
            "You are a helpful email editor and advisor. "
            "When improving an email, also suggest better ways to phrase ideas or add anything important that may be missing. "
            "Be polite and constructive."
        )

        user_prompt = (
            f"Please improve the following email with a {tone} tone. "
            f"If you see opportunities to add clarity, context, or more effective phrasing, please do so."
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
