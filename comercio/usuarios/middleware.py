from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica si la vista es de login y el usuario está autenticado
        if request.path == '/usuarios/login/' and request.user.is_authenticated:
            return redirect('/comercio/')  # Cambia 'profile' por la URL de destino

        response = self.get_response(request)
        return response
