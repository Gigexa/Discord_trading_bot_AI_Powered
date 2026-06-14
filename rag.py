from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import feedparser
import numpy as np



class RAG:
    def __init__(self):
        self.feed = feedparser.parse("https://news.ycombinator.com/rss")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def get_news(self,symbol):
        # Fetch news
        feed = feedparser.parse("https://news.ycombinator.com/rss")
        articles = []

        for entry in feed.entries:
            news_id = getattr(
                entry,
                "link",
                entry.title
            )

            articles.append(
                {
                    "id": news_id,
                    "title": entry.title,
                    "link": entry.link,
                }
            )

        news_texts = []

        for item in articles:
            news_texts.append(item['title'])

        return self.build_news_embeddings(news_texts,symbol,articles)

    def build_news_embeddings(self,news_texts,prompt,articles):
        embeddings = self.model.encode(news_texts)
        query_embedding = self.model.encode(prompt)

        scores = util.cos_sim(
            query_embedding,
            embeddings
        )
        return self.get_top_3(scores,articles)

    def get_top_3(self,scores,articles):
        try:
            top_indices = np.argsort(scores[0])[-3:]

            titles_dict = [{'title': articles[i]['title'], 'link': articles[i]['link']} for i in top_indices]
            return titles_dict

        except Exception as e:
            print(e)
            print("something is not okay here ")
            return None
