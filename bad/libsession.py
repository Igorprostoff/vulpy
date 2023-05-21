import json
import base64


def create(response, username):
    session = base64.b64encode(json.dumps({'username': username}).encode())
    response.set_cookie('vul_app_session', session)
    return response


def load(request):

    session = {}
    cookie = request.cookies.get('vul_app_session')

    try:
        if cookie:
            decoded = base64.b64decode(cookie.encode())
            if decoded:
                session = json.loads(base64.b64decode(cookie))
    except Exception:
        pass

    return session


def destroy(response):
    response.set_cookie('vul_app_session', '', expires=0)
    return response

