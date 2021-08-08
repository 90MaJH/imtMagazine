from django import forms
from django.forms import PasswordInput
from django_summernote.widgets import SummernoteWidget
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import ImtBoards
from .models import ImtBoards_reply
from .models import ImtBoards_notice_reply
from .models import Qnas
from .models import Qnas_reply
from .models import Qnas_notice_reply
from .models import User
from .models import Message_detail

# Accounts
class MagazineUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'nickname', 'category_imtboards_1', 'category_imtboards_2', 'category_imtboards_3', 'category_qnas_1', 'category_qnas_2', 'category_qnas_3')

class MagazineUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('category_imtboards_1', 'category_imtboards_2', 'category_imtboards_3', 'category_qnas_1', 'category_qnas_2', 'category_qnas_3')

class MagazineUserNicknameChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('nickname',)


class MagazineSigninForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'username'}))

    def __init__(self, *args, **kwargs):
        super(MagazineSigninForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(attrs={'class': 'input100', 'placeholder': 'passwowrd'})

class MessageDetailForm(forms.ModelForm):
    class Meta:
        model = Message_detail
        fields = ('context',)

        widgets = {
            'context': forms.Textarea(attrs={'class': 'form-control type_msg',
                                             'placeholder': 'Type your message...'}),
        }

# ImtBoards
class ImtBoardsWriteForm(forms.ModelForm):
    class Meta:
        model = ImtBoards
        fields = ('pub_user', 'pub_user_nickname', 'password', 'category', 'title', 'context')

        widgets = {
            'pub_user': forms.HiddenInput,
            'pub_user_nickname': forms.TextInput(attrs={'placeholder': '5자이하'}),
            'title': forms.TextInput(attrs={'placeholder': 'under 50 characters'}),
            'context': SummernoteWidget(),
            'password': PasswordInput(attrs={'class': 'form-control',
                                             'placeholder': '4자이하'}),
        }


class ImtBoardsReplyForm(forms.ModelForm):
    class Meta:
        model = ImtBoards_reply
        fields = ('reply_user', 'password', 'reply_user_nickname', 'context')

        widgets = {
            'reply_user': forms.HiddenInput,
            'reply_user_nickname': forms.TextInput(attrs={'placeholder': '5자이하'}),
            'password': PasswordInput(attrs={'placeholder': '4자이하'}),
            'context': forms.Textarea(attrs={'cols': 2, 'rows': 5}),
            'imtBoards': forms.HiddenInput,
            'parent': forms.HiddenInput,
        }


class ImtBoardsNoticeReplyForm(forms.ModelForm):
    class Meta:
        model = ImtBoards_notice_reply
        fields = ('reply_user', 'password', 'reply_user_nickname', 'context')

        widgets = {
            'reply_user': forms.HiddenInput,
            'reply_user_nickname': forms.TextInput(attrs={'placeholder': '5자이하'}),
            'password': PasswordInput(attrs={'placeholder': '4자이하'}),
            'context': forms.Textarea(attrs={'cols': 2, 'rows': 5}),
            'imtBoards_notice': forms.HiddenInput,
            'parent': forms.HiddenInput,
        }


# Qna
class QnasWriteForm(forms.ModelForm):
    class Meta:
        model = Qnas
        fields = ('pub_user', 'pub_user_nickname', 'password', 'category', 'title', 'context')

        widgets = {
            'pub_user': forms.HiddenInput,
            'pub_user_nickname': forms.TextInput(attrs={'placeholder': '5자이하'}),
            'title': forms.TextInput(attrs={'placeholder': 'under 50 characters'}),
            'context': SummernoteWidget(),
            'password': PasswordInput(attrs={'class': 'form-control',
                                             'placeholder': '4자이하'}),
        }


class QnasReplyForm(forms.ModelForm):
    class Meta:
        model = Qnas_reply
        fields = ('reply_user', 'reply_user_nickname', 'password', 'reply_user_nickname', 'context')

        widgets = {
            'reply_user': forms.HiddenInput,
            'reply_user_nickname': forms.TextInput(attrs={'placeholder': '5자이하'}),
            'password': PasswordInput(attrs={'placeholder': '4자이하'}),
            'context': forms.Textarea(attrs={'cols': 2, 'rows': 5}),
            'qnas': forms.HiddenInput,
            'parent': forms.HiddenInput,
        }


class QnasNoticeReplyForm(forms.ModelForm):
    class Meta:
        model = Qnas_notice_reply
        fields = ('reply_user', 'password', 'reply_user_nickname', 'context')

        widgets = {
            'reply_user': forms.HiddenInput,
            'reply_user_nickname': forms.TextInput(attrs={'placeholder': '5자이하'}),
            'password': PasswordInput(attrs={'placeholder': '4자이하'}),
            'context': forms.Textarea(attrs={'cols': 2, 'rows': 5}),
            'qnas_notice': forms.HiddenInput,
            'parent': forms.HiddenInput,
        }


