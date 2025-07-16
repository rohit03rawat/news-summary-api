from rest_framework import serializers
from .models import SavedNews

class SavedNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedNews
        fields = ['id', 'title', 'url', 'summary','source','published_at', 'created_at']
        read_only_fields = ['id', 'created_at']
