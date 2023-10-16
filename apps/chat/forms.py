from django import forms

from .models import Group, GroupChat, OneChat


class SingleMessageForm(forms.ModelForm):
    class Meta:
        model = OneChat
        fields = ["receiver_id", "message", "image"]


class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["group_name", "receivers"]


class GroupMessageForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(GroupMessageForm, self).__init__(*args, **kwargs)
        self.fields["group"].queryset = Group.objects.filter(receivers=user)

    class Meta:
        model = GroupChat
        fields = ["group", "message", "image"]
