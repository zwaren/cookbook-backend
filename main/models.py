from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    description = models.TextField()
    ingredients = models.TextField()


class RecipeStep(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    image = models.URLField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

