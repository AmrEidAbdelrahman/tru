from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey

from rest_framework.response import Response
from rest_framework import status, throttling
from rest_framework_api_key.permissions import HasAPIKey

from core_manager.models import APICallLog
from core_manager.utils import validate_and_extract_national_id


class NationalIDRateThrottle(throttling.UserRateThrottle):
    """Custom rate throttle for national ID validation endpoint."""
    scope = 'national_id'

class NationalIDValidatorView(APIView):
    """
    API endpoint for validating and extracting information from Egyptian national IDs.
    Requires API key authentication and is rate-limited per key.
    """
    permission_classes = [HasAPIKey]
    throttle_classes = [NationalIDRateThrottle]

    def post(self, request):
        """
        Validate the provided national ID and extract information if valid.
        Logs each API call with the result and associated API key.
        """
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = APIKey.objects.get_from_key(key)
        national_id = request.data.get('national_id')
        result = validate_and_extract_national_id(national_id)
        APICallLog.objects.create(
            api_key=api_key,
            national_id=national_id or '',
            is_valid=result['is_valid'],
            extracted_data=result['data'] if result['is_valid'] else None,
            response_status=status.HTTP_200_OK if result['is_valid'] else status.HTTP_400_BAD_REQUEST
        )
        if result['is_valid']:
            return Response(result['data'], status=status.HTTP_200_OK)
        else:
            return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)

