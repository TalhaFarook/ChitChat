from django import forms
from .models import OneChat, Group, GroupChat

# Form for sending a single message
class SingleMessageForm(forms.ModelForm):
    class Meta:
        model = OneChat
        # Specify required fields for sending a single user message
        fields = ['receiver_id', 'message', 'image']

# Form for creating a group 
class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        # Specify required fields for group creation
        fields = ['group_name', 'receivers']  

# Form for sending a message to a group
class GroupMessageForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(GroupMessageForm, self).__init__(*args, **kwargs)
        # Filter users on the basis of group member
        self.fields['group'].queryset = Group.objects.filter(receivers=user)

    class Meta:
        model = GroupChat
        # Specify required fields for sending a group message
        fields = ['group', 'message', 'image']

