from django.shortcuts import render
from .models import Bird

# views.py

# Add this cats list below the imports
# birds = [
#   {'name': 'Novie', 'breed': 'turkey vulture', 'description': 'furry little demon', 'age': 3},
#   {'name': 'Woody', 'breed': 'acorn woodpecker', 'description': 'gentle and loving', 'age': 2},
# ]


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# Add new view
def birds_index(request):
  # We pass data to a template very much like we did in Express!
  birds = Bird.objects.all()
  return render(request, 'birds/index.html', { 'birds': birds })

def birds_detail(request, bird_id):
  bird = Bird.objects.get(id=bird_id)
  return render(request, 'birds/detail.html', {'bird': bird})