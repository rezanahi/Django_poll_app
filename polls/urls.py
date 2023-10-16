from django.urls import path
from .views import index, detail, vote, result

app_name = 'polls'

urlpatterns = [
    path('', index),
    path("<int:question_id>/", detail, name='detail'),
    path("<int:question_id>/result/", result),
    path("<int:question_id>/vote/", vote),
]