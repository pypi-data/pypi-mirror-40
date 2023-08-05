from biography.models import Quote
from rest_framework import serializers


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        exclude = ('biography',)
