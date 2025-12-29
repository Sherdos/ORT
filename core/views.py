from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Test, TestAttempt, UserAnswer, Question


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tests"] = Test.objects.all()[:6]
        if self.request.user.is_authenticated:
            context["recent_attempts"] = TestAttempt.objects.filter(
                user=self.request.user
            )[:5]
        return context


class CustomLoginView(LoginView):
    template_name = "core/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")


class CustomLogoutView(LogoutView):
    next_page = "home"


class RegisterView(TemplateView):
    template_name = "core/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        form = UserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация успешна! Теперь войдите в систему.")
            return redirect("login")
        return render(request, self.template_name, {"form": form})


class TestListView(ListView):
    model = Test
    template_name = "core/tests.html"
    context_object_name = "tests"


class TestDetailView(DetailView):
    model = Test
    template_name = "core/test_detail.html"
    context_object_name = "test"


class ResultsView(LoginRequiredMixin, ListView):
    model = TestAttempt
    template_name = "core/results.html"
    context_object_name = "attempts"
    login_url = "login"

    def get_queryset(self):
        return TestAttempt.objects.filter(user=self.request.user)


class AttemptDetailView(LoginRequiredMixin, DetailView):
    model = TestAttempt
    template_name = "core/attempt_detail.html"
    context_object_name = "attempt"
    login_url = "login"

    def get_queryset(self):
        return TestAttempt.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all answers with related data for analysis
        context["answers"] = self.object.answers.select_related(
            "question"
        ).prefetch_related("selected_options", "question__options")
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "core/profile.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        attempts = TestAttempt.objects.filter(user=user, is_completed=True)

        context["total_tests"] = attempts.count()
        context["total_correct"] = sum(a.correct_answers for a in attempts)
        context["total_questions"] = sum(a.total_questions for a in attempts)

        if context["total_questions"] > 0:
            context["average_score"] = round(
                (context["total_correct"] / context["total_questions"]) * 100, 1
            )
        else:
            context["average_score"] = 0

        # Recent attempts
        context["recent_attempts"] = attempts[:10]

        # Mistakes analysis - questions user got wrong most often
        wrong_answers = UserAnswer.objects.filter(
            attempt__user=user, is_correct=False
        ).select_related("question")

        # Count mistakes per question
        mistake_counts = {}
        for answer in wrong_answers:
            q_id = answer.question.id
            if q_id not in mistake_counts:
                mistake_counts[q_id] = {"question": answer.question, "count": 0}
            mistake_counts[q_id]["count"] += 1

        # Sort by mistake count
        context["common_mistakes"] = sorted(
            mistake_counts.values(), key=lambda x: x["count"], reverse=True
        )[:10]

        return context
