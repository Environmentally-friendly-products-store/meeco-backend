from core.serializers import SLUG_MODEL_FIELDS, SlugModelSerializer
from events.models import Event


class ShortEventSerializer(SlugModelSerializer):
    class Meta(SlugModelSerializer.Meta):
        model = Event


class FullEventSerializer(ShortEventSerializer):
    class Meta(ShortEventSerializer.Meta):
        fields = SLUG_MODEL_FIELDS + (
            "id",
            "description",
            "discount",
            "date_end",
        )


class EventSerializer(ShortEventSerializer):
    class Meta(ShortEventSerializer.Meta):
        fields = SLUG_MODEL_FIELDS + (
            "id",
            "description",
            "image",
            "discount",
            "date_start",
            "date_end",
        )
