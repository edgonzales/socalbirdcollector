# main_app/views.py
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Bird, House, Photo

from .forms import FeedingForm

import boto3
import uuid
import os

# Add this cats list below the imports
# birds = [
#   {'name': 'Novie', 'breed': 'turkey vulture', 'description': 'furry little demon', 'age': 3},
#   {'name': 'Woody', 'breed': 'acorn woodpecker', 'description': 'gentle and loving', 'age': 2},
# ]

def add_photo(request, bird_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = f"socalbirdcollector/{uuid.uuid4().hex[:6]}{photo_file.name[photo_file.name.rfind('.'):]}"
    try:
      bucket = os.environ['BUCKET_NAME']
			# upload to aws, file, bucket name, where you want to store it in bucket
      s3.upload_fileobj(photo_file, bucket, key)
			# build the url to save to the database
      photo_url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
			# save the url to the Photo Model
      Photo.objects.create(url=photo_url, bird_id=bird_id)

    except Exception as e:
      print('An error uploading to AWS')
      print(e)
  return redirect('detail', bird_id=bird_id)

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
