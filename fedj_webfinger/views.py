from http import HTTPStatus
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse

from fedj_webfinger.models import Resource, Alias

def webfinger_index(request: HttpRequest):
    if request.method != "GET":
        return HttpResponseForbidden()
    
    if "resource" not in request.GET:
        return JsonResponse({"error": "missing 'resource' query param"}, status=HTTPStatus.BAD_REQUEST)
    
    resource = request.GET["resource"]

    try:
        subject = Resource.objects.get(uri=resource)
    except:
        return JsonResponse({
            "message": "resource not found"
        }, status=HTTPStatus.NOT_FOUND)

    aliases = Alias.objects.all().filter(account=subject)
    return JsonResponse({
        "subject": subject.uri,
        "aliases": [alias.value for alias in aliases]
    },
    # headers={"Content-Type": "application/jrd+json"}
    )