from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from .models import Question, Lesson, Group, Student, Result
from django.views.decorators.csrf import csrf_exempt
import random

@api_view(['GET'])
def lessons(request, group_id):

    ls = Lesson.objects.filter(group_id=group_id)

    data = []

    for l in ls:
        data.append({
            "id": l.id,
            "title": l.title
        })

    return Response(data)

@api_view(['GET'])
def questions(request, lesson_id):

    easy = list(Question.objects.filter(lesson_id=lesson_id, difficulty=1))
    medium = list(Question.objects.filter(lesson_id=lesson_id, difficulty=2))
    hard = list(Question.objects.filter(lesson_id=lesson_id, difficulty=3))

    if len(easy) < 5 or len(medium) < 5 or len(hard) < 5:
        return Response({
            "error": "15 questions!",
            "easy": len(easy),
            "medium": len(medium),
            "hard": len(hard)
        }, status=400)

    random.shuffle(easy)
    random.shuffle(medium)
    random.shuffle(hard)

    selected = easy[:5] + medium[:5] + hard[:5]

    data = []

    for q in selected:
        data.append({
            "question": q.question,
            "options": [
                q.option_a,
                q.option_b,
                q.option_c,
                q.option_d
            ],
            "correct": q.correct - 1
        })

    return Response(data)
    
@api_view(['GET'])
def groups(request):

    gs = Group.objects.all()

    data = []

    for g in gs:
        data.append({
            "id": g.id,
            "name": g.name
        })

    return Response(data)

@api_view(['POST'])
@authentication_classes([])
@csrf_exempt
def save_result(request):

    student_id = request.data.get("student")
    lesson_id = request.data.get("lesson")
    score = int(request.data.get("score", 0))

    result = Result.objects.filter(
        student_id=student_id,
        lesson_id=lesson_id
    ).first()

    if result:

        if score > result.score:
            result.score = score
            result.save()

    else:

        Result.objects.create(
            student_id=student_id,
            lesson_id=lesson_id,
            score=score
        )

    return Response({"status": "ok"})

@api_view(['GET'])    
def leaderboard(request, lesson_id):

    results = Result.objects.filter(lesson_id=lesson_id).order_by("-score")[:10]

    data = []

    for r in results:

        data.append({
            "student": r.student.name,
            "student_id": r.student.id,
            "score": r.score
        })

    return Response(data)

@api_view(['GET'])
def students(request, group_id):

    st = Student.objects.filter(group_id=group_id)

    data = []

    for s in st:
        data.append({
            "id": s.id,
            "name": s.name
        })

    return Response(data)