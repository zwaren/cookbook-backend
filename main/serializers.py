from rest_framework import serializers

from .models import RecipeStep, Recipe, File

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
