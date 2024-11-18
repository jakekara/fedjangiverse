from http import HTTPStatus
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse

from fedj_webfinger.models import Link, LinkTitle, Subject, Alias

def webfinger_index(request: HttpRequest):
    if request.method != "GET":
        return HttpResponseForbidden()

    if "resource" not in request.GET:
        return JsonResponse(
            {"error": "missing 'resource' query param"}, status=HTTPStatus.BAD_REQUEST
        )

    resource = request.GET["resource"]

    rel = request.GET.get("rel", None)

    try:
        subject = Subject.objects.get(value=resource)
    except:
        return JsonResponse(
            {"message": "resource not found"}, status=HTTPStatus.NOT_FOUND
        )
    
    aliases = Alias.objects.all().filter(subject=subject)
    serialized_aliases = [alias.value for alias in aliases]

    links = Link.objects.all().filter(subject=subject)
    # Conditionally filter links by rel param, if provided
    if rel is not None:
        links = links.filter(rel=rel)

    serialized_links = []

    for link in links:
        serialized_link = {
            "rel": link.rel,
            "href": link.href,
            "type": link.type,
        }

        titles: list[LinkTitle] = LinkTitle.objects.filter(link=link)
        for title in titles:
            if "titles" not in serialized_link:
                serialized_link["titles"] = []
            serialized_link["titles"].append({
                title.name: title.value
            }) 

        serialized_links.append(serialized_link)


    return JsonResponse({
            "subject": subject.value,
            "aliases": serialized_aliases,
            "links": serialized_links
        })
