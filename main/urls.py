from django.urls import path

from . import views

urlpatterns = [
    path('recipes', views.RecipeList.as_view()),
    path('recipe_steps', views.RecipeStepList.as_view()),
    path('upload', views.FileUploadView.as_view()),
    path('vk', views.VkHook.as_view()),
    path('notes', views.NoteViewSet.as_view({'get': 'list', 'post': 'create'})),
]
