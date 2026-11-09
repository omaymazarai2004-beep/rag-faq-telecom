import streamlit as st

from src.rag import FaqRag

st.set_page_config(page_title="Assistant FAQ télécom", page_icon="📡")
st.title("📡 Assistant FAQ télécom")
st.caption("Posez votre question : la réponse s'appuie sur la base de FAQ.")


@st.cache_resource
def charger():
    return FaqRag()


rag = charger()
k = st.sidebar.slider("Nombre de sources (top-k)", 1, 5, 3)

question = st.chat_input("Votre question…")
if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        res = rag.answer(question, k=k)
        st.write(res["reponse"])
        st.caption(f"Mode : {res['mode']}")
        with st.expander("Sources utilisées"):
            for s in res["sources"]:
                st.markdown(f"**[{s['id']}] {s['question']}** — similarité {s['score']:.2f}")
                st.write(s["reponse"])
