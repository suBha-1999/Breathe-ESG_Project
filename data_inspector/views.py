from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import EmissionRecord
from .serializers import EmissionRecordSerializer

class EmissionRecordListView(generics.ListAPIView):
    """
    Returns all emission records. 
    Allows filtering by status (e.g., ?status=FLAGGED) so the analyst can find suspicious rows.
    """
    serializer_class = EmissionRecordSerializer

    def get_queryset(self):
        queryset = EmissionRecord.objects.all().order_by('-created_at')
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

class ApproveRecordView(APIView):
    """Allows the React dashboard to approve a row for audit."""
    def post(self, request, pk):
        try:
            record = EmissionRecord.objects.get(pk=pk)
            record.status = 'APPROVED'
            record.save()
            return Response({"message": f"Record {pk} approved for audit."})
        except EmissionRecord.DoesNotExist:
            return Response({"error": "Record not found"}, status=404)