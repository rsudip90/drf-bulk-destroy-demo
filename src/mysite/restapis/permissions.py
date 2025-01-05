from rest_framework import permissions


class NotePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE" and "agreement" in obj.title:
            return False

        # only owner can update, delete the note
        return obj.owner == request.user

    def has_bulk_destroy_permission(self, request, view, requested_obj_qs):
        for note_obj in requested_obj_qs:
            # if any note object is not permitted to delete then return
            if not self.has_object_permission(request, view, note_obj):
                return False

        return True
