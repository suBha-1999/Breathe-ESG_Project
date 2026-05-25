from django.urls import path
from .views import EmissionRecordListView, ApproveRecordView

urlpatterns = [
    path('api/records/', EmissionRecordListView.as_view(), name='record-list'),
    path('api/records/<int:pk>/approve/', ApproveRecordView.as_view(), name='record-approve'),
]