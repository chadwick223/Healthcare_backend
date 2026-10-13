from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Doctor, Patient


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    def validate_email(self, value):
        email = value.lower().strip()
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def create(self, validated_data):
        name = validated_data.get('name').strip()
        email = validated_data.get('email').lower().strip()
        password = validated_data.get('password')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email', '').lower().strip()
        password = attrs.get('password')

        user = (
            User.objects.filter(email__iexact=email).first()
            or User.objects.filter(username__iexact=email).first()
        )

        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("This user account is inactive.")

        refresh = RefreshToken.for_user(user)

        return {
            'user': user,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class PatientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150, required=True)
    age = serializers.IntegerField(min_value=0, max_value=150, required=True)
    gender = serializers.CharField(max_length=10, required=True)
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True, default='')
    address = serializers.CharField(required=False, allow_blank=True, default='')
    medical_history = serializers.CharField(required=False, allow_blank=True, default='')
    created_by = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_created_by(self, obj):
        if obj.created_by.first_name:
            return obj.created_by.first_name
        return obj.created_by.username

    def validate_gender(self, value):
        gender = value.strip().upper()

        if gender in ['M', 'MALE']:
            return 'M'
        elif gender in ['F', 'FEMALE']:
            return 'F'
        elif gender in ['O', 'OTHER']:
            return 'O'
        else:
            raise serializers.ValidationError("Gender must be 'M' (Male), 'F' (Female), or 'O' (Other).")

    def create(self, validated_data):
        return Patient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.medical_history = validated_data.get('medical_history', instance.medical_history)
        instance.save()
        return instance


# Backward compatibility alias
PatientCreateSerializer = PatientSerializer


class DoctorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150, required=True)
    specialization = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True, default='')
    experience_years = serializers.IntegerField(min_value=0, required=False, default=0)
    created_by = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_created_by(self, obj):
        if obj.created_by.first_name:
            return obj.created_by.first_name
        return obj.created_by.username

    def validate_email(self, value):
        email = value.lower().strip()
        query = Doctor.objects.filter(email__iexact=email)
        if self.instance is not None:
            query = query.exclude(id=self.instance.id)
        if query.exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return email

    def create(self, validated_data):
        return Doctor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.specialization = validated_data.get('specialization', instance.specialization)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.experience_years = validated_data.get('experience_years', instance.experience_years)
        instance.save()
        return instance
