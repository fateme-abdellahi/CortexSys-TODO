from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterView(APIView):
	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
   
			# get JWT token for the new user
			token_serializer = TokenObtainPairSerializer(data={
				'username': user.username,
				'password': request.data.get('password'),
			})
			if token_serializer.is_valid():
				tokens = token_serializer.validated_data
				return Response({"tokens": tokens}, status=status.HTTP_201_CREATED)

            #user info not valid
			return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #data not valid
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
