# from django.contrib.postgres.fields.array import ArrayField
from rest_framework import serializers, fields
from . import models as custom_models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from django.contrib.auth import password_validation
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = custom_models.City
        fields = '__all__'


class DefaultCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = custom_models.Company
        fields = '__all__'


class GetCompanySerializer(serializers.ModelSerializer):

    city = serializers.StringRelatedField()
    # city = serializers.CharField(source="city.name")

    class Meta:
        model = custom_models.Company
        fields = '__all__'


class HierarchySerializer(serializers.ModelSerializer):

    class Meta:
        model = custom_models.Hierarchy
        fields = '__all__'


class ListHierarchySerializer(serializers.ModelSerializer):

    parent = HierarchySerializer()
    company = DefaultCompanySerializer()

    class Meta:
        model = custom_models.Hierarchy
        fields = '__all__'


# User Serializer
class VibroUserSerializer(serializers.ModelSerializer):

    # company = DefaultCompanySerializer(required=False)

    class Meta:
        model = custom_models.VibroUser
        fields = [
            'id',
            'username',
            'first_name',
            "last_name",
            'celphone',
            # 'phone',
            'email',
            'company',
            'user_type',
            'picture',
            'is_active'
        ]


# Register Serializer
class RegisterVibroUserSerializer(serializers.ModelSerializer):

    company = DefaultCompanySerializer(required=False)

    class Meta:
        model = custom_models.VibroUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'company',
            'password',
            # 'phone',
            'celphone',
        ]
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 8}
                        }

    def create(self, validated_data):
        user = custom_models.VibroUser.objects.create_user(**validated_data)
        return user

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value


# Register admin Serializer
class RegisterAdminUserSerializer(serializers.ModelSerializer):

    # company = DefaultCompanySerializer(required=False)
    user_type = serializers.CharField(required=False)

    class Meta:
        model = custom_models.VibroUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'company',
            'password',
            # 'phone',
            'celphone',
            'user_type'
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        user = custom_models.VibroUser.objects.create_user(
            **validated_data)
        return user

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value


# Rest Password Serializer
class ResetSerializer(serializers.Serializer):

    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)

    class Meta:
        model = custom_models.VibroUser
        fields = [
            'id',
            'username',
            'first_name',
            'email',
        ]


# Change Password Serializer
class ChangePassSerializer(serializers.Serializer):

    model = custom_models.VibroUser
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# Change Password Serializer
class ForgotPassSerialiazer(serializers.Serializer):

    model = custom_models.VibroUser
    password = serializers.CharField(required=True)


class UpdadateUserSerialiazer(serializers.ModelSerializer):

    class Meta:
        model = custom_models.VibroUser
        fields = [
            "id",
            'first_name',
            'last_name',
            # 'phone',
            'celphone',
            'email',
            'company',
            'user_type',
            'certifications',
            'picture',
            'is_active'
        ]


class LoginSerializer(TokenObtainPairSerializer):

    # company = DefaultCompanySerializer()

    default_error_messages = {
        'no_active_account':
        _('No se ha encontrado una '
          'cuenta activa con las '
          'credenciales proveidas')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['id'] = self.user.id
        data['username'] = self.user.username
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["celphone"] = self.user.celphone
        # data["phone"] = self.user.phone
        data["email"] = self.user.email
        if self.user.company:
            data["company"] = self.user.company.id
        data["user_type"] = self.user.user_type
        data["is_active"] = self.user.is_active
        request = self.context.get('request')
        data["picture"] = request.build_absolute_uri(self.user.picture.url)
        return data


class MachineSerializer(serializers.ModelSerializer):

    # company = DefaultCompanySerializer()

    class Meta:
        model = custom_models.Machine
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):

    # machine = MachineSerializer()

    class Meta:
        model = custom_models.Sensor
        fields = "__all__"


class GearSerializer(serializers.ModelSerializer):

    # machine = MachineSerializer()

    class Meta:
        model = custom_models.Gear
        fields = "__all__"


class AxisSerializer(serializers.ModelSerializer):

    # gear = GearSerializer()

    class Meta:
        model = custom_models.Axis
        fields = '__all__'


class BearingSerializer(serializers.ModelSerializer):

    # axis = AxisSerializer()

    class Meta:
        model = custom_models.Bearing
        fields = '__all__'


class CouplingSerializer(serializers.ModelSerializer):

    # gear = GearSerializer()

    class Meta:
        model = custom_models.Coupling
        feilds = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):

    # machine = MachineSerializer()
    # engineer_one = VibroUserSerializer()
    # engineer_two = VibroUserSerializer()
    # analyst = VibroUserSerializer()
    # certifier = VibroUserSerializer()
    date = fields.DateField(input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])

    class Meta:
        model = custom_models.Measurement
        fields = '__all__'


# class FlawSerializer(serializers.ModelSerializer):

#     # measurement = MeasurementSerializer()

#     class Meta:
#         model = custom_models.Flaw
#         fields = '__all__'


class TermoImageSerializer(serializers.ModelSerializer):

    # measurement = MeasurementSerializer()

    class Meta:
        model = custom_models.TermoImage
        fields = '__all__'


class PointSerializer(serializers.ModelSerializer):

    # measurement = MeasurementSerializer()

    class Meta:
        model = custom_models.Point
        fields = '__all__'


class ListValuesSerializer(serializers.ModelSerializer):

    point = PointSerializer()
    espectra = serializers.ListField(
        child=serializers.DecimalField(
            decimal_places=2,
            max_digits=4,
            default=0),
        required=False)
    time_signal = serializers.ListField(
        child=serializers.DecimalField(
            decimal_places=2,
            max_digits=4,
            default=0),
        required=False)

    class Meta:
        model = custom_models.Values
        fields = '__all__'


class ValuesSerializer(serializers.ModelSerializer):

    espectra = serializers.ListField(
        child=serializers.DecimalField(
            decimal_places=2,
            max_digits=4,
            default=0),
        required=False)
    time_signal = serializers.ListField(
        child=serializers.DecimalField(
            decimal_places=2,
            max_digits=4,
            default=0),
        required=False)

    class Meta:
        model = custom_models.Values
        fields = '__all__'
