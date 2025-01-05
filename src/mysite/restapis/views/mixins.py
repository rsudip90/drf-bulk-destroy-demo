import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied

from ..serializers import BulkDestroyInstanceSerializer


log = logging.getLogger(__name__)


class BulkDestroyModelMixin:
    """
    BulkDestroyModelMixin provides the flexibility to delete
    multiple resources on the list endpoint with the delete
    method.
    """

    # in case, viewset has not defined bulk-destroy count
    __DEFAULT_BULK_DESTROY_COUNT = 5

    # safe side max count
    __MAX_BULK_DESTROY_COUNT = 10

    def bulk_destroy(self, request, *args, **kwargs):
        # if not allowed then raise the error
        if not getattr(self, "allow_bulk_destroy_method", False):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = BulkDestroyInstanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get ids from serializer validated data
        destroy_instance_id_list = serializer.validated_data.get("ids", [])

        # validation check - at least one id is provided
        if len(destroy_instance_id_list) == 0:
            raise ValidationError("at least one object id is required to perform batch delete operation")

        # max allowed bulk destroy count
        bulk_destroy_count = getattr(self, "bulk_destroy_count", 0) or self.__DEFAULT_BULK_DESTROY_COUNT
        bulk_destroy_count = min(bulk_destroy_count, self.__MAX_BULK_DESTROY_COUNT)
        if len(destroy_instance_id_list) > bulk_destroy_count:
            raise PermissionDenied(f"You do not have permission to delete more than {bulk_destroy_count} objects")

        # there might be valid ids to which the requested user doesn't have access
        # hence raise the permission denied error
        valid_bulk_instance_qs = self.get_queryset().filter(pk__in=destroy_instance_id_list)
        if len(destroy_instance_id_list) != valid_bulk_instance_qs.count():
            raise PermissionDenied(detail="You do not have permission to delete one or more objects")

        for permission in self.get_permissions():
            if (
                hasattr(permission, "has_bulk_destroy_permission") and
                not permission.has_bulk_destroy_permission(request, self, valid_bulk_instance_qs)
            ):
                raise PermissionDenied(detail="You do not have permission to delete one or more objects")


        # finally, after all checks, perform bulk destroy
        self.perform_bulk_destroy(valid_bulk_instance_qs)

        # return response
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_bulk_destroy(self, bulk_instance_qs):
        log.info(f"bulk destroy, instance list: {list(bulk_instance_qs)}")
        # using filtered querset just delete it
        bulk_instance_qs.delete()
