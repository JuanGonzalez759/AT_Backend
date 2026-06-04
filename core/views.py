from django.http import JsonResponse


def cors_test(request):
    return JsonResponse({'ok': True, 'path': request.path})
