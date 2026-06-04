from django.utils.deprecation import MiddlewareMixin


class DebugCorsMiddleware(MiddlewareMixin):
    """Temporary middleware for debugging CORS issues in production.

    This adds permissive Access-Control headers when an Origin header is present.
    Remove this middleware after diagnosing the issue.
    """
    def process_response(self, request, response):
        origin = request.META.get('HTTP_ORIGIN')
        if origin:
            response.setdefault('Access-Control-Allow-Origin', origin)
            response.setdefault('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
            response.setdefault('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            response.setdefault('Access-Control-Allow-Credentials', 'true')
        return response
