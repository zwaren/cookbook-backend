from django.contrib.postgres.search import SearchVector
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import File, Recipe, RecipeStep
from .serializers import FileSerializer, RecipeSerializer, RecipeStepSerializer


class RecipeList(ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get('q')

        if q is not None:
            return qs.select_related('author') \
            .annotate(search=SearchVector('name', 'description', 'ingredients')) \
            .filter(search=q)

        return Recipe.objects.all()


class RecipeStepList(ListCreateAPIView):
    queryset = RecipeStep.objects.all()
    serializer_class = RecipeStepSerializer


class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

      file_serializer = FileSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
