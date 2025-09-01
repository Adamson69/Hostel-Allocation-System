from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Hostel, Room, StudentProfile, Application, Allocation
from .forms import RegisterForm, LoginForm, ApplicationForm

def home(request):
    hostels = Hostel.objects.all().order_by("name")
    return render(request, "home.html", {"hostels": hostels})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("student_dashboard")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        u = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        if u:
            login(request, u)
            return redirect("student_dashboard")
        messages.error(request, "Invalid credentials.")
    return render(request, "auth/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("student_dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        pwd = form.cleaned_data["password"]
        matric_no = form.cleaned_data["matric_no"]
        gender = form.cleaned_data["gender"]
        level = form.cleaned_data["level"]
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            u = User.objects.create_user(username=username, password=pwd)
            StudentProfile.objects.create(user=u, matric_no=matric_no, gender=gender, level=level)
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
    return render(request, "auth/register.html", {"form": form})

@login_required
def student_dashboard(request):
    profile = getattr(request.user, "profile", None)
    apps = Application.objects.filter(student=request.user).order_by("-created_at")
    alloc = Allocation.objects.filter(student=request.user).first()
    return render(request, "student/dashboard.html", {"profile": profile, "applications": apps, "allocation": alloc})

@login_required
def apply_view(request):
    profile = request.user.profile
    form = ApplicationForm(request.POST or None, user_gender=profile.gender)
    if request.method == "POST" and form.is_valid():
        app = form.save(commit=False)
        app.student = request.user
        app.save()
        messages.success(request, "Application submitted.")
        return redirect("student_dashboard")
    return render(request, "student/apply.html", {"form": form})

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    apps = Application.objects.select_related("student","preferred_hostel").order_by("-created_at")
    hostels = Hostel.objects.all()
    rooms = Room.objects.select_related("hostel").order_by("hostel__name","number")
    return render(request, "admin/dashboard.html", {"apps": apps, "hostels": hostels, "rooms": rooms})

@user_passes_test(is_admin)
def allocate_view(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    if app.status == "approved":
        messages.info(request, "Application already approved.")
        return redirect("admin_dashboard")

    # naive allocation: find first room in preferred hostel with space
    rooms = Room.objects.filter(hostel=app.preferred_hostel).order_by("number")
    for r in rooms:
        if r.occupied < r.capacity:
            Allocation.objects.create(student=app.student, hostel=r.hostel, room=r)
            r.occupied += 1
            r.save()
            # reduce hostel available if we track it
            h = r.hostel
            if h.capacity_available > 0:
                h.capacity_available -= 1
                h.save()
            app.status = "approved"
            app.save()
            messages.success(request, f"Allocated {app.student.username} to {r.hostel.name} / Room {r.number}")
            break
    else:
        messages.error(request, "No available space in preferred hostel.")
    return redirect("admin_dashboard")
