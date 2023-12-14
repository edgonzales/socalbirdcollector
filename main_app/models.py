from django.db import models
from django.urls import reverse


# you can access the cat with cat_set when you have toy
class House(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('houses_detail', kwargs={'pk': self.id})

# Create your models here.
class Bird(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    houses = models.ManyToManyField(House)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'bird_id': self.id})
    
# A tuple of 2-tuples
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)


class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
        )
    
    # Create a cat_id FK
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']