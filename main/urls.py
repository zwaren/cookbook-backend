from django.urls import path

from . import views

urlpatterns = [
    path('recipes', views.RecipeList.as_view()),
    path('recipe_steps', views.RecipeStepList.as_view()),
]
