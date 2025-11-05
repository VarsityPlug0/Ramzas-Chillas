from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views import View
import os
from django.conf import settings

class FrontendAppView(View):
    """
    Serves the React frontend application
    """
    
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        # For API routes, let Django handle them normally
        if request.path.startswith('/api/'):
            # This shouldn't happen as API routes are defined separately
            return HttpResponse("API route", status=404)
        
        # For all other routes, serve the React app
        # This allows React Router to handle client-side routing
        try:
            return render(request, 'frontend/index.html')
        except Exception as e:
            # If the template doesn't exist, return a simple HTML shell
            return HttpResponse("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Ramza's Chillas</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
                <div id="root">
                    <h1>Ramza's Chillas</h1>
                    <p>Loading application...</p>
                </div>
            </body>
            </html>
            """, content_type="text/html")

# Fallback view for serving the React app
def serve_react_app(request):
    """
    Serve the React frontend application
    """
    try:
        return render(request, 'frontend/index.html')
    except Exception as e:
        # Return a simple HTML shell if template not found
        return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ramza's Chillas</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <div id="root">
                <h1>Ramza's Chillas</h1>
                <p>Loading application...</p>
            </div>
        </body>
        </html>
        """, content_type="text/html")