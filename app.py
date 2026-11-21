import base64
import os
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openrouter import ChatOpenRouter

st.set_page_config(page_title="Omni AI", page_icon="◼️", layout="centered")

st.markdown(
    """
    <style>
    /* Monochrome Black & White Theme */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000;
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #262626;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff;
    }
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: #0f0f0f;
        border: 1px solid #262626;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.6rem;
        color: #ffffff;
    }
    /* Chat input bar */
    [data-testid="stBottom"], [data-testid="stChatInput"] {
        background-color: #000000;
    }
    [data-testid="stChatInput"] textarea {
        background-color: #0f0f0f !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
        border-radius: 10px !important;
    }
    /* Sidebar inputs, uploader & buttons */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #141414 !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background-color: #141414 !important;
        border: 1px dashed #404040 !important;
    }
    .stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        font-weight: 600;
        border-radius: 8px;
    }
    .stButton > button:hover {
        background-color: #e5e5e5 !important;
        color: #000000 !important;
    }
    h1, h2, h3, p, label, span {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Omni AI")
st.caption("Minimalist multimodal AI assistant (Text + Images) powered by LangChain & OpenRouter")

VISION_MODELS = [
    "google/gemini-2.5-flash",
    "openai/gpt-4o-mini",
    "anthropic/claude-sonnet-4.5",
]

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "OpenRouter API Key",
        value=os.getenv("OPENROUTER_API_KEY", ""),
        type="password",
        placeholder="sk-or-v1-...",
    )
    selected_model = st.selectbox("Vision-Capable Model", VISION_MODELS + ["Custom..."])
    if selected_model == "Custom...":
        model_name = st.text_input("Custom Model Slug", value="google/gemini-2.5-flash")
    else:
        model_name = selected_model

    temperature = st.slider("Temperature", min_value=0.0, max_value=1.5, value=0.7, step=0.1)
    system_prompt = st.text_area(
        "System Prompt",
        value="You are Omni AI, a sharp, helpful multimodal assistant that can analyze both text and images.",
        height=100,
    )

    st.divider()
    uploaded_image = st.file_uploader(
        "Attach an image (optional)",
        type=["png", "jpg", "jpeg", "webp"],
        help="Upload a screenshot or photo, then type your question in the chat box.",
    )
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Attached image", use_container_width=True)

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


def to_langchain_message(item: dict):
    if item["role"] == "assistant":
        return AIMessage(content=item["text"])
    if item.get("image_b64"):
        return HumanMessage(
            content=[
                {"type": "text", "text": item["text"]},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{item['mime_type']};base64,{item['image_b64']}"},
                },
            ]
        )
    return HumanMessage(content=item["text"])


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("image_bytes"):
            st.image(msg["image_bytes"], width=280)
        st.markdown(msg["text"])

if user_input := st.chat_input("Message Omni AI (or ask about your attached image)..."):
    if not api_key:
        st.warning("Please set OPENROUTER_API_KEY or enter your OpenRouter API key in the sidebar.")
        st.stop()

    user_entry = {"role": "user", "text": user_input}
    if uploaded_image is not None:
        raw_bytes = uploaded_image.getvalue()
        user_entry["image_bytes"] = raw_bytes
        user_entry["image_b64"] = base64.b64encode(raw_bytes).decode("utf-8")
        user_entry["mime_type"] = uploaded_image.type or "image/png"

    with st.chat_message("user"):
        if user_entry.get("image_bytes"):
            st.image(user_entry["image_bytes"], width=280)
        st.markdown(user_input)

    history = [to_langchain_message(m) for m in st.session_state.messages]
    current_message = to_langchain_message(user_entry)
    lc_messages = [SystemMessage(content=system_prompt)] + history + [current_message]

    llm = ChatOpenRouter(
        model=model_name,
        api_key=api_key,
        temperature=temperature,
    )
    chain = llm | StrOutputParser()

    with st.chat_message("assistant"):
        try:
            response_text = st.write_stream(chain.stream(lc_messages))
            st.session_state.messages.append(user_entry)
            st.session_state.messages.append({"role": "assistant", "text": response_text})
        except Exception as exc:
            st.error(f"Request failed: {exc}")