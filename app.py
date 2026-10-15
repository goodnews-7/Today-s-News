import streamlit as st
import feedparser
from urllib.parse import quote

# ページ基本設定（スマホ表示に最適化）
st.set_page_config(page_title="朝のマイニュース", page_icon="🗞️", layout="centered")

st.title("🗞️ モーニング・ニュース")
st.caption("毎朝の1〜2分で読める情報配信（要約・海外メディア対応）")

# キャッシュを無効化して常に最新データを取得するための更新ボタン
if st.button("🔄 最新ニュースに更新"):
    st.cache_data.clear()

def get_rss_feed(url, max_items=3):
    """RSSフィードから最新記事を取得する関数"""
    try:
        # キャッシュを回避するためにタイムアウトとパースを設定
        feed = feedparser.parse(url)
        return feed.entries[:max_items]
    except Exception as e:
        return []

def get_google_news_rss(query, max_items=3):
    """Googleニュースの検索結果をRSS取得する関数"""
    encoded_query = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    return get_rss_feed(url, max_items)

def clean_html(text):
    """要約用テキストから不要なHTMLタグ等を取り除く簡便関数"""
    if not text:
        return ""
    # HTMLタグの簡易除去
    clean = text.split('<')[0] if '<' in text else text
    return clean[:120] + "..." if len(clean) > 120 else clean

# --- 1. Ligonier Ministries 日本語ブログ ---
st.markdown("## ✝️ Ligonier Ministries")
ligonier_feed = get_rss_feed("https://ja.ligonier.org/feed/", max_items=1)
if ligonier_feed:
    item = ligonier_feed[0]
    st.subheader(item.title)
    summary_text = item.get('summary', item.get('description', '最新の記事が投稿されています。'))
    st.write(f"**【要約・概要】** {clean_html(summary_text)}")
    st.markdown(f"[📖 記事を読む]({item.link})")
else:
    st.info("Ligonierの最新記事を読み込み中、または更新がありません。[公式サイトへ](https://ja.ligonier.org/)")

st.divider()

# --- 2. キリスト教（改革派・聖書主義） ---
st.markdown("## ⛪ キリスト教ニュース")
christian_news = get_google_news_rss("キリスト教 OR 改革派 OR 聖書", max_items=3)
if christian_news:
    for article in christian_news:
        st.markdown(f"**・ [{article.title}]({article.link})**")
        source_name = article.get('source', {}).get('title', 'ニュース')
        st.caption(f"配信元: {source_name} | {clean_html(article.get('summary', ''))}")
else:
    st.write("最新ニュースを読み込んでいます...")

st.divider()

# --- 3. AI関連（海外情報含む） ---
st.markdown("## 🤖 AI・最新技術 (海外情報含む)")
ai_news = get_google_news_rss("AI OR 人工知能 OR OpenAI OR Claude", max_items=3)
if ai_news:
    for article in ai_news:
        st.markdown(f"**・ [{article.title}]({article.link})**")
        source_name = article.get('source', {}).get('title', 'ニュース')
        st.caption(f"配信元: {source_name} | {clean_html(article.get('summary', ''))}")

st.divider()

# --- 4. 農業 (政策・作況・時事ニュース) ---
st.markdown("## 🌾 農業ニュース (政策・豊不作・時事)")
agri_news = get_google_news_rss("農業 政策 OR 豊作 OR 不作 OR 農水省 OR 作況", max_items=3)
if agri_news:
    for article in agri_news:
        st.markdown(f"**・ [{article.title}]({article.link})**")
        source_name = article.get('source', {}).get('title', 'ニュース')
        st.caption(f"配信元: {source_name} | {clean_html(article.get('summary', ''))}")

st.divider()

# --- 5. 政治と経済 (CNN / 海外主要メディア含む) ---
st.markdown("## 📈 政治・経済 (CNN・国際・国内)")
eco_news = get_google_news_rss("政治 OR 経済 OR CNN OR ワシントン・ポスト", max_items=3)
if eco_news:
    for article in eco_news:
        st.markdown(f"**・ [{article.title}]({article.link})**")
        source_name = article.get('source', {}).get('title', 'ニュース')
        st.caption(f"配信元: {source_name} | {clean_html(article.get('summary', ''))}")
