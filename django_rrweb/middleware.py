from uuid import uuid4


def session_key_middleware(get_response):
    """Session key middleware"""

    def middleware(request):
        session_key = request.COOKIES.get('rrweb-session-key')

        if session_key is None:
            session_key = str(uuid4())

        response = get_response(request)
        response.set_cookie('rrweb-session-key', session_key)
        return response

    return middleware
