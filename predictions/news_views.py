import requests
from django.http import JsonResponse
import os
from datetime import datetime, timedelta

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def agro_news(request):
    try:
        from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

        #Using AND logic to ensure climate/weather terms 
        # are tied to agriculture specifically.
        query = (
            "(agriculture OR farming OR agronomy OR 'crop yield' OR livestock OR "
            "horticulture OR 'agri-tech' OR 'sustainable farming' OR irrigation) "
            "AND (farmer OR crops OR harvest OR soil OR agribusiness)"
        )

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "from": from_date,
            "sortBy": "relevance", # Changed from popularity to prioritize your keywords
            "language": "en",
            "pageSize": 40,        # Fetch more initially to filter them down
            "apiKey": NEWS_API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "ok":
            return JsonResponse({"error": data.get("message")}, status=400)

        # We define "Must-Have" keywords to exclude generic climate/political news
        primary_sector_keywords = [
            'farm', 'crop', 'soil', 'livestock', 'agriculture', 'agri', 
            'harvest', 'irrigation', 'yield', 'cultivation', 'cattle'
        ]
        
        filtered_articles = []
        for article in data.get("articles", []):
            title = (article.get("title") or "").lower()
            desc = (article.get("description") or "").lower()
            content = title + " " + desc

            # Check if at least one primary sector keyword is in the title or description
            if any(word in content for word in primary_sector_keywords):
                filtered_articles.append({
                    "title": article.get("title"),
                    "description": article.get("description") or "",
                    "url": article.get("url"),
                    "image": article.get("urlToImage") or "",
                    "source": article.get("source", {}).get("name"),
                    "published": article.get("publishedAt"),
                })

        # Return the top 6 most relevant filtered results
        return JsonResponse({"news": filtered_articles[:6]})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)