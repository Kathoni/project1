from django.shortcuts import render

# Create your views here.
def dashboard(request):
    """
    Render the dashboard view.
    """
    return render(request, 'dashboard.html')