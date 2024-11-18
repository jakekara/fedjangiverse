from http import HTTPStatus
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods
from fedj_webfinger.models import Link, LinkProperty, LinkTitle, Subject, Alias

@require_http_methods(["GET"])
def webfinger_index(request: HttpRequest):
    """View for webfinger. Should be at https://{domain}/.well-known/webfinger"""

    # Make sure the client has supplied the required 'resource'
    # query param and return a helpful message if not
    if "resource" not in request.GET:
        return JsonResponse(
            {"error": "missing 'resource' query param"}, status=HTTPStatus.BAD_REQUEST
        )

    # Get the requested resource
    resource = request.GET["resource"]

    # Get the rel filter, for filtering links, if provided,
    # or else None
    rel = request.GET.get("rel", None)

    # Look up the subject and return a 404 if not found
    try:
        subject = Subject.objects.get(value=resource)
    except:
        return JsonResponse(
            {"message": "resource not found"}, status=HTTPStatus.NOT_FOUND
        )
    
    # Get all the Aliases and serialize them for the HTTP
    # response payload
    aliases = Alias.objects.all().filter(subject=subject)
    serialized_aliases = [alias.value for alias in aliases]

    # Get all the Links and serialize them fo the HTTP
    # response payload
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

        properties: list[LinkProperty] = LinkProperty.objects.filter(link=link)
        for property in properties:
            if "properties" not in serialized_link:
                serialized_link["properties"] = []
            serialized_link["properties"].append({
                property.name: property.value
            })

        serialized_links.append(serialized_link)


    return JsonResponse({
            "subject": subject.value,
            "aliases": serialized_aliases,
            "links": serialized_links
        })
