from rest_framework import serializers

from .models import Product, ImageSet


class ImagePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSet
        fields = ('preview_image',)


class ShortProductSerializer(serializers.ModelSerializer):
    preview_image = ImagePreviewSerializer(read_only=True, source='images')

    class Meta:
        model = Product
        fields = ('id', 'price_per_unit', 'preview_image')