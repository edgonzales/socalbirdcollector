# main_app/views.py
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Bird, House
from .forms import FeedingForm
from django.shortcuts import render, redirect

# views.py

# Add this cats list below the imports
# birds = [
#   {'name': 'Novie', 'breed': 'turkey vulture', 'description': 'furry little demon', 'age': 3},
#   {'name': 'Woody', 'breed': 'acorn woodpecker', 'description': 'gentle and loving', 'age': 2},
# ]

class BirdCreate(CreateView):
  model = Bird
  fields = ['name', 'breed', 'description', 'age']

class BirdUpdate(UpdateView):
  model = Bird
  # Let's disallow the renaming of a Bird by excluding the name field!
  fields = ['breed', 'description', 'age']

class BirdDelete(DeleteView):
  model = Bird
  success_url = '/birds'


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
    # First, create a list of the toy ids that the cat DOES have
  id_list = bird.houses.all().values_list('id')
  # Now we can query for toys whose ids are not in the list using exclude
  houses_bird_doesnt_have = House.objects.exclude(id__in=id_list)
  feeding_form = FeedingForm()
  return render(request, 'birds/detail.html', {
    'bird': bird, 'feeding_form': feeding_form,
    # Add the houses to be displayed
    'houses': houses_bird_doesnt_have
    })

def add_feeding(request, bird_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the bird_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.bird_id = bird_id
    new_feeding.save()
  return redirect('detail', bird_id=bird_id)


class HouseList(ListView):
  model = House


class HouseDetail(DetailView):
  model = House


class HouseCreate(CreateView):
  model = House
  fields = '__all__'


class HouseUpdate(UpdateView):
  model = House
  fields = ['name', 'color']


class HouseDelete(DeleteView):
  model = House
  success_url = '/houses/'

def assoc_house(request, bird_id, house_id):
  # Note that you can pass a house's id instead of the whole house object
  Bird.objects.get(id=bird_id).houses.add(house_id)
  return redirect('detail', bird_id=bird_id)
