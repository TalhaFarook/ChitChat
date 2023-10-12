from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'chat'
urlpatterns = [
    # URL for sending a user chat message
    path('message/', views.send_message_view, name='send_message'),

    # URL for viewing the inbox of chat messages
    path('messages/', views.inbox_view, name='inbox'),

    # URL for viewing chat messages with a specific user
    path('messages/<int:user_id>/', views.user_messages_view, name='user_messages'),

    # URL for creating a new group with users to send messages
    path('create_group/', views.create_group_view, name='create_group'),
    
    # URL for sending a message in a group
    path('group_message/', views.send_group_message_view, name='send_group_message'),

    # URL for viewing the inbox of group chat messages
    path('group_messages/', views.group_inbox_view, name='group_inbox'),

        # URL for viewing the inbox of group chat messages
    path('group_messages/<int:group_id>/', views.group_messages_view, name='group_messages'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # URL route for media files by mapping them to the paths in the MEDIA_ROOT setting
