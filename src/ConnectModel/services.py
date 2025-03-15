from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from AuthModel.models import app_credential
from django.http import JsonResponse
from .models import Connect, CREDENTIAL_TYPES
from UserModel.models import User
from AuthModel.serializers import UserAuthSerializer
from .serializers import ConnectSerializer

@extend_schema(
    description='Create new connection with type and token' + "<br><br> <b>Admin Credential</b>",
    summary='Create new connection for service access',
    methods=['POST'],
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'type': {'type': 'string', 'default':'app', 'enum': [choice[0] for choice in CREDENTIAL_TYPES]},
                'desc': {'type': 'string', 'default': ''},
                'token': {'type': 'string', 'default': ''},
            },
            'required': ['type', 'token']
        }
    },
    responses={
        200: OpenApiResponse(
            response={'return': 'boolean'},
            description='Connection created successfully',
        ),
    },
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def GetorCreateConnection(request):
    try:
        type=request.data.get('type')
        desc=request.data.get('desc', '')
        token=request.data.get('token')
        connection = Connect.create_connect(type=type, desc=desc, token=token)
        return JsonResponse({ 'return': True, 'message': 'Connection created successfully', 'connect': ConnectSerializer(connection).data})
    except Exception as e:
        return JsonResponse({'return': False, 'error': str(e)})
#################################################################################
@extend_schema(
    description='Get all type active connections' + "<br><br> <b>Admin Credential</b>",
    summary='List all type active connections for service access',
    methods=['GET'],
    responses={
        200: OpenApiResponse(
            response={'return': 'boolean'},
            description='List of all active connections',
        ),
    },
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def GetConnections(request):
    try:
        connections = Connect().get_active_connects()
        return JsonResponse({
            'return': True,
            'message': 'Active connections retrieved successfully',
            'connections': ConnectSerializer(connections, many=True).data
        })
    except Exception as e:
        return JsonResponse({
            'return': False,
            'error': str(e)
        })
#################################################################################
@extend_schema(
    description='Get connection all type credentials' + "<br><br> <b>No Credential, need Secret Key</b>",
    summary='get connection credentials',
    methods=['POST'],
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'secret_key': {'type': 'string', 'default': '1@1', 'description': 'secret key is time limited key to access all machines GetCredential api.'},
                'type': {'type': 'string', 'enum': [choice[0] for choice in CREDENTIAL_TYPES]},
                'user_uuid': {'type': 'string', 'format': 'uuid', 'default': '', 'description': 'if type in [user, admin] then need user_uuid'},
            },
            'required': ['secret_key','type']
        }
    },
    responses={
        200: OpenApiResponse(
            response={'return': 'boolean'},
            description='Connection processed successfully',
        ),
    },
)
@api_view(['POST'])
def GetCredential(request):
    try:
        secret_key = request.headers.get('secret_key', '')
        # # if secret_key:
        #     check api key validation
        
        type = request.data.get('type')
        user_uuid = request.data.get('user_uuid', '')
        
        user_credential = {}
        admin_credential = {}
        app_credential = {}
        
        if type in ['user'] and user_uuid:
            user = User.objects.filter(uuid=user_uuid, is_active=True).first()
            user_credential = UserAuthSerializer(user.auth()).data 
            
        if type in ['admin'] and user_uuid:
            user = User.objects.filter(uuid=user_uuid, is_superuser=True, is_active=True).first()
            admin_credential = UserAuthSerializer(user.auth()).data
        
        elif type in ['app']:
            Connects = Connect.get_active_connects()
            connect = Connects.filter(type=type).first()
            app_credential = ConnectSerializer(connect).data
            
        return JsonResponse({'return': True, 'message': 'Connection processed successfully.',
                             'user_credential': user_credential,
                             'admin_credential': admin_credential,
                             'app_credential': app_credential})
    except Exception as e:
        return JsonResponse({'return': False, 'error': str(e)})
