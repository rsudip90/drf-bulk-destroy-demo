from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Note
from ..serializers import NoteSerializer
from ..permissions import NotePermission
from .mixins import BulkDestroyModelMixin


class NoteViewSet(BulkDestroyModelMixin, viewsets.ModelViewSet):
    """
    NoteViewSet to handle CRUD operations with bulk-destroy.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated, NotePermission, )
    allow_bulk_destroy_method = True
    bulk_destroy_count = 5

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
