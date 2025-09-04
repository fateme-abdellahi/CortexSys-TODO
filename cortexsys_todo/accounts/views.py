from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .permissions import RegisterPermission


class RegisterView(APIView):

    # all users can access this view
    permission_classes = [RegisterPermission]

    # register a new user with JWT token generation. username, password, password2, email are required.
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        # validate user info
        if serializer.is_valid():
            user = serializer.save()

            # get JWT token for the new user
            token_serializer = TokenObtainPairSerializer(
                data={
                    "username": user.username,
                    "password": request.data.get("password"),
                }
            )
            # add token to response
            if token_serializer.is_valid():
                tokens = token_serializer.validated_data
                return Response({"tokens": tokens}, status=status.HTTP_201_CREATED)

                # user info not valid
            return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # data not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
