from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Doctor, Patient
from core.api.serializers import (
    DoctorSerializer,
    LoginSerializer,
    PatientSerializer,
    RegisterSerializer,
)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "id": user.id,
                        "name": user.first_name,
                        "email": user.email,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = data["user"]
            return Response(
                {
                    "message": "Login successful",
                    "access": data["access"],
                    "refresh": data["refresh"],
                    "user": {
                        "id": user.id,
                        "name": user.first_name,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.filter(created_by=request.user).order_by('-created_at')
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save(created_by=request.user)
            return Response(
                {
                    "message": "Patient added successfully",
                    "patient": PatientSerializer(patient).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return Patient.objects.filter(id=pk, created_by=user).first()

    def get(self, request, pk):
        patient = self.get_object(pk, request.user)
        if patient is None:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        patient = self.get_object(pk, request.user)
        if patient is None:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            updated_patient = serializer.save()
            return Response(
                {
                    "message": "Patient updated successfully",
                    "patient": PatientSerializer(updated_patient).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        patient = self.get_object(pk, request.user)
        if patient is None:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        patient.delete()
        return Response(
            {"message": "Patient record deleted successfully."},
            status=status.HTTP_200_OK,
        )


class DoctorListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctors = Doctor.objects.all().order_by('-created_at')
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.save(created_by=request.user)
            return Response(
                {
                    "message": "Doctor added successfully",
                    "doctor": DoctorSerializer(doctor).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return Doctor.objects.filter(id=pk).first()

    def get(self, request, pk):
        doctor = self.get_object(pk)
        if doctor is None:
            return Response(
                {"error": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        doctor = self.get_object(pk)
        if doctor is None:
            return Response(
                {"error": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if doctor.created_by != request.user:
            return Response(
                {"error": "You do not have permission to update this doctor record."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            updated_doctor = serializer.save()
            return Response(
                {
                    "message": "Doctor updated successfully",
                    "doctor": DoctorSerializer(updated_doctor).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doctor = self.get_object(pk)
        if doctor is None:
            return Response(
                {"error": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if doctor.created_by != request.user:
            return Response(
                {"error": "You do not have permission to delete this doctor record."},
                status=status.HTTP_403_FORBIDDEN,
            )
        doctor.delete()
        return Response(
            {"message": "Doctor record deleted successfully."},
            status=status.HTTP_200_OK,
        )


# Backward compatibility alias
PatientCreateView = PatientListCreateView
