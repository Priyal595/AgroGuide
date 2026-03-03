

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from .services import ChatbotService

service = ChatbotService()

@require_GET
def get_categories(request):
    return JsonResponse(service.get_categories(), safe=False)

@require_GET
def get_questions(request):
    category = request.GET.get("category")
    questions = service.get_questions(category)
    if questions is None:
        return JsonResponse({"error": "Invalid category"}, status=400)
    return JsonResponse({"category": category, "questions": questions})

@csrf_exempt
@require_POST
def get_answer(request):
    try:
        body = json.loads(request.body)
        category = body.get("category")
        question = body.get("question")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    data = service.get_answer(category, question)
    if data is None:
        return JsonResponse({"error": "Invalid category or question"}, status=400)

    return JsonResponse({
        "category": category,
        "answer": data["answer"],
        "related": data["related"]
    })