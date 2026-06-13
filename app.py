import streamlit as st
import requests
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="News Dashboard", layout="wide")

BASE_URL = "https://newsapi.org/v2/top-headlines"

# -----------------------------
# SIDEBAR - INPUTS
# -----------------------------
st.sidebar.title("📰 News Filters")

api_key = st.sidebar.text_input("Enter News API Key", type="password")

country = st.sidebar.selectbox(
    "🌍 Select Country",
    ["us", "in", "gb", "au", "ca", "de", "fr", "jp", "sg"]
)

category = st.sidebar.selectbox(
    "📂 Select Topic",
    ["general", "business", "entertainment", "health", "science", "sports", "technology"]
)

keyword = st.sidebar.text_input("🔎 Keyword Search")

article_count = st.sidebar.slider("📊 Number of Articles", 1, 50, 10)

fetch_button = st.sidebar.button("🚀 Fetch News")

# -----------------------------
# FUNCTION TO FETCH NEWS
# -----------------------------
def fetch_news(api_key, country, category, keyword, limit):
    params = {
        "apiKey": api_key,
        "country": country,
        "category": category,
        "pageSize": limit
    }

    # If keyword exists, switch to "everything" endpoint logic
    if keyword:
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": api_key,
            "q": keyword,
            "pageSize": limit,
            "sortBy": "publishedAt"
        }
    else:
        url = BASE_URL

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None, response.json().get("message", "Error fetching news")

    return response.json().get("articles", []), None

# -----------------------------
# MAIN UI
# -----------------------------
st.title("🗞️ Advanced News Dashboard")
st.write("Fetch real-time news with filters for topic, location, and keywords.")

if fetch_button:
    if not api_key:
        st.error("⚠️ Please enter API key")
    else:
        with st.spinner("Fetching latest news..."):
            articles, error = fetch_news(
                api_key, country, category, keyword, article_count
            )

        if error:
            st.error(f"Error: {error}")
        else:
            if not articles:
                st.warning("No articles found.")
            else:
                st.success(f"Found {len(articles)} articles")

                for i, article in enumerate(articles):
                    st.markdown("---")

                    title = article.get("title", "No Title")
                    description = article.get("description", "No description available")
                    url = article.get("url", "#")
                    image = article.get("urlToImage")

                    col1, col2 = st.columns([1, 3])

                    with col1:
                        if image:
                            st.image(image, use_container_width=True)

                    with col2:
                        st.subheader(title)
                        st.write(description)
                        st.markdown(f"🔗 [Read Full Article]({url})")

                        published = article.get("publishedAt", "")
                        if published:
                            st.caption(f"🕒 {published}")

st.markdown("---")
st.caption("Built with Streamlit + NewsAPI")
