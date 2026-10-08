
import streamlit as st
from google import genai

# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="Jyothirmai's chatbot",
    page_icon="🤖"
)

st.title("🤖Jyothirmai's chatbot")
st.caption("Chat with Gemini using Google AI Studio")

# =====================================================
# API KEY
# =====================================================

GOOGLE_API_KEY = "AQ.Ab8RN6JjCbtDD2XsvEwzL5QAhTtMoUWXq4PRvz14IBKm6fJNyw"

if GOOGLE_API_KEY == "YOUR_NEW_API_KEY_HERE":
    st.error("Please add your Google AI Studio API key.")
    st.stop()

# =====================================================
# CREATE CLIENT
# =====================================================

try:
    client = genai.Client(
        api_key=GOOGLE_API_KEY
    )

except Exception as e:
    st.error("Could not connect to Gemini.")
    st.code(str(e))
    st.stop()

# =====================================================
# CHAT HISTORY
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "previous_interaction_id" not in st.session_state:
    st.session_state.previous_interaction_id = None

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("⚙️ Settings")

    st.write("Model:")
    st.code("gemini-3.8-flash")

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []
        st.session_state.previous_interaction_id = None

        st.rerun()

# =====================================================
# DISPLAY OLD MESSAGES
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="👤" if message["role"] == "user" else "🤖"
    ):

        st.markdown(message["content"])

# =====================================================
# CHAT INPUT
# =====================================================

prompt = st.chat_input("Type your message...")

if prompt:

    # -------------------------------------------------
    # SHOW USER MESSAGE
    # -------------------------------------------------

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # -------------------------------------------------
    # GEMINI RESPONSE
    # -------------------------------------------------

    with st.chat_message("assistant", avatar="🤖"):

        try:

            # First message
            if st.session_state.previous_interaction_id is None:

                interaction = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=prompt
                )

            # Continue conversation
            else:

                interaction = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=prompt,
                    previous_interaction_id=(
                        st.session_state.previous_interaction_id
                    )
                )

            # -------------------------------------------------
            # GET RESPONSE
            # -------------------------------------------------

            answer = interaction.output_text

            if answer:

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                # Remember conversation
                st.session_state.previous_interaction_id = (
                    interaction.id
                )

            else:

                st.warning(
                    "Gemini returned an empty response."
                )

        except Exception as e:

            st.error("❌ Gemini API Error")
            st.code(str(e))
