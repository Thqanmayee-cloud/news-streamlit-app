import streamlit as st
import requests

st.title("📰 News Dashboard")

api_key = st.text_input("Enter API Key", type="password")

country = st.selectbox("Country", ["us", "in", "gb", "au"])
category = st.selectbox("Category", ["general", "business", "sports", "technology"])
keyword = st.text_input("Search keyword")
limit = st.slider("Number of articles", 1, 20, 10)

if st.button("Fetch News"):

    if not api_key:
        st.error("Please enter API key")
    else:
        url = "https://newsapi.org/v2/top-headlines"

        params = {
            "apiKey": api_key,
            "country": country,
            "category": category,
            "pageSize": limit
        }

        if keyword:
            url = "https://newsapi.org/v2/everything"
            params = {
                "apiKey": api_key,
                "q": keyword,
                "pageSize": limit
            }

        res = requests.get(url, params=params)

        if res.status_code == 200:
            articles = res.json().get("articles", [])

            for a in articles:
                st.subheader(a.get("title"))
                st.write(a.get("description"))
                st.markdown(f"[Read more]({a.get('url')})")
                st.image(a.get("urlToImage") or "")
        else:
            st.error("Error fetching news")
