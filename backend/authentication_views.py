from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from . import permissions as custom_permissions
from . import serializers as custom_serializers
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from . import models as custom_models
from rest_framework import viewsets
from rest_framework import status
from .tasks import Email


# Get User API
class UserAPI(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = custom_serializers.VibroUserSerializer

    def get_object(self):
        """
        get user object
        """

        return self.request.user


# Register API
class RegisterAPI(generics.GenericAPIView):

    serializer_class = custom_serializers.RegisterVibroUserSerializer

    def post(self, request, *args, **kwargs):
        """
        create a new user and respond accoringly to user.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Email.delay('register', request)
        refresh = RefreshToken.for_user(self.request.user)
        return Response({
            "user": custom_serializers.VibroUserSerializer(
                user,
                context=self.get_serializer_context()).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })


class RegisterAdminAPI(generics.GenericAPIView):

    permission_classes = [custom_permissions.IsSuperUser]
    serializer_class = custom_serializers.RegisterAdminUserSerializer

    def post(self, request, *args, **kwargs):
        """
        create a new user and respond accoringly to user.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Email.delay('register', request)
        refresh = RefreshToken.for_user(self.request.user)
        return Response({
            "user": custom_serializers.VibroUserSerializer(
                user,
                context=self.get_serializer_context()).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })


# Reset API
class ResetAPI(generics.GenericAPIView):

    serializer_class = custom_serializers.ResetSerializer

    def post(self, request, *args, **kwargs):
        """
        confirm existence of user, generate jwt
        for recovery and respond to user accordingly.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = custom_models.VibroUser.objects.filter(
            email=request.data['email']).first()
        if user.exists():
            Email.delay('reset', request)
        else:
            raise NotFound('usuario no encontrado')
        return Response({"detail": f"un correo de recuperacion ha sido enviado a la cuenta {user.blur_email()}"})


# Change Password API
class ChangePassAPI(generics.UpdateAPIView):

    permission_classes = [
        permissions.IsAuthenticated & custom_permissions.IsUpdateMethod
    ]

    serializer_class = custom_serializers.ChangePassSerializer

    def update(self, request, *args, **kwargs):
        """
        Change password of user granted they know their previous password.
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.get_object().check_password(serializer.data.get("password")):
                return Response({"Error": "Contraseña incorrecta"}, status=status.HTTP_400_BAD_REQUEST)
            user = self.get_object()
            try:
                validate_password(serializer.data.get("new_password"))
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            Email.delay('change_password', request)
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": custom_serializers.VibroUserSerializer(
                    user,
                    context=self.get_serializer_context()).data,
                "refresh": str(refresh),
                'access': str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        """
        get user object
        """

        return self.request.user


class ForgotPassAPI(generics.UpdateAPIView):

    permission_classes = [
        permissions.IsAuthenticated & custom_permissions.IsUpdateMethod
    ]

    serializer_class = custom_serializers.ForgotPassSerialiazer

    def update(self, request, *args, **kwargs):
        """
        Change password of user provided they have forgotten their password.
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.get_object()
            try:
                validate_password(serializer.data.get("new_password"))
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("password"))
            user.save()

            Email.delay('change_password', request)
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": custom_serializers.VibroUserSerializer(
                    user,
                    context=self.get_serializer_context()).data,
                "refresh": str(refresh),
                'access': str(refresh.access_token)
            },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        """
        get user object
        """

        return self.request.user


class VibroUserView(viewsets.ModelViewSet):

    permission_classes = [
        custom_permissions.HasUserPermissions
    ]
    serializer_class = custom_serializers.UpdadateUserSerialiazer

    def get_queryset(self):

        id = self.request.query_params.get('id', None)
        user_type = self.request.query_params.get('user_type', None)
        company_name = self.request.query_params.get('company_name', None)
        first_name = self.request.query_params.get('first_name', None)
        last_name = self.request.query_params.get('last_name', None)

        if not (self.request.user.is_superuser or self.request.user.is_staff):
            queryset = custom_models.VibroUser.objects.exclude(
                user_type="Client")
        else:
            queryset = custom_models.VibroUser.objects.all()
        if id:
            queryset = queryset.filter(id=id)
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        if company_name:
            queryset = queryset.filter(company__name__contains=company_name)
        if first_name:
            queryset = queryset.filter(first_name__contains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__contains=last_name)
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if not (request.user.user_type in {"Admin", "Engineer"}):
            serializer.validated_data.pop('certifications', None)
        if not (request.user.is_superuser or request.user.is_staff):
            serializer.validated_data.pop('user_type', None)
            serializer.validated_data.pop('picture', None)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_object(self):
        """
        get user object
        """

        return self.request.user