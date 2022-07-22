from flask import Response

def response_dispatcher(request, router):
    print(f"post_handler: handling request. request = {request}")

    if not request.data:
        print("post_handler: received empty request")
        return Response(status=200)

    print(f"post_handler: slack payload: {request.json}")
    if "challenge" in request.json:
        print("post_handler: resolving challenge")
        return request.json["challenge"]

    return router(request)