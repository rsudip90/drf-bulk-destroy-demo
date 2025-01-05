from rest_framework.routers import DefaultRouter

from restapis import views


class CustomAPIRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # by DRF definition, this might be subject to change to version of DRF
        list_router = self.routes[0]
        list_router.mapping.update({
            "delete": "bulk_destroy"
        })


# Routers provide an easy way of automatically determining the URL conf.
APIRouter = CustomAPIRouter()

# note API routers
APIRouter.register(r'notes', views.NoteViewSet, basename="notes")
