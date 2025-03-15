# working_noban_data/serializers.py

from rest_framework import serializers

# Serializer for endpoints that do not require a custom SQL query.
class CSVQuerySerializer(serializers.Serializer):
    csv = serializers.BooleanField(required=False, default=False)
    page = serializers.IntegerField(
        required=False, min_value=1, 
        help_text="Optional page number for pagination (10 items per page)"
    )

# Serializer for the endpoint that accepts a custom SQL query.
class CustomQuerySerializer(serializers.Serializer):
    query = serializers.CharField(
        required=True, 
        help_text="SQL query to execute on the nobaan database"
    )
    csv = serializers.BooleanField(
        required=False, default=False, 
        help_text="Return result as CSV if true, JSON if false"
    )
    page = serializers.IntegerField(
        required=False, min_value=1, 
        help_text="Optional page number for pagination (10 items per page)"
    )


# New serializer for this endpoint only, adding the date parameter
class BookingQuerySerializer(CSVQuerySerializer):
    date = serializers.DateField(
        required=False,
        help_text="Booking date in YYYY-MM-DD format. Defaults to today if not provided."
    )
    
