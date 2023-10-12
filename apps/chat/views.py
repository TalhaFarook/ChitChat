from django.shortcuts import render, get_object_or_404
from .forms import SingleMessageForm, GroupMessageForm, GroupCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserTable, OneChat, Group, GroupChat
from django.utils import timezone
from PIL import Image

@login_required
# This view will handle the inputs from the message form for single messages
def send_message_view(request):
    user = request.user
    # Check for message sent successful or not

    if request.method == 'POST':
        form = SingleMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
 
            if int(request.POST['receiver_id']) == user.id:
                # Display a message that you can't send yourself a message
                return render(request, 'single/send_single_message_form.html', {'form': form, 'message_status': 1})
            
            # Set the sender and receiver of the message
            message.receiver_id_id = request.POST['receiver_id']
            message.sender_id = user.id

            if message.image:
                # Open the original image and create a copy
                original_img = Image.open(message.image)
                new_img = original_img.copy()

                # Resize the copy
                new_img = new_img.resize((250, 250), Image.LANCZOS)

                # Save the resized image to the media directory
                new_img.save(message.image.path)
                message.image = message.image.path

            # Mark the message as sent and save it
            message.is_sent = True
            message.save()

            # Display a message indicating that the message has been sent successfully
            return render(request, 'single/send_single_message_form.html', {'form': form, 'message_status': 2})
    else:
        form = SingleMessageForm()

    return render(request, 'single/send_single_message_form.html', {'form': form, 'message_status': 0})

@login_required
# This view will handle the inbox for single users
def inbox_view(request):
    # Gather all the received and sent messages by the current user
    received_messages = OneChat.objects.filter(receiver_id_id=request.user.id)
    sent_messages = OneChat.objects.filter(sender_id=request.user.id)

    users_id, names = [], []
    if received_messages:
        # Gather unique sender IDs and names from messages to display in inbox
        for message in received_messages:
            # Get the user's name and id to create a hyperlink to send to their chat
            users_id.append(message.sender_id)
            names.append(UserTable.objects.get(pk=message.sender_id))

    # Display messages to users who haven't responded back   
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

        # Combine sender IDs and names as pairs to display on the inbox page
        users_names = zip(users_id, names)
    else:
        users_names = []

    return render(request, 'single/inbox.html', {'users_names': users_names})

@login_required
# This view will show all the messages of a particular user
def user_messages_view(request, user_id):
    user = request.user

    # Gather all the received and sent messages by the current user
    received_messages = OneChat.objects.filter(receiver_id_id=user.id, sender_id=user_id)
    sent_messages = OneChat.objects.filter(receiver_id_id=user_id, sender_id=user.id)

    # Combine received and sent messages into one queryset
    messages = received_messages | sent_messages

    # Mark received messages as read
    for message in received_messages:
        if not message.is_read:
            message.is_read = True
            message.save()

    # Get the user details of the sender id to check for their activity (or inactivity)
    user = UserTable.objects.get(pk=user_id)
    active = ''

    # Check for user's activity
    if user.current_active == 1:
        active = 'Active'
    else:
        # Calculate and display the user's last activity
        duration = timezone.now() - user.last_login
        days = duration.days
        seconds = duration.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        if days > 0:
            active = f'{days} day ago!'
        elif hours > 0:
            active = f'{hours} hours ago!'
        elif minutes > 0:
            active = f'{minutes} minutes ago'
        else:
            active = f'{seconds} seconds ago'

    return render(request, 'single/user_messages.html', {'messages': messages, 'id': user_id, 'active': active, 'username': user.username})

@login_required
# This view will create a new group
def create_group_view(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)

        if form.is_valid():
            group_name = request.POST['group_name']
            group_receivers = request.POST.getlist('receivers')

            # Create a new group with the specified name
            group = Group.objects.create(group_name=group_name)

            # Assign receivers to the group
            group.receivers.set(group_receivers)
            group.save() 

            return render(request, 'group/create_group.html', {'form': form, 'message_status': 1}) 
    
    else:
        form = GroupCreationForm()

    return render(request, 'group/create_group.html', {'form': form, 'message_status': 0}) 

@login_required
# This view will handle the inputs from the message form for group messages
def send_group_message_view(request):
    if request.method == 'POST':
        form = GroupMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            group = Group.objects.get(pk=message.group_id)
            
            # Set the sender and group for the group message
            message.sender_id = request.user
            message.group = group

            message.image = request.POST['image']

            if message.image:
                # Open the original image and create a copy
                original_img = Image.open(message.image)
                new_img = original_img.copy()

                # Resize the copy
                new_img = new_img.resize((250, 250), Image.LANCZOS)

                # Save the resized image to the media directory
                new_img.save(message.image.path)
                message.image = message.image.path

            message.save()

            return render(request, 'group/send_group_message.html', {'form': form, 'message_status': 1})
    else:
        form = GroupMessageForm()

    return render(request, 'group/send_group_message.html', {'form': form, 'message_status': 0})

@login_required
# This view will handle the inbox for group chats for a users
def group_inbox_view(request):
    user = request.user.id

    # Retrieve groups for which the user is a receiver
    groups = Group.objects.filter(receivers=user)

    print(groups)

    if groups:
        ids, names = [], []

        for group in groups:
            names.append(group)

            # Retrieve the group ID
            ids.append(get_object_or_404(Group, group_name=group).group_id)

        group_names = zip(ids, names)
    else:
        group_names = []

    return render(request, 'group/group_inbox.html', {'groups': group_names})

@login_required
# This view will show all the messages of a particular group chat
def group_messages_view(request, group_id):
    # Filter group chat messages by group ID
    groupchat_obj = GroupChat.objects.filter(group_id=group_id)
    
    # Retrieve the group name based on the group ID
    group_name = get_object_or_404(Group, group_id=group_id).group_name

    # Retrieve the user's ID
    id = request.user.id

    return render(request, 'group/group_messages.html', {'groupchat_obj': groupchat_obj, 'group_name': group_name, 'id': id})
