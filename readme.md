# Omni AI

A minimalist, monochrome black-and-white **multimodal** AI chatbot built with **Streamlit**, **LangChain**, and **OpenRouter**—supporting both **text and image inputs** alongside a customizable **System Prompt**.

## Why "Omni AI"?

**Omni AI** is built to adapt to *any* task or role on the fly:

- **Multimodal Understanding (Text + Images):** Upload screenshots, diagrams, handwritten notes, or photos and ask questions about them.
- **Dynamic System Prompt:** Redefine the assistant's exact role and tone directly from the sidebar—turn it into a Coding Tutor, Study Buddy, UI Reviewer, or Document Explainer without changing the code.

## Features

- **Image & Screenshot Analysis:** Attach PNG, JPG, or WEBP images in the sidebar and chat about them using vision-capable models.
- **Real-Time Streaming:** Token-by-token streaming via LangChain (`ChatOpenRouter | StrOutputParser`).
- **Model Flexibility:** Switch between vision-capable models (Gemini, GPT-4o-mini, Claude) or enter any custom OpenRouter model slug.
- **Custom Controls:** Live System Prompt editor, temperature slider, and one-click chat reset.
- **Monochrome UI:** High-contrast black-and-white interface.

## Tech Stack

- [Streamlit](https://docs.streamlit.io/) — Frontend web UI & image uploader
- [LangChain (`langchain-openrouter`)](https://docs.langchain.com/oss/python/integrations/chat/openrouter) — Multimodal message & streaming pipeline
- [OpenRouter](https://openrouter.ai/) — Unified LLM API gateway

## Run Locally (Windows PowerShell)

```powershell
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:OPENROUTER_API_KEY="your-openrouter-api-key"
streamlit run app.py
```

## Connect

Interested in trying the live hosted version, collaborating, or discussing the build? Feel free to open an issue or connect with me on GitHub or LinkedIn!