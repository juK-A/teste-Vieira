"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import login_view, register_view, logout_view
from tarefas.views import ActivitiesListView, ActivitiesDetailView, NewActivitiesCreateView, ActivitiesUpdateView, ActivitiesDeleteView, complete_activity_view, link_discord_view
from extras.views import email_view, jira_view, jira_suit_view, jira_sus_view, card_view, card_app_view, card_bug_view, card_incidente_view, card_outros_view, card_performance_view, card_qrcode_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout', logout_view, name='logout'),
    path('list_activities/', ActivitiesListView.as_view(), name='list_activities'),
    path('new_activities/', NewActivitiesCreateView.as_view(), name='new_activities'),
    path('details_activities/<int:pk>/', ActivitiesDetailView.as_view(), name='details_activities'),
    path('details_activities/complete_activity/<int:pk>/', complete_activity_view, name='complete_activity'),
    path('details_activities/<int:pk>/delete/', ActivitiesDeleteView.as_view(), name='delete_activities'),
    path('update_activities/<int:pk>/', ActivitiesUpdateView.as_view(), name='update_activities'),
    path('e-mail/', email_view, name='e-mail'),
    path('jira/', jira_view, name='jira'),
    path('jira/SUS', jira_sus_view, name='jira-sus'),
    path('jira/SUIT', jira_suit_view, name='jira-suit'),
    path('vincular/<uuid:token>/', link_discord_view, name='link_discord'),
    path('cards/', card_view, name='card'),
    path('cards/qrcode', card_qrcode_view, name='card_qrcode'),
    path('cards/performance', card_performance_view, name='card_performance'),
    path('cards/outros', card_outros_view, name='card_outros'),
    path('cards/incidente', card_incidente_view, name='card_incidente'),
    path('cards/bug', card_bug_view, name='card_bug'),
    path('cards/app', card_app_view, name='card_app'),
]