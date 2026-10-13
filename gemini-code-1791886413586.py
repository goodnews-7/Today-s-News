import streamlit as st
import feedparser
from urllib.parse import quote

# ページ基本設定（スマホ表示に最適化）
st.set_page_config(page_title="朝のマイニュース", page_icon="🗞️", layout="centered")

st.title("🗞️ モーニング・ニュース")
st.caption("毎朝の1〜2分で読める情報配信")

def get_rss_feed(url, max_items=3):
    """RSSフィードから記事を取得する関数"""
    try:
        feed = feedparser.parse(url)
        return feed.entries[:max_items]
    except Exception as e:
        return []

def get_google_news_rss(query, max_items=3):
    """Googleニュースの検索結果をRSS取得する関数"""
    encoded_query = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    return get_rss_feed(url, max_items)

# --- 1. Ligonier Ministries 日本語ブログ ---
st.markdown("## ✝️ Ligonier Ministries")
ligonier_feed = get_rss_feed("https://ja.ligonier.org/feed/", max_items=1)
if ligonier_feed:
    item = ligonier_feed[0]
    st.subheader(item.title)
    # 簡易的な要約・概要表示
    summary = item.get('summary', '最新の記事が投稿されています。')
    # タグ等の除去と短縮
    clean_summary = summary.split('<')[0][:150] + "..." if '<' in summary else summary[:150] + "..."
    st.write(clean_summary)
    st.markdown(f"[📖 記事を読む]({item.link})")
else:
    st.info("Ligonierの最新記事を読み込み中、または更新がありません。[公式サイトへ](https://ja.ligonier.org/)")

st.divider()

# --- 2. キリスト教（改革派・聖書主義） ---
st.markdown("## ⛪ キリスト教ニュース")
christian_news = get_google_news_rss("キリスト教 改革派 OR 聖書", max_items=3)
for article in christian_news:
    st.markdown(f"**・ [{article.title}]({article.link})**")
    st.caption(f"配信元: {article.get('source', {}).get('title', 'ニュース')}")

st.divider()

# --- 3. AI関連 ---
st.markdown("## 🤖 AI・最新技術")
ai_news = get_google_news_rss("AI 人工知能 最新", max_items=3)
for article in ai_news:
    st.markdown(f"**・ [{article.title}]({article.link})**")
    st.caption(f"配信元: {article.get('source', {}).get('title', 'ニュース')}")

st.divider()

# --- 4. 農業 ---
st.markdown("## 🌾 農業ニュース")
agri_news = get_google_news_rss("農業 スマート農業 農政", max_items=3)
for article in agri_news:
    st.markdown(f"**・ [{article.title}]({article.link})**")
    st.caption(f"配信元: {article.get('source', {}).get('title', 'ニュース')}")

st.divider()

# --- 5. 政治と経済 ---
st.markdown("## 📈 政治・経済")
eco_news = get_google_news_rss("政治 経済 日本", max_items=3)
for article in eco_news:
    st.markdown(f"**・ [{article.title}]({article.link})**")
    st.caption(f"配信元: {article.get('source', {}).get('title', 'ニュース')}")