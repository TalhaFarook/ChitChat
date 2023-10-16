from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import View
from PIL import Image

from .forms import GroupCreationForm, GroupMessageForm, SingleMessageForm
from .models import Group, GroupChat, OneChat, UserTable


class SendMessageView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        form = SingleMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            if int(request.POST["receiver_id"]) == user.id:
                return render(
                    request,
                    "single/send_single_message_form.html",
                    {"form": form, "message_status": 1},
                )
            message.receiver_id_id = request.POST["receiver_id"]
            message.sender_id = user.id
            if message.image:
                original_img = Image.open(message.image)
                new_img = original_img.copy()
                new_img = new_img.resize((250, 250), Image.LANCZOS)
                new_img.save(message.image.path)
                message.image = message.image.path
            message.is_sent = True
            message.save()
            return render(
                request,
                "single/send_single_message_form.html",
                {"form": form, "message_status": 2},
            )

    def get(self, request):
        form = SingleMessageForm()
        return render(
            request,
            "single/send_single_message_form.html",
            {"form": form, "message_status": 0},
        )


class InboxView(LoginRequiredMixin, View):
    def get(self, request):
        received_messages = OneChat.objects.filter(receiver_id_id=request.user.id)
        sent_messages = OneChat.objects.filter(sender_id=request.user.id)
        users_id, names = [], []
        if received_messages:
            for message in received_messages:
                users_id.append(message.sender_id)
                names.append(UserTable.objects.get(pk=message.sender_id))
        if sent_messages:
            ids = []
            for sent in sent_messages:
                ids.append(sent.receiver_id_id)
            unique_ids = list(set(ids))
            for id in unique_ids:
                user = get_object_or_404(UserTable, id=id)
                users_id.append(user.id)
                names.append(user)
        if users_id and names:
            users_id = list(set(users_id))
            names = list(set(names))
            users_names = zip(users_id, names)
        else:
            users_names = []
        return render(request, "single/inbox.html", {"users_names": users_names})


class UserMessagesView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = request.user
        received_messages = OneChat.objects.filter(
            receiver_id_id=user.id, sender_id=user_id
        )
        sent_messages = OneChat.objects.filter(
            receiver_id_id=user_id, sender_id=user.id
        )
        messages = received_messages | sent_messages
        for message in received_messages:
            if not message.is_read:
                message.is_read = True
                message.save()
        user = UserTable.objects.get(pk=user_id)
        active = ""
        if user.current_active == 1:
            active = "Active"
        else:
            duration = timezone.now() - user.last_login
            days = duration.days
            seconds = duration.seconds
            hours, remainder = divmod(seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            if days > 0:
                active = f"{days} day ago!"
            elif hours > 0:
                active = f"{hours} hours ago!"
            elif minutes > 0:
                active = f"{minutes} minutes ago"
            else:
                active = f"{seconds} seconds ago"
        return render(
            request,
            "single/user_messages.html",
            {
                "messages": messages,
                "id": user_id,
                "active": active,
                "username": user.username,
            },
        )


class CreateGroupView(LoginRequiredMixin, View):
    def post(self, request):
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group_name = request.POST["group_name"]
            group_receivers = request.POST.getlist("receivers")
            group = Group.objects.create(group_name=group_name)
            group.receivers.set(group_receivers)
            group.save()
            return render(
                request, "group/create_group.html", {"form": form, "message_status": 1}
            )

    def get(self, request):
        form = GroupCreationForm()
        return render(
            request, "group/create_group.html", {"form": form, "message_status": 0}
        )


class SendGroupMessageView(LoginRequiredMixin, View):
    def post(self, request):
        form = GroupMessageForm(request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            group = Group.objects.get(pk=message.group_id)
            message.sender_id = request.user
            message.group = group
            message.image = request.POST["image"]
            if message.image:
                original_img = Image.open(message.image)
                new_img = original_img.copy()
                new_img = new_img.resize((250, 250), Image.LANCZOS)
                new_img.save(message.image.path)
                message.image = message.image.path
            message.save()
            return render(
                request,
                "group/send_group_message.html",
                {"form": form, "message_status": 1},
            )

    def get(self, request):
        form = GroupMessageForm(request.user)
        return render(
            request,
            "group/send_group_message.html",
            {"form": form, "message_status": 0},
        )


class GroupInboxView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.id
        groups = Group.objects.filter(receivers=user)
        if groups:
            ids, names = [], []
            for group in groups:
                names.append(group)
                temp = Group.objects.filter(group_name=group).values_list(
                    "group_id", flat=True
                )
                for id in temp:
                    ids.append(id)
            group_names = zip(ids, names)
        else:
            group_names = []
        return render(request, "group/group_inbox.html", {"groups": group_names})


class GroupMessagesView(LoginRequiredMixin, View):
    def get(self, request, group_id):
        groupchat_obj = GroupChat.objects.filter(group_id=group_id)
        group_name = get_object_or_404(Group, group_id=group_id).group_name
        group = Group.objects.get(group_id=group_id)
        receivers_list = list(group.receivers.all())
        id = request.user.id
        return render(
            request,
            "group/group_messages.html",
            {
                "groupchat_obj": groupchat_obj,
                "group_name": group_name,
                "id": id,
                "receivers_list": receivers_list,
            },
        )
