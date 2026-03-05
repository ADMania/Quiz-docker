from django.urls import path
from .views import questions, lessons, groups, students, save_result, leaderboard
from django.http import HttpResponse

def index(request):
    return HttpResponse("Quiz API работает")

urlpatterns = [
    path("groups/", groups),
    path("students/<int:group_id>/", students),
    path("questions/<int:lesson_id>/", questions),
    path("lessons/<int:group_id>/", lessons),
    path("result/", save_result),
    path("leaderboard/<int:lesson_id>/", leaderboard),
    path("", index),
]