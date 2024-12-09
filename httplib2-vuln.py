import httplib2
from rest_framework.decorators import api_view

@api_view(["GET", "POST"])
async def snippet_list(request):
    tainted = request.GET["query"]

    tainted_url = "https://" + tainted

    body = "Test123"
    headers = {
        'Foo': 'Bar'
    }

    h = httplib2.Http()
    # ruleid: tainted-django-http-request-httplib2
    resp, content = h.request(uri=tainted)

    # ruleid: tainted-django-http-request-httplib2
    resp, content = h.request(tainted_url, "POST", body=body, headers=headers)

    # ok: tainted-django-http-request-httplib2
    resp, content = h.request("https://semgrep.dev")
