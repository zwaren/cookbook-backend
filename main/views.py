from rest_framework.generics import ListCreateAPIView

from .models import RecipeStep, Recipe
from .serializers import RecipeStepSerializer, RecipeSerializer


class RecipeList(ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeStepList(ListCreateAPIView):
    queryset = RecipeStep.objects.all()
    serializer_class = RecipeStepSerializer