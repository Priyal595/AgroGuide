import requests
from django.http import JsonResponse
import os
from datetime import datetime, timedelta

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def agro_news(request):
    try:
        if not NEWS_API_KEY:
            return JsonResponse({"error": "API key not configured"}, status=500)

        from django.core.cache import cache
        cached_news = cache.get("agro_news")
        if cached_news:
            return JsonResponse(cached_news)

        from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

        query = (
            "(agriculture OR farming OR agronomy OR crop OR livestock OR irrigation) "
            "AND (farmer OR crops OR soil OR harvest OR yield)"
        )

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "from": from_date,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": 30,
            "apiKey": NEWS_API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "ok":
            return JsonResponse({"error": data.get("message")}, status=400)

        primary_keywords = [
            'farmer', 'crop', 'soil', 'livestock',
            'harvest', 'irrigation', 'yield'
        ]

        filtered_articles = []
        for article in data.get("articles", []):
            title = (article.get("title") or "").lower()
            desc = (article.get("description") or "").lower()
            content = title + " " + desc

            if any(word in content for word in primary_keywords):
                filtered_articles.append({
                    "title": article.get("title"),
                    "description": article.get("description") or "",
                    "url": article.get("url"),
                    "image": article.get("urlToImage") or "https://via.placeholder.com/400x250",
                    "source": article.get("source", {}).get("name"),
                    "published": article.get("publishedAt"),
                })

        result = {"news": filtered_articles[:6]}
        cache.set("agro_news", result, timeout=3600)

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)