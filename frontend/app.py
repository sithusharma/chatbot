import streamlit as st
import requests

# Page Title and Introduction
st.title("HR Document Chatbot 💬")
st.markdown("""
This is a **demo** of an internal HR chatbot designed to answer questions based on company policy documents.
It retrieves the most relevant sections from HR policies and generates a clear, professional response.
""")

# Add GitHub link for transparency
st.markdown("""
[🔗 View Source Code on GitHub](https://github.com/sithusharma/chatbot)
""")

# Input Field
query = st.text_input("Ask a question about HR policies:")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Please wait... Processing your query. This may take a few seconds."):
            try:
                response = requests.get("http://localhost:8000/search", params={"query": query})
                response.raise_for_status()

                # Expecting backend to return {"response": "Your nice response here"}
                result = response.json()
                full_response = result.get("matches", "No response found.")

                # Clean up and present nicely (remove \n, {}, or unnecessary formatting if any)
                cleaned_response = full_response.replace("\\n", "\n").strip("{}").strip()

                st.success("Here’s the response from the HR chatbot:")
                st.write(cleaned_response)

            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Failed to contact backend: {e}")
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")
