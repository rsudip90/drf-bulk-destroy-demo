from rest_framework import serializers

class BulkDestroyInstanceSerializer(serializers.Serializer):
    """
    ids of all to be destroyed objects
    """
    ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        write_only=True
    )
