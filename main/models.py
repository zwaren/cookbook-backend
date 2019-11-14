from django.db import models

from django.contrib.postgres.indexes import GinIndex


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    description = models.TextField()
    ingredients = models.TextField()

    class Meta:
        indexes = [GinIndex(fields=['name', 'description', 'ingredients'])]


class RecipeStep(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    image = models.URLField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name
