from rest_framework_simplejwt.views import TokenRefreshView
from . import authentication_views
from rest_framework import routers
from django.urls import path
from . import views


# TODO test endpoints
auth_views = [
    path('auth/user', authentication_views.UserAPI.as_view(), name='user'),
    path('auth/register', authentication_views.RegisterAPI.as_view(), name='register'),
    path('auth/register/admin',
         authentication_views.RegisterAdminAPI.as_view(), name='register-admin'),
    path('auth/reset', authentication_views.ResetAPI.as_view(), name='reset'),
    path('auth/change', authentication_views.ChangePassAPI.as_view(), name='change'),
    path('auth/change/forgot',
         authentication_views.ForgotPassAPI.as_view(), name='change-forgot'),
    path('auth/login/', authentication_views.LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
]

router = routers.DefaultRouter()
router.register('city', views.CityView, 'city')
router.register('company', views.CompanyView, 'company')
router.register('hierarchy', views.HierarchyView, 'hierarchy')
router.register('vibrouser', authentication_views.VibroUserView, 'vibrouser')
router.register('machine', views.MachineView, 'machine')
router.register('sensor', views.SensorView, 'sensor')
router.register('gear', views.GearView, 'gear')
router.register('axis', views.AxisView, 'axis')
router.register('bearing', views.BearingView, 'bearing')
router.register('coupling', views.CouplingView, 'coupling')
router.register('measurement', views.MeasurementView, 'measurement')
router.register('values', views.ValuesView, 'values')
router.register('termal', views.TermoImageView, 'termal')
router.register('point', views.PointView, 'point')
router.register('report', views.ReportView, 'report')  # TODO needs testing
# router.register("dates", views.MeasurementDatesView,
#                 'dates')  # TODO test measurement dates


urlpatterns = auth_views + router.urls
"""
GET REQUESTS
trailing slash followed by query params
###########################
DELETE REQUESTS
trailing slash followed by id of instance to be deleted then another slash
###########################
POST REQUESTS
trailing slash followed and body of object to create
PATCH REQUESTS
trailing slash followed by id of instance to be patched then trailing slash
"""
