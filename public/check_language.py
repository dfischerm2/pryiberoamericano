from django.http import JsonResponse
from django.utils.translation import get_language

def check_language(request):
    return JsonResponse({
        "current_language": get_language(),
        "session_language": request.session.get('django_language'),
        "cookie_language": request.COOKIES.get('django_language')
    })