from django.urls import path
from django.contrib.auth.views import LoginView

from quiz.views import join, profile, quiz, round, category, question, slide, answer, choice

urlpatterns = [
    path('', join.JoinView.as_view(), name="join"),

    path('profile/', profile.ProfileView.as_view(), name='profile'),

    # Quiz
    path('create/quiz/', quiz.CreateQuizView.as_view(), name="create-quiz"),
    path('edit/quiz-<int:quiz_id>/', quiz.EditQuizView.as_view(), name="edit-quiz"),
    path('delete/quiz-<int:quiz_id>/', quiz.DeleteQuizView.as_view(), name="delete-quiz"),

    # Round
    path('create/quiz-<int:quiz_id>/round/', round.CreateRoundView.as_view(), name="create-round"),
    path('edit/quiz-<int:quiz_id>/round-<int:round_id>/', round.EditRoundView.as_view(), name="edit-round"),
    path('delete/quiz-<int:quiz_id>/round-<int:round_id>/', round.DeleteRoundView.as_view(), name="delete-round"),

    # Category
    path('create/quiz-<int:quiz_id>/round-<int:round_id>/category/', category.CreateCategoryView.as_view(), name="create-category"),
    path('edit/quiz-<int:quiz_id>/round-<int:round_id>/category-<int:category_id>/', category.EditCategoryView.as_view(), name="edit-category"),
    path('delete/quiz-<int:quiz_id>/round-<int:round_id>/category-<int:category_id>/', category.DeleteCategoryView.as_view(), name="delete-category"),

    # Question
    path('create/quiz-<int:quiz_id>/round-<int:round_id>/question/', question.CreateQuestionView.as_view(), name="create-question"),
    path('edit/quiz-<int:quiz_id>/round-<int:round_id>/question-<int:question_id>/', question.EditQuestionView.as_view(), name="edit-question"),
    path('delete/quiz-<int:quiz_id>/round-<int:round_id>/question-<int:question_id>/', question.DeleteQuestionView.as_view(), name="delete-question"),

    # Slide
    path('create/quiz-<int:quiz_id>/round-<int:round_id>/question-<int:question_id>/slide/', slide.CreateSlideView.as_view(), name="create-slide"),
    path('edit/quiz-<int:quiz_id>/round-<int:round_id>/question-<int:question_id>/slide-<int:slide_id>/', slide.EditSlideView.as_view(), name="edit-slide"),
    path('delete/quiz-<int:quiz_id>/round-<int:round_id>/question-<int:question_id>/slide-<int:slide_id>/', slide.DeleteSlideView.as_view(), name="delete-slide"), 

    # Answer   
    path('create/quiz-<int:quiz_id>/round-<int:round_id>/question-<int:question_id>/answer/', answer.CreateAnswerView.as_view(), name="create-answer"),
    path('edit/quiz-<int:quiz_id>/round-<int:round_id>/question-<int:question_id>/answer-<int:answer_id>/', answer.EditAnswerView.as_view(), name="edit-answer"),
    path('delete/quiz-<int:quiz_id>/round-<int:round_id>/question-<int:question_id>/answer-<int:answer_id>/', answer.DeleteAnswerView.as_view(), name="delete-answer"), 

    path('create/quiz-<int:quiz_id>/round-<int:round_id>/question-<int:question_id>/choice/', choice.CreateChoiceView.as_view(), name="create-choice"),
    path('edit/quiz-<int:quiz_id>/round-<int:round_id>/question-<int:question_id>/choice-<int:choice_id>/', choice.EditChoiceView.as_view(), name="edit-choice"),
    path('delete/quiz-<int:quiz_id>/round-<int:round_id>/question-<int:question_id>/choice-<int:choice_id>/', choice.DeleteChoiceView.as_view(), name="delete-choice"), 
]