from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    path("message/", views.SendMessageView.as_view(), name="send_message"),
    path("messages/", views.InboxView.as_view(), name="inbox"),
    path(
        "messages/<int:user_id>/",
        views.UserMessagesView.as_view(),
        name="user_messages",
    ),
    path("create_group/", views.CreateGroupView.as_view(), name="create_group"),
    path(
        "group_message/",
        views.SendGroupMessageView.as_view(),
        name="send_group_message",
    ),
    path("group_messages/", views.GroupInboxView.as_view(), name="group_inbox"),
    path(
        "group_messages/<int:group_id>/",
        views.GroupMessagesView.as_view(),
        name="group_messages",
    ),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # URL route for media files by mapping them to the paths in MEDIA_ROOT setting
