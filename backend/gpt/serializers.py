from rest_framework import serializers

class InputGPTSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)
