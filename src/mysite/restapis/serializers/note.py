from rest_framework import serializers

from ..models import Note

class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model   = Note
        fields  = '__all__'
