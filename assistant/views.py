
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rag.api_service import ask_assistant
import json

@csrf_exempt
def assistant_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        body = json.loads(request.body)
        question = body.get("query")
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not question:
        return JsonResponse({"error": "Query is required"}, status=400)

    answer = ask_assistant(question)

    return JsonResponse({
        "query": question,
        "answer": answer
    })