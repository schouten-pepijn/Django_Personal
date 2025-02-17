from django.urls import path
from . import views

app_name = "movies"

# movies/
# movies/1
# movies/1/details

# url configuration
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:movie_id>", views.detail, name="detail")
]