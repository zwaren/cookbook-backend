from rest_framework import serializers

from .models import RecipeStep, Recipe, File, Note


class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    recipe_steps = RecipeStepSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    nid = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Note
        fields = ['nid', 'title', 'description']
