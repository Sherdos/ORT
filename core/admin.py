from django.contrib import admin
import nested_admin
from .models import Tag, Question, Option, Test, TestAttempt, UserAnswer


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


# Regular inline for Question admin
class OptionInline(admin.TabularInline):
    """Allows adding options directly when creating/editing a question"""

    model = Option
    extra = 4
    min_num = 2


# Nested inlines for Test admin (Test -> Question -> Option)
class NestedOptionInline(nested_admin.NestedTabularInline):
    """Nested inline for options within questions within tests"""

    model = Option
    extra = 4
    min_num = 2
    classes = ["collapse"]


class NestedQuestionInline(nested_admin.NestedStackedInline):
    """Nested inline for questions within tests - includes options"""

    model = Question.tests.through
    extra = 0
    verbose_name = "Question"
    verbose_name_plural = "Questions"
    autocomplete_fields = ["question"]


class QuestionInlineForTest(nested_admin.NestedStackedInline):
    """Inline to add/edit questions directly in Test with their options"""

    model = Question
    extra = 1
    inlines = [NestedOptionInline]
    filter_horizontal = ["tags"]
    fieldsets = (
        (None, {"fields": ("text", "image", "type", "difficulty")}),
        ("Details", {"fields": ("explanation", "tags"), "classes": ["collapse"]}),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "short_text", "type", "difficulty", "get_tags"]
    list_filter = ["type", "difficulty", "tags"]
    search_fields = ["text"]
    filter_horizontal = ["tags"]
    inlines = [OptionInline]

    def short_text(self, obj):
        return obj.text[:80] + "..." if len(obj.text) > 80 else obj.text

    short_text.short_description = "Question"

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    get_tags.short_description = "Tags"


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "question", "is_correct"]
    list_filter = ["is_correct"]
    search_fields = ["text", "question__text"]


@admin.register(Test)
class TestAdmin(nested_admin.NestedModelAdmin):
    list_display = [
        "title",
        "duration_minutes",
        "question_count",
        "points_per_correct_answer",
        "actual_questions",
    ]
    search_fields = ["title", "text"]
    filter_horizontal = ["questions"]
    fieldsets = (
        (None, {"fields": ("title", "text", "image")}),
        (
            "Settings",
            {
                "fields": (
                    "duration_minutes",
                    "question_count",
                    "points_per_correct_answer",
                )
            },
        ),
        (
            "Select Existing Questions",
            {
                "fields": ("questions",),
                "description": "Select existing questions to include in this test",
                "classes": ["collapse"],
            },
        ),
    )
    inlines = [NestedQuestionInline]

    def actual_questions(self, obj):
        return obj.questions.count()

    actual_questions.short_description = "Questions Added"


class UserAnswerInline(admin.TabularInline):
    """Show user answers within test attempt"""

    model = UserAnswer
    extra = 0
    readonly_fields = ["question", "is_correct", "text_answer", "answered_at"]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "test",
        "score",
        "correct_answers",
        "total_questions",
        "percentage_display",
        "is_completed",
        "started_at",
    ]
    list_filter = ["is_completed", "test", "started_at"]
    search_fields = ["user__username", "test__title"]
    readonly_fields = [
        "user",
        "test",
        "started_at",
        "completed_at",
        "score",
        "correct_answers",
        "total_questions",
    ]
    inlines = [UserAnswerInline]

    def percentage_display(self, obj):
        return f"{obj.percentage}%"

    percentage_display.short_description = "Score %"


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ["attempt", "question_short", "is_correct", "answered_at"]
    list_filter = ["is_correct", "attempt__test"]
    search_fields = ["attempt__user__username", "question__text"]

    def question_short(self, obj):
        return (
            obj.question.text[:50] + "..."
            if len(obj.question.text) > 50
            else obj.question.text
        )

    question_short.short_description = "Question"
