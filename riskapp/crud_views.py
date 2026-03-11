from django.http import JsonResponse, HttpResponseNotAllowed, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
import json

from .models import PredictionRecord

def record_to_dict(record: PredictionRecord):
    return {
        "id": record.id,
        "created_at": record.created_at.isoformat(),
        "answers": record.answers_json,
        "risk_score": record.risk_score,
        "risk_band": record.risk_band,
        "model_version": record.model_version,
        "notes": record.notes,
    }

@csrf_exempt
def prediction_list(request):
    # READ all + CREATE
    if request.method == "GET":
        records = PredictionRecord.objects.order_by("-created_at")[:50]
        data = [record_to_dict(r) for r in records]
        return JsonResponse(data, safe=False, status=200)

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        record = PredictionRecord.objects.create(
            answers_json=body.get("answers", {}),
            risk_score=body.get("risk_score", 0.0),
            risk_band=body.get("risk_band", "moderate"),
            model_version=body.get("model_version", "logreg_v1"),
            notes=body.get("notes", ""),
        )
        return JsonResponse(record_to_dict(record), status=201)

    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def prediction_detail(request, pk):
    # READ one + UPDATE + DELETE
    try:
        record = PredictionRecord.objects.get(pk=pk)
    except PredictionRecord.DoesNotExist:
        raise Http404("PredictionRecord does not exist")

    if request.method == "GET":
        return JsonResponse(record_to_dict(record), status=200)

    if request.method in ["PUT", "PATCH"]:
        try:
            body = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # allow updating notes and risk_band to simulate review
        if "notes" in body:
            record.notes = body["notes"]
        if "risk_band" in body:
            record.risk_band = body["risk_band"]
        if "risk_score" in body:
            record.risk_score = body["risk_score"]
        if "answers" in body:
            record.answers_json = body["answers"]

        record.save()
        return JsonResponse(record_to_dict(record), status=200)

    if request.method == "DELETE":
        record.delete()
        return JsonResponse({"deleted": True}, status=204)

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])
