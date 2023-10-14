from django.urls import path
from .views import index, detail, vote, result

urlpatterns = [
    path('', index),
    path("<int:question_id>/", detail),
    path("<int:question_id>/result/", result),
    path("<int:question_id>/vote/", vote),
]