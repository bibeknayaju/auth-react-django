from rest_framework import generics, permissions
from .serializers import UserSerializer, RegisterUserSerializer, LoginSerializer
from knox.models import AuthToken
from rest_framework.response import Response

# Register api


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = str(AuthToken.objects.create(user))

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': token
        })

# login api


# class LoginAPI(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data

#         # token = str(AuthToken.objects.create(user))
#         token = str(AuthToken.objects.create(user).key)
#         # token = token_str.split(": ")[-1].strip("')")

#         print("token here", token)
#         return Response({
#             'user': UserSerializer(user, context=self.get_serializer_context()).data,
#             'token': token
#         })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token_obj, created = AuthToken.objects.create(user)
        token_str = str(token_obj)
        token = token_str.split(": ")[0].strip("')")

        print("token here:", token)
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': token
        })
# user api


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
