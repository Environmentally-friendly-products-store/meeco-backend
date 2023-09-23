from rest_framework import serializers

from .models import Event


class FullEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "image",
            "discount",
            "date_start",
            "date_end",
            "slug",
        )


class ShortEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "image",
            "discount",
            "date_start",
            "date_end",
        )
