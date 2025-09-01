from django.contrib import admin
from .models import Hostel, Room, StudentProfile, Application, Allocation

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "capacity_total", "capacity_available")

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("hostel", "number", "capacity", "occupied")

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "matric_no", "gender", "level")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "preferred_hostel", "status", "created_at")

@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ("student", "hostel", "room", "allocated_at")
