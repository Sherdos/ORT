from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class QuestionType(models.TextChoices):
    SINGLE_CHOICE = "single_choice", "Single Choice"
    MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"
    TEXT_INPUT = "text_input", "Text Input"


class QuestionDifficulty(models.TextChoices):
    EASY = "easy", "Easy"
    MEDIUM = "medium", "Medium"
    HARD = "hard", "Hard"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    image = models.FileField(upload_to="questions/", blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    type = models.CharField(
        max_length=20, choices=QuestionType.choices, default=QuestionType.SINGLE_CHOICE
    )
    difficulty = models.CharField(
        max_length=10,
        choices=QuestionDifficulty.choices,
        default=QuestionDifficulty.MEDIUM,
    )
    tags = models.ManyToManyField(Tag, related_name="questions", blank=True)

    def __str__(self):
        return self.text[:50]


class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]


class Test(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to="tests/", blank=True, null=True)
    duration_minutes = models.PositiveIntegerField()
    question_count = models.PositiveIntegerField()
    points_per_correct_answer = models.PositiveIntegerField(default=1)
    questions = models.ManyToManyField(Question, related_name="tests", blank=True)

    def __str__(self):
        return self.title


class TestAttempt(models.Model):
    """Stores overall result of a user's test attempt"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="test_attempts"
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="attempts")
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(blank=True, null=True)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.user.username} - {self.test.title} ({self.started_at.date()})"

    @property
    def percentage(self):
        if self.total_questions == 0:
            return 0
        return round((self.correct_answers / self.total_questions) * 100, 2)

    @property
    def incorrect_answers(self):
        return self.total_questions - self.correct_answers


class UserAnswer(models.Model):
    """Stores each individual answer a user gives - tracks mistakes"""

    attempt = models.ForeignKey(
        TestAttempt, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="user_answers"
    )
    # For single/multiple choice questions
    selected_options = models.ManyToManyField(
        Option, related_name="user_selections", blank=True
    )
    # For text input questions
    text_answer = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["attempt", "question"]

    def __str__(self):
        status = "✓" if self.is_correct else "✗"
        return f"{status} {self.attempt.user.username} - Q:{self.question.pk}"
