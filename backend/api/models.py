from django.db import models
from smart_selects.db_fields import ChainedForeignKey

class Group(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if self.order == 0:
            last = Group.objects.order_by("-order").first()
            self.order = (last.order + 1) if last else 1
        super().save(*args, **kwargs)



class Student(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Question(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    ANSWERS = (
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D"),
    )

    lesson = ChainedForeignKey(
        Lesson,
        chained_field="group",
        chained_model_field="group",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE
    )

    question = models.TextField()

    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()

    correct = models.IntegerField(choices=ANSWERS)
    
    DIFFICULTY_CHOICES = [
    (1, "Легкий"),
    (2, "Средний"),
    (3, "Сложный"),
    ]

    difficulty = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        default=1
    )

    def __str__(self):
        return self.question


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    score = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
   