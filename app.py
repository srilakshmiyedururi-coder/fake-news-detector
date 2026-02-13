import streamlit as st
import pickle
import re
from newspaper import Article

model = pickle.load(open("fake_news_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

st.set_page_config(page_title="AI Fake News Detector", page_icon="🌐")
st.title("🌐 Smart Fake News Detector")
st.write("వార్త యొక్క **URL (Link)** ఇవ్వండి లేదా **Text** పేస్ట్ చేయండి.")

option = st.radio("Choose Input Type:", ("News URL", "Manual Text"))

user_input = ""

if option == "News URL":
    url = st.text_input("Paste the news link here:")
    if url:
        try:
            article = Article(url)
            article.download()
            article.parse()
            user_input = article.title + " " + article.text
            st.info(f"**Fetched Headline:** {article.title}")
        except:
            st.error("లింక్ నుండి డేటాను తీసుకోలేకపోతున్నాను. దయచేసి సరైన URL ఇవ్వండి.")
else:
    user_input = st.text_area("Paste the news content here:", height=200)

if st.button("Check Authenticity"):
    if len(user_input.split()) < 10:
        st.warning("విశ్లేషించడానికి కనీసం 10 పదాలు ఉండాలి.")
    else:
        cleaned = clean_text(user_input)
        vec = tfidf.transform([cleaned])
        prediction = model.predict(vec)
        
        if prediction[0] == 1:
            st.success("### Result: This news is likely REAL ✅")
            st.balloons()
        else:
            st.error("### Result: This news is likely FAKE 🚩")