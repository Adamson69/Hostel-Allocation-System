from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (("male","Male"),("female","Female"))

class Hostel(models.Model):
    name = models.CharField(max_length=120, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    capacity_total = models.PositiveIntegerField(default=0)
    capacity_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.gender})"

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="rooms")
    number = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField(default=4)
    occupied = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("hostel","number")

    def __str__(self):
        return f"{self.hostel.name} - {self.number}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    matric_no = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    level = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.matric_no}"

APPLICATION_STATUS = (
    ("pending","Pending"),
    ("approved","Approved"),
    ("rejected","Rejected"),
)

class Application(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    preferred_hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=APPLICATION_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"App[{self.id}] {self.student.username} -> {self.preferred_hostel}"

class Allocation(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allocations")
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allocated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.hostel.name} / {self.room.number}"
