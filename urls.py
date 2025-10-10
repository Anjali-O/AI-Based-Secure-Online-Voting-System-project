from django.urls import path
from .views import *
urlpatterns = [
   # path("pathname/", functionname, name="")
    path("", home, name="home1"),
    path("admin-registration/", registration, name="registration1"),
    path("admin-login/", signin, name='log1'),
    path("admin-password-reset/",passreset,name="password-reset1"),
    path("admin-otp-generate/", otpgene, name='otp-generate1'),
    path("admin-logout/",signout, name="logout1"),
    path('admin-show-vote/', show_vote, name='show_vote'),

    path('admin-candidate/', view_candidate, name='candidate'),
    path('admin-add-candidate/', add_candidate, name='add-candidate'),
    path('edit_candidate/<int:cid>', edit_candidate, name='edit'),
    path('delete-candidate/<int:cid>', delete_candidate, name='delete'),

    path('admin-add-state/', add_state, name='add_state'),
    path('view-state/', view_state, name='view_state'),
    path('edit-state/<int:sid>', edit_state, name='edit_state'),
    path('delete-state/<int:sid>', delete_state, name='delete_state'),

    path('admin-add-district/', add_district, name='add_dist'),
    path('view-district/', view_district, name='view_dist'),
    path('edit-district/<int:did>', edit_district, name='edit_dist'),
    path('delete-district/<int:did>', delete_district, name='delete_dist'),

    path('admin-add-municipality/', add_municipality, name='add_municipality'),
    path('view-municipality/', view_municipality, name='view_municipality'),
    path('edit-municipality/<int:mid>', edit_municipality, name='edit_municipality'),
    path('delete_municipality/<int:mid>', delete_municipality, name='delete_municipality'),

    path('admin-add-voters/', add_voters, name='add_voters'),
    path('view-voters/', view_voters, name='view_voters'),
    path('edit-voters/<int:vid>', edit_voters, name='edit_voters'),
    path('delete-voters/<int:vid>', delete_voters, name='delete_voters'),

    path('view-reg-voters', view_user_reg, name='view_reg_voters')

    ]