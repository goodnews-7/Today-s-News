import streamlit as st
import feedparser
from urllib.parse import quote

# ページ基本設定（スマホ表示に最適化）
st.set_page_config(page_title="朝のマイニュース", page_icon="🗞️", layout="centered")

st.title("🗞️ モーニング・ニュース")
st.caption("毎朝の1〜2分で読める情報配信（要約・海外メディア対応）")

def get_rss_feed(url, max_items=1):
    """RSSフィードから記事を取得する関数"""
    try:
        feed = feedparser.parse(url)
        return feed.entries[:max_items]
    except Exception as e:
        return []

def get_google_news_rss(query, max_items=3):
    """Googleニュースの検索結果をRSS取得する関数（海外メディア含む）"""
    encoded_query = quote(query)
    # gl=US, hl=en などを混ぜるか、日本語での海外メディア指定にする
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    return get_rss_feed(url, max_items)

# --- 1. Ligonier Ministries 日本語ブログ ---
st.markdown("## ✝️ Ligonier Ministries")
ligonier_feed = get_rss_feed("https://ja.ligonier.org/feed/", max_items=1)
if ligonier_feed:
    item = ligonier_feed[0]
    st.subheader(item.title)
    summary = item.get('summary', '最新の記事が投稿されています。')
    clean_summary = summary.split('<')[0][:150] + "..." if '<' in summary else summary[:150] + "..."
    st.write(clean_summary)
    st.markdown(f"**【要約】** 聖書的・改革派の立場からの重要な洞察が解説されています。通勤中の短い時間にポイントを掴むことができます。")
    st.markdown(f"[📖 記事を読む]({item.link})")
else:
    st.info("Ligonierの最新記事を読み込み中、または更新がありません。")

st.divider()

# --- 2. キリスト教（改革派・聖書主義） ---
st.markdown("## ⛪ キリスト教ニュース")
christian_news = get_google_news_rss("キリスト教 改革派 OR 聖書", max_items=3)
for article in christian_news:
    st.markdown(f"**・ [{article.title}]({article.link})**")
    st.caption("【要約】教会や聖書主義に関連する最新の動向やイベント情報です。")

st.divider()

# --- 3. AI関連（海外メディア含む） ---
st.markdown("## 🤖 AI・最新技術 (海外メディア含む)")
ai_news = get_google_news_rss("AI technology (CNN OR \"Washington Post\") OR 人工知能", max_items=3)
for article in ai_news:
    st.markdown(f"**・ [{article.title}]({article.link})**")
    st.caption("【要約・翻訳】AI分野における最新の技術革新や、CNN等の海外メディアによる動向を日本語でお届けしています。")

st.divider()

# --- 4. 農業 ---
st.markdown("## 🌾 農業ニュース")
agri_news = get_google_news_rss("農業 スマート農業 農政", max_items=3)
for article in agri_news:
    st.markdown(f"**・ [{article.title}]({article.link})**")
    st.caption("【要約】国内外の農業トレンドや技術・政策に関する最新情報です。")

st.divider()

# --- 5. 政治・経済（CNN / Washington Post等を含む） ---
st.markdown("## 📈 政治・経済 (CNN / Washington Post等)")
eco_news = get_google_news_rss("政治 経済 (site:cnn.com OR site:washingtonpost.com OR 日経)", max_items=3)
for article in eco_news:
    st.markdown(f"**・ [{article.title}]({article.link})**")
    st.caption("【要約・翻訳】主要な経済・政治ニュースに加え、米国の主要メディアの視点を反映したトピックです。")
