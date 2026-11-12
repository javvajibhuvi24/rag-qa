import streamlit as st

from answer import answer_with_sources

st.set_page_config(page_title="Loan FAQ Assistant", page_icon="💬")
st.title("Loan FAQ Assistant")
st.caption("Answers come only from a small sample FAQ. Built with sentence-transformers and the Gemini API.")

question = st.text_input("Ask a question about personal loans")

if question:
    with st.spinner("Searching..."):
        reply, sources = answer_with_sources(question)
    st.write(reply)
    if sources:
        with st.expander("Sources used"):
            for score, chunk in sources:
                st.markdown(f"**{score:.2f}** · {chunk['source']}")
                st.write(chunk["text"])