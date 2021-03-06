import json

from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from websocket import create_connection

from .models import File, Recipe, RecipeStep, Note
from .serializers import FileSerializer, RecipeSerializer, RecipeStepSerializer, NoteSerializer


def ws(data):
    ws = create_connection("wss://cookback-ws.herokuapp.com/")
    ws.send(data)
    ws.close()


class RecipeList(ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        ws(json.dumps({
            "type": "recipe",
            "data": response.data
        }))
        return response

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get('q')

        if q is not None:
            return qs.annotate(search=SearchVector('name', 'description', 'ingredients')) \
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


class VkHook(APIView):
    queryset = Recipe.objects.all()

    def post(self, request):
        if request.data.get('type') == "confirmation" and request.data.get("group_id") == 188793599:
            return HttpResponse('b7b7bd24')

        label = request.data.get('object').get('body').split('\n')
        if label[0] == "create":
            recipe = { "name": label[1], "image": label[2], "description": label[3], "ingredients": label[4] }
            serializer = RecipeSerializer(data=recipe)

            if serializer.is_valid(raise_exception=True):
                recipe = serializer.save()

            ws(json.dumps({
                "type": "post",
                "data": request.data
            }))

            ws(json.dumps({
                "type": "recipe",
                "data": recipe
            }))

        elif label[0] == "update":
            recipe = Recipe.objects.get(id=int(label[1]))

            recipe.name = label[2]
            recipe.image = label[3]
            recipe.description = label[4]
            recipe.ingredients = label[5]
            recipe.save()

            ws(json.dumps({
                "type": "post",
                "data": request.data
            }))

            ws(json.dumps({
                "type": "recipe",
                "data": recipe
            }))

        return HttpResponse('ok', content_type="text/plain", status=200)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
