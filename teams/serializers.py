from rest_framework import serializers

from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    """Serializes Team model"""

    class Meta:
        model = Team
        fields = "__all__"
