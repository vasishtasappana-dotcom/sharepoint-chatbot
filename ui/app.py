import streamlit as st, requests, os

st.set_page_config(page_title="Chatbot (Demo)")
st.title("SharePoint Chatbot — Demo")

api_url = os.getenv("API_URL", "http://api:8080")  # in-cluster default

if "chat" not in st.session_state:
    st.session_state.chat = []

for role, msg in st.session_state.chat:
    st.chat_message(role).write(msg)

q = st.chat_input("Ask a question about the docs")
if q:
    st.session_state.chat.append(("user", q))
    try:
        r = requests.post(f"{api_url}/chat", json={"message": q}, timeout=30)
        a = r.json()
        answer = a.get("answer", "")
        sources = "\n".join([f"- {s['title']}" for s in a.get("sources", [])])
        out = answer + ("\n\n**Sources**\n" + sources if sources else "")
    except Exception as e:
        out = f"Error calling API: {e}"
    st.session_state.chat.append(("assistant", out))
    st.chat_message("assistant").write(out)
