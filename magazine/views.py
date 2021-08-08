from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction
from django.contrib import auth
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
import re

# EMAIl authorization
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text

from .forms import *
from .models import *


# base
def base(request):
    return render(request, 'magazine/common/base.html', {})


# accounts
@transaction.atomic
def signin(request):
    notifications = ''
    new_msg_flag = False

    if request.method == 'POST':
        login_form = MagazineSigninForm(request, request.POST)
        if login_form.is_valid():
            auth.login(request, login_form.get_user())
            return redirect('/')
        else:
            messages.error(request, 'username or password not correct')
    else:
        if request.user.id:
            user = User.objects.get(id=request.user.id)
            notifications = Notification.objects.filter(user=user.id, delete_yn='N').order_by('-id')
            for notification in notifications:
                notification.preview = notification.preview
                notification.read_yn = 'Y'
                # if the prev_display_yn is 'N', there is no way to delete that noti.
                # more over, there is no ussage of delete_yn.
                # so automatically delete that noti to do not reload after now.
                if notification.prev_display_yn == 'N':
                    notification.delete_yn = 'Y'
                notification.save()
            user.notification_cnt = 0
            user.save()

            msg_participaint = Message_participaint.objects.filter(user=user.id, read_yn='N')
            if msg_participaint:
                new_msg_flag = True

        login_form = MagazineSigninForm()

    return render(request, 'magazine/accounts/signin.html',
                  {'form': login_form, 'notifications': notifications, 'new_msg_flag': new_msg_flag})


def signup(request):
    if request.method == "POST":
        form = MagazineUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.username
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            message = render_to_string('magazine/accounts/user_activate_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.id)).encode().decode(),
                                           'token': account_activation_token.make_token(user)
                                       })
            mail_subject = "[NOKOKO] Email authorization for signup"
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = "html"
            email.send()
            return render(request, 'magazine/accounts/activate_wating.html')
    else:
        form = MagazineUserCreationForm()

    return render(request, 'magazine/accounts/signup.html', {'form': form})


def activate(request, uid64, token):
    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.get(id=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('/signin')
    else:
        return HttpResponse('<script>'
                            'alert("Invalid access");'
                            'location.href="/"'
                            '</script>')


def signout(request):
    auth.logout(request)
    return redirect('/')


class UserPasswordResetView(PasswordResetView):
    template_name = 'magazine/accounts/password_reset.html'

    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'from_email': self.from_email,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
                'extra_email_context': self.extra_email_context,
            }
            form.save(**opts)
            return super().form_valid(form)
        else:
            return HttpResponse('<script>'
                                'alert("Please check your Email address");'
                                'location.href="/password_reset/"'
                                '</script>')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'magazine/accounts/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'magazine/accounts/password_reset_confirm.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


def UserPasswordResetCompleteView(request):
    return redirect('/signin')


def nicknameChange(request):
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        form = MagazineUserNicknameChangeForm(request.POST)

        if form.is_valid():
            user.nickname = form.cleaned_data['nickname']
            user.save()

            return HttpResponse('<script>'
                                'alert("Changed");'
                                'location.href=("/")'
                                '</script>')
    else:
        form = MagazineUserNicknameChangeForm(instance=user)

    return render(request, 'magazine/accounts/nickname_change.html', {'form': form})


def check_notification(request, notificationId):
    noti = Notification.objects.get(id=notificationId)
    url = noti.url
    noti.check_yn = 'Y'
    noti.save()
    return redirect(url)


def delete_notification(request):
    try:
        notificationId = request.POST.get('notificationId')
        noti = Notification.objects.get(id=notificationId)
        noti.delete_yn = 'Y'
        noti.save()

        return HttpResponse(200)
    except Exception as E:
        return HttpResponse(500)


def myinfo(request):
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        form = MagazineUserChangeForm(request.POST)

        if form.is_valid():
            user.category_imtboards_1 = form.cleaned_data['category_imtboards_1']
            user.category_imtboards_2 = form.cleaned_data['category_imtboards_2']
            user.category_imtboards_3 = form.cleaned_data['category_imtboards_3']
            user.category_qnas_1 = form.cleaned_data['category_qnas_1']
            user.category_qnas_2 = form.cleaned_data['category_qnas_2']
            user.category_qnas_3 = form.cleaned_data['category_qnas_3']
            user.save()

            return HttpResponse('<script>'
                                'alert("Changed");'
                                'location.href=("/")'
                                '</script>')
    else:
        form = MagazineUserChangeForm(instance=user)

    return render(request, 'magazine/accounts/myinfo.html', {'form': form})


def messageHeader(request):
    messageHeaderArray = []
    user = User.objects.get(id=request.user.id)
    msg_headers = Message_header.objects.raw("select a.id"
                                             " from magazine_message_header a"
                                             " join magazine_message_participaint b"
                                             " on b.msg_header = a.id"
                                             " where b.user = " + str(user.id) +
                                             " and b.participaint_yn = 'Y'")

    for msg_header in msg_headers:
        participaints = Message_participaint.objects.raw("select a.id, b.user, b.read_yn, b.new_cnt, c.nickname"
                                                         " from magazine_message_header a"
                                                         " join magazine_message_participaint b"
                                                         " on b.msg_header = a.id"
                                                         " join magazine_user c"
                                                         " on b.user = c.id"
                                                         " where a.id = " + str(msg_header.id))

        last_message = Message_detail.objects.filter(msg_header=msg_header.id) \
                           .order_by('-id')[:1]
        msg_participaint = Message_participaint.objects.get(msg_header=msg_header.id, user=user.id)
        new_cnt = msg_participaint.new_cnt
        if msg_participaint.read_yn == 'N':
            msg_participaint.read_yn = 'Y'
            msg_participaint.save()

        if last_message:
            last_message = last_message.values('context')[0].get('context')

        messageHeaderRow = {"msg_header": msg_header.id, "participaints": participaints, "last_message": last_message,
                            "new_cnt": new_cnt}
        messageHeaderArray.append(messageHeaderRow)

    return render(request, 'magazine/accounts/message_header.html', {'messageHeaderArray': messageHeaderArray})


@transaction.atomic
def messageDetail(request, msg_header_id, opponent):
    userId = request.user.id
    prevChatFlag = False

    if request.method == "POST":
        responseForm = MessageDetailForm(request.POST)

        if responseForm.is_valid():
            context = responseForm.data['context']
            seq = 1
            noti_user = User.objects.get(id=opponent)

            # When you initiate the chat
            if msg_header_id == 0:
                # Select my chatting list to find out ever talked with opponent
                myChats = Message_participaint.objects.filter(user=userId)
                for myChat in myChats:
                    # check if there is a list in which opponent also participated in my list
                    targetChat = Message_participaint.objects.get(msg_header=myChat.msg_header, user=opponent)
                    # If there is a list of both me and opponent
                    if targetChat:
                        # take that chat for re-participate
                        myChat.participaint_yn = 'Y'
                        targetChat.participaint_yn = 'Y'
                        targetChat.read_yn = 'N'
                        targetChat.new_cnt += 1
                        msg_header_id = myChat.msg_header
                        prevChatFlag = True
                        Notification.objects.create(user=opponent, types='007', prev_display_yn='N')
                        noti_user.notification_cnt += 1
                        myChat.save()
                        targetChat.save()
                        noti_user.save()
                        break
                # If there is no list, create new
                if not prevChatFlag:
                    msg_header = Message_header.objects.create()
                    Message_participaint.objects.create(msg_header=msg_header.id, user=userId, read_yn='Y', new_cnt=0)
                    Message_participaint.objects.create(msg_header=msg_header.id, user=opponent)
                    Notification.objects.create(user=opponent, types='007', prev_display_yn='N')
                    noti_user.notification_cnt += 1
                    noti_user.save()
                    msg_header_id = msg_header.id

            else:
                targetChat = Message_participaint.objects.get(msg_header=msg_header_id, user=opponent)
                targetChat.new_cnt += 1
                targetChat.read_yn = 'N'
                if targetChat.participaint_yn == 'N':
                    targetChat.participaint_yn = 'Y'

                Notification.objects.create(user=opponent, types='007', prev_display_yn='N')
                noti_user.notification_cnt += 1
                targetChat.save()
                noti_user.save()

                last_message = Message_detail.objects.filter(msg_header=msg_header_id).order_by('-id')[:1]
                if last_message:
                    seq = last_message[0].seq
                    seq += 1

            messageDetail = responseForm.save(commit=False)
            messageDetail.msg_header = msg_header_id
            messageDetail.seq = seq
            messageDetail.user = userId
            messageDetail.context = context
            messageDetail.ins_user = userId
            messageDetail.upt_user = userId

            messageDetail.save()

        return redirect('/message_detail/' + str(msg_header_id) + '/' + str(opponent))
    else:
        form = MessageDetailForm()

        if msg_header_id == 0:
            # Select my chatting list to find out ever talked with opponent
            myChats = Message_participaint.objects.filter(user=userId)
            if myChats:
                for myChat in myChats:
                    # check if there is a list in which opponent also participated in my list
                    targetChat = Message_participaint.objects.get(msg_header=myChat.msg_header, user=opponent)
                    # If there is a list of both me and opponent
                    if targetChat:
                        message_details = Message_detail.objects.filter(msg_header=myChat.msg_header)
                        myChat.new_cnt = 0
                        myChat.save()

                        return render(request, 'magazine/accounts/message_detail.html',
                                      {'messages': message_details, 'msg_header': myChat.msg_header, 'form': form})
            else:
                return render(request, 'magazine/accounts/message_detail.html',
                              {'messages': '', 'msg_header': 0, 'form': form})

        else:
            myChat = Message_participaint.objects.get(msg_header=msg_header_id, user=userId)
            myChat.new_cnt = 0
            myChat.save()
            message_details = Message_detail.objects.filter(msg_header=msg_header_id)
            return render(request, 'magazine/accounts/message_detail.html',
                          {'messages': message_details, 'msg_header': msg_header_id, 'form': form})


def message_delete(request):
    msg_header = request.POST.get('msg_header')
    myChat = Message_participaint.objects.get(msg_header=msg_header, user=request.user.id)
    myChat.participaint_yn = 'N'
    myChat.save()
    return HttpResponse('200')


# ImtBoards
@transaction.atomic
def imtBoards_write(request):
    if request.method == "POST":
        form = ImtBoardsWriteForm(request.POST)
        postUser = int(form['pub_user'].data)

        if form.is_valid():
            imtBoards = form.save(commit=False)
            imtBoards.ins_user = postUser
            imtBoards.upt_user = postUser

            categoryKey = form['category'].data
            categoryValue = Base_code.objects.filter(high_cat='001', middle_cat='001', low_cat='001',
                                                     key=categoryKey).values('value')
            categoryValue = categoryValue[0].get('value')
            notificationtargetUsers = User.objects.filter(category_imtboards_1=categoryKey, delete_yn='N') | \
                                      User.objects.filter(category_imtboards_2=categoryKey, delete_yn='N') | \
                                      User.objects.filter(category_imtboards_3=categoryKey, delete_yn='N')
            notificationPreview = form['context'].data
            notificationPreview = remove_tag(notificationPreview)[:100]

            imtBoards.save()
            for targetUser in notificationtargetUsers:
                if (targetUser.id != 0 and targetUser.id != postUser):
                    targetUser.notification_cnt += 1
                    noti = Notification.objects.create(user=targetUser.id, types='003',
                                                       message='new thing was posted about ' + categoryValue + ' in imtBoards',
                                                       url='/imtBoards_view/' + str(imtBoards.id), params='',
                                                       preview=notificationPreview)
                    targetUser.save()

            return redirect('/imtBoards_view/' + str(imtBoards.id))
    else:
        form = ImtBoardsWriteForm()

    return render(request, 'magazine/imtBoards/imtBoards_write.html', {'form': form})


def imtBoards_modify(request, postId):
    imtBoards = ImtBoards.objects.get(id=postId)

    if request.method == "POST":
        form = ImtBoardsWriteForm(request.POST)
        postUser = int(form['pub_user'].data)

        if form.is_valid():
            imtBoards.pub_user_nickname = form.cleaned_data['pub_user_nickname']
            imtBoards.password = form.cleaned_data['password']
            imtBoards.category = form.cleaned_data['category']
            imtBoards.title = form.cleaned_data['title']
            imtBoards.context = form.cleaned_data['context']
            imtBoards.ins_user = postUser
            imtBoards.upt_user = postUser
            imtBoards.save()
            return redirect('/imtBoards_view/' + str(imtBoards.id))
    else:
        form = ImtBoardsWriteForm(instance=imtBoards)
    return render(request, 'magazine/imtBoards/imtBoards_write.html', {'form': form})


def imtBoards_list(request):
    notices = ImtBoards_notice.objects.filter(delete_yn='N').order_by('-id')
    categories = Base_code.objects. \
        filter(high_cat='001', middle_cat='001', low_cat='001', delete_yn='N'). \
        only('key', 'value')

    searchCategoryKey = request.GET.get('searchCategory')
    if searchCategoryKey:
        searchCategoryValue = Base_code.objects.get(high_cat='001', middle_cat='001', low_cat='001',
                                                    key=searchCategoryKey).value
    else:
        searchCategoryValue = None
    searchWord = request.GET.get('searchWord')

    if (searchCategoryKey != None):
        if (searchCategoryKey == ''):
            all_posts = ImtBoards.objects.filter(title__contains=searchWord, delete_yn='N') \
                        | ImtBoards.objects.filter(pub_user_nickname__contains=searchWord, delete_yn='N') \
                            .order_by('-id')
        else:
            if (searchWord == ''):
                all_posts = ImtBoards.objects.filter(category=searchCategoryKey, delete_yn='N').order_by('-id')
            else:
                all_posts = ImtBoards.objects. \
                                filter(category=searchCategoryKey, title__contains=searchWord, delete_yn='N') \
                            | ImtBoards.objects. \
                                filter(category=searchCategoryKey, pub_user_nickname__contains=searchWord,
                                       delete_yn='N') \
                                .order_by('-id')
    else:
        all_posts = ImtBoards.objects.filter(delete_yn='N').order_by('-id')

    searchParams = {'searchWord': searchWord, 'searchCategoryKey': searchCategoryKey,
                    'searchCategoryValue': searchCategoryValue}

    for post in all_posts:
        if (post.latest_reply_dttm):
            timeinterval = (timezone.now() - post.latest_reply_dttm).total_seconds()
            if timeinterval < 30:
                post.latest_reply_dttm = 1
            elif timeinterval < 60:
                post.latest_reply_dttm = 2
            elif timeinterval < 60 * 5:
                post.latest_reply_dttm = 3
            elif timeinterval < 60 * 10:
                post.latest_reply_dttm = 4
            elif timeinterval < 60 * 30:
                post.latest_reply_dttm = 5
            elif timeinterval < 60 * 60:
                post.latest_reply_dttm = 6
            elif timeinterval < 60 * 60 * 24:
                post.latest_reply_dttm = 7
            else:
                post.latest_reply_dttm = 8

    for notice in notices:
        if (notice.latest_reply_dttm):
            timeinterval = (timezone.now() - notice.latest_reply_dttm).total_seconds()
            if timeinterval < 30:
                notice.latest_reply_dttm = 1
            elif timeinterval < 60:
                notice.latest_reply_dttm = 2
            elif timeinterval < 60 * 5:
                notice.latest_reply_dttm = 3
            elif timeinterval < 60 * 10:
                notice.latest_reply_dttm = 4
            elif timeinterval < 60 * 30:
                notice.latest_reply_dttm = 5
            elif timeinterval < 60 * 60:
                notice.latest_reply_dttm = 6
            elif timeinterval < 60 * 60 * 24:
                notice.latest_reply_dttm = 7
            else:
                notice.latest_reply_dttm = 8

    page = int(request.GET.get('p', 1))
    pagenator = Paginator(all_posts, 10)
    posts = pagenator.get_page(page)
    return render(request, 'magazine/imtBoards/imtBoards_list.html',
                  {'posts': posts, 'notices': notices, 'categories': categories, 'searchParams': searchParams})


@transaction.atomic
def imtBoards_view(request, pk):
    if request.method == "POST":
        responseForm = ImtBoardsReplyForm(request.POST)

        if responseForm.is_valid():
            imtBoardsId = int(responseForm.data['imtBoards'])
            parentSeq = int(responseForm.data['parent'])
            replyUserId = int(responseForm.data['reply_user'])
            reply = ImtBoards_reply.objects.filter(imtBoards=imtBoardsId).order_by('-id')[:1]
            seq = 1
            if reply:
                seq = reply[0].seq
                seq += 1

            imtBoardsReply = responseForm.save(commit=False)
            imtBoardsReply.imtBoards = imtBoardsId
            imtBoardsReply.seq = seq
            imtBoardsReply.reply_user = replyUserId
            imtBoardsReply.ins_user = replyUserId
            imtBoardsReply.upt_user = replyUserId

            imtBoards = ImtBoards.objects.get(id=imtBoardsId)
            imtBoards.reply_cnt += 1
            imtBoards.latest_reply_dttm = timezone.now()

            if imtBoards and imtBoards.pub_user != 0:
                pubUser = User.objects.get(id=imtBoards.pub_user)

            if parentSeq == 0:
                imtBoardsReply.parent = seq
                if imtBoards.pub_user != replyUserId:
                    if imtBoards.pub_user != 0:
                        noti = Notification.objects.create(user=imtBoards.pub_user, types='001',
                                                           message='someone replies to your post on imtBoards',
                                                           url='/imtBoards_view/' + str(imtBoards.id),
                                                           params='',
                                                           preview=responseForm.data['context'][:100])
                        pubUser.notification_cnt += 1
                        pubUser.save()
            else:
                imtBoardsReply.parent = parentSeq
                parentReplyUserId = ImtBoards_reply.objects.filter(imtBoards=imtBoards.id, seq=parentSeq).values(
                    'reply_user')
                parentReplyUserId = int(parentReplyUserId[0].get('reply_user'))
                parentReplyUser = User.objects.get(id=parentReplyUserId)

                if imtBoards.pub_user != replyUserId:
                    if parentReplyUserId != replyUserId:
                        if imtBoards.pub_user == parentReplyUserId:
                            if parentReplyUserId != 0:
                                noti = Notification.objects.create(user=parentReplyUserId, types='002',
                                                                   message='someone re-replies to your reply on imtBoards',
                                                                   url='/imtBoards_view/' + str(imtBoards.id),
                                                                   params='',
                                                                   preview=responseForm.data['context'][:100])
                                parentReplyUser.notification_cnt += 1
                                parentReplyUser.save()
                        else:
                            if imtBoards.pub_user != 0:
                                noti = Notification.objects.create(user=imtBoards.pub_user, types='001',
                                                                   message='someone replies to your post on imtBoards',
                                                                   url='/imtBoards_view/' + str(imtBoards.id),
                                                                   params='',
                                                                   preview=responseForm.data['context'][:100])
                                pubUser.notification_cnt += 1
                                pubUser.save()
                            if parentReplyUserId != 0:
                                noti = Notification.objects.create(user=parentReplyUserId, types='002',
                                                                   message='someone re-replies to your reply on imtBoards',
                                                                   url='/imtBoards_view/' + str(imtBoards.id),
                                                                   params='',
                                                                   preview=responseForm.data['context'][:100])
                                parentReplyUser.notification_cnt += 1
                                parentReplyUser.save()
                    else:
                        if imtBoards.pub_user != 0:
                            noti = Notification.objects.create(user=imtBoards.pub_user, types='001',
                                                               message='someone replies to your post on imtBoards',
                                                               url='/imtBoards_view/' + str(imtBoards.id),
                                                               params='',
                                                               preview=responseForm.data['context'][:100])
                            pubUser.notification_cnt += 1
                            pubUser.save()
                else:
                    if parentReplyUserId != replyUserId:
                        if parentReplyUserId != 0:
                            noti = Notification.objects.create(user=parentReplyUserId, types='002',
                                                               message='someone re-replies to your reply on imtBoards',
                                                               url='/imtBoards_view/' + str(imtBoards.id),
                                                               params='',
                                                               preview=responseForm.data['context'][:100])
                            parentReplyUser.notification_cnt += 1
                            parentReplyUser.save()

            imtBoards.save()
            imtBoardsReply.save()

            post = ImtBoards.objects.get(id=pk)
            return redirect('imtBoards_view', pk=post.id)
    else:
        post = ImtBoards.objects.get(id=pk)
        replies = ImtBoards_reply.objects.filter(imtBoards=post.id, delete_yn='N').order_by('parent')
        form = ImtBoardsReplyForm()
        post.read_cnt += 1
        post.save()

    return render(request, 'magazine/imtBoards/imtBoards_view.html', {'post': post, 'replies': replies, 'form': form})


@transaction.atomic
def imtBoards_notice_view(request, pk):
    if request.method == "POST":
        responseForm = ImtBoardsNoticeReplyForm(request.POST)

        if responseForm.is_valid():
            imtBoardsNoticeId = int(responseForm.data['imtBoards_notice'])
            parentSeq = int(responseForm.data['parent'])
            replyUserId = int(responseForm.data['reply_user'])
            reply = ImtBoards_notice_reply.objects.filter(imtBoards_notice=imtBoardsNoticeId).order_by('-id')[:1]
            seq = 1
            if reply:
                seq = reply[0].seq
                seq += 1

            imtBoardsNoticeReply = responseForm.save(commit=False)
            imtBoardsNoticeReply.imtBoards_notice = imtBoardsNoticeId
            imtBoardsNoticeReply.seq = seq
            imtBoardsNoticeReply.reply_user = replyUserId
            imtBoardsNoticeReply.ins_user = replyUserId
            imtBoardsNoticeReply.upt_user = replyUserId

            imtBoardsNotice = ImtBoards_notice.objects.get(id=imtBoardsNoticeId)
            imtBoardsNotice.reply_cnt += 1
            imtBoardsNotice.latest_reply_dttm = timezone.now()

            if parentSeq == 0:
                imtBoardsNoticeReply.parent = seq
            else:
                imtBoardsNoticeReply.parent = parentSeq
                parentReplyUserId = ImtBoards_reply.objects.filter(imtBoards=imtBoardsNotice.id, seq=parentSeq).values(
                    'reply_user')
                parentReplyUserId = int(parentReplyUserId[0].get('reply_user'))
                parentReplyUser = User.objects.get(id=parentReplyUserId)

                if parentReplyUserId != replyUserId:
                    if parentReplyUserId != 0:
                        noti = Notification.objects.create(user=parentReplyUserId, types='002',
                                                           message='someone re-replies to your reply on imtBoards',
                                                           url='/imtBoards_notice_view/' + str(imtBoardsNotice.id),
                                                           params='',
                                                           preview=responseForm.data['context'][:100])
                        parentReplyUser.notification_cnt += 1
                        parentReplyUser.save()

            imtBoardsNotice.save()
            imtBoardsNoticeReply.save()

            notice = ImtBoards_notice.objects.get(id=pk)
            return redirect('imtBoards_notice_view', pk=notice.id)
    else:
        notice = ImtBoards_notice.objects.get(id=pk)
        replies = ImtBoards_notice_reply.objects.filter(imtBoards_notice=notice.id, delete_yn='N').order_by('parent')
        form = ImtBoardsNoticeReplyForm()
        notice.read_cnt += 1
        notice.save()

    return render(request, 'magazine/imtBoards/imtBoards_notice_view.html',
                  {'notice': notice, 'replies': replies, 'form': form})


# Qna
@transaction.atomic
def qnas_write(request):
    if request.method == "POST":
        form = QnasWriteForm(request.POST)
        postUser = int(form['pub_user'].data)

        if form.is_valid():
            qnas = form.save(commit=False)
            qnas.ins_user = postUser
            qnas.upt_user = postUser

            categoryKey = form['category'].data
            categoryValue = Base_code.objects.filter(high_cat='001', middle_cat='002', low_cat='001',
                                                     key=categoryKey).values('value')
            categoryValue = categoryValue[0].get('value')
            notificationtargetUsers = User.objects.filter(category_qnas_1=categoryKey, delete_yn='N') | \
                                      User.objects.filter(category_qnas_2=categoryKey, delete_yn='N') | \
                                      User.objects.filter(category_qnas_3=categoryKey, delete_yn='N')
            notificationPreview = form['context'].data
            notificationPreview = remove_tag(notificationPreview)[:100]

            qnas.save()

            for targetUser in notificationtargetUsers:
                if (targetUser.id != 0 and targetUser.id != postUser):
                    targetUser.notification_cnt += 1
                    noti = Notification.objects.create(user=targetUser.id, types='003',
                                                       message='new thing was posted about ' + categoryValue + ' in N.B.hoods',
                                                       url='/qnas_view/' + str(qnas.id), params='',
                                                       preview=notificationPreview)
                    targetUser.save()

            return redirect('/qnas_view/' + str(qnas.id))
    else:
        form = QnasWriteForm()
    return render(request, 'magazine/qnas/qnas_write.html', {'form': form})


def qnas_modify(request, postId):
    qnas = Qnas.objects.get(id=postId)

    if request.method == "POST":
        form = QnasWriteForm(request.POST)
        postUser = int(form['pub_user'].data)

        if form.is_valid():
            qnas.pub_user_nickname = form.cleaned_data['pub_user_nickname']
            qnas.password = form.cleaned_data['password']
            qnas.category = form.cleaned_data['category']
            qnas.title = form.cleaned_data['title']
            qnas.context = form.cleaned_data['context']
            qnas.ins_user = postUser
            qna.upt_user = postUser
            qna.save()
            return redirect('/qnas_view/' + str(qnas.id))
    else:
        form = QnasWriteForm(instance=qnas)
    return render(request, 'magazine/qnas/qnas_write.html', {'form': form})


def qnas_list(request):
    notices = Qnas_notice.objects.filter(delete_yn='N').order_by('-id')
    categories = Base_code.objects \
        .filter(high_cat='001', middle_cat='002', low_cat='001', delete_yn='N') \
        .only('key', 'value')

    searchCategoryKey = request.GET.get('searchCategory')
    if searchCategoryKey:
        searchCategoryValue = Base_code.objects.get(high_cat='001', middle_cat='002', low_cat='001',
                                                    key=searchCategoryKey).value
    else:
        searchCategoryValue = None
    searchWord = request.GET.get('searchWord')

    if (searchCategoryKey != None):
        if (searchCategoryKey == ''):
            all_posts = Qnas.objects.filter(title__contains=searchWord, delete_yn='N') \
                        | Qnas.objects.filter(pub_user_nickname__contains=searchWord, delete_yn='N') \
                            .order_by('-id')
        else:
            if (searchWord == ''):
                all_posts = Qnas.objects.filter(category=searchCategoryKey, delete_yn='N').order_by('-id')
            else:
                all_posts = Qnas.objects. \
                                filter(category=searchCategoryKey, title__contains=searchWord, delete_yn='N') \
                            | Qnas.objects. \
                                filter(category=searchCategoryKey, pub_user_nickname__contains=searchWord,
                                       delete_yn='N') \
                                .order_by('-id')
    else:
        all_posts = Qnas.objects.filter(delete_yn='N').order_by('-id')

    searchParams = {'searchWord': searchWord, 'searchCategoryKey': searchCategoryKey,
                    'searchCategoryValue': searchCategoryValue}

    for post in all_posts:
        if (post.latest_reply_dttm):
            timeinterval = (timezone.now() - post.latest_reply_dttm).total_seconds()
            if timeinterval < 30:
                post.latest_reply_dttm = 1
            elif timeinterval < 60:
                post.latest_reply_dttm = 2
            elif timeinterval < 60 * 5:
                post.latest_reply_dttm = 3
            elif timeinterval < 60 * 10:
                post.latest_reply_dttm = 4
            elif timeinterval < 60 * 30:
                post.latest_reply_dttm = 5
            elif timeinterval < 60 * 60:
                post.latest_reply_dttm = 6
            elif timeinterval < 60 * 60 * 24:
                post.latest_reply_dttm = 7
            else:
                post.latest_reply_dttm = 8

    for notice in notices:
        if (notice.latest_reply_dttm):
            timeinterval = (timezone.now() - notice.latest_reply_dttm).total_seconds()
            if timeinterval < 30:
                notice.latest_reply_dttm = 1
            elif timeinterval < 60:
                notice.latest_reply_dttm = 2
            elif timeinterval < 60 * 5:
                notice.latest_reply_dttm = 3
            elif timeinterval < 60 * 10:
                notice.latest_reply_dttm = 4
            elif timeinterval < 60 * 30:
                notice.latest_reply_dttm = 5
            elif timeinterval < 60 * 60:
                notice.latest_reply_dttm = 6
            elif timeinterval < 60 * 60 * 24:
                notice.latest_reply_dttm = 7
            else:
                notice.latest_reply_dttm = 8

    page = int(request.GET.get('p', 1))
    pagenator = Paginator(all_posts, 10)
    posts = pagenator.get_page(page)
    return render(request, 'magazine/qnas/qnas_list.html',
                  {'posts': posts, 'notices': notices, 'categories': categories, 'searchParams': searchParams})


@transaction.atomic
def qnas_view(request, pk):
    if request.method == "POST":
        responseForm = QnasReplyForm(request.POST)

        if responseForm.is_valid():
            qnasId = int(responseForm.data['qnas'])
            parentSeq = int(responseForm.data['parent'])
            replyUserId = int(responseForm.data['reply_user'])
            reply = Qnas_reply.objects.filter(qnas=qnasId).order_by('-id')[:1]
            seq = 1
            if reply:
                seq = reply[0].seq
                seq += 1

            qnasReply = responseForm.save(commit=False)
            qnasReply.qnas = qnasId
            qnasReply.seq = seq
            qnasReply.reply_user = replyUserId
            qnasReply.ins_user = replyUserId
            qnasReply.upt_user = replyUserId

            qnas = Qnas.objects.get(id=qnasId)
            qnas.reply_cnt += 1
            qnas.latest_reply_dttm = timezone.now()

            if qnas and qnas.pub_user != 0:
                pubUser = User.objects.get(id=qnas.pub_user)

            if parentSeq == 0:
                qnasReply.parent = seq
                if qnas.pub_user != replyUserId:
                    if qnas.pub_user != 0:
                        Notification.objects.create(user=qnas.pub_user, types='001',
                                                    message='someone replies to your post on N.B.hoods',
                                                    url='/qnas_view/' + str(qnas.id),
                                                    params='',
                                                    preview=responseForm.data['context'][:100])
                        pubUser.notification_cnt += 1
                        pubUser.save()
            else:
                qnasReply.parent = parentSeq
                parentReplyUserId = ImtBoards_reply.objects.filter(imtBoards=qnas.id, seq=parentSeq).values(
                    'reply_user')
                parentReplyUserId = int(parentReplyUserId[0].get('reply_user'))
                parentReplyUser = User.objects.get(id=parentReplyUserId)

                if qnas.pub_user != replyUserId:
                    if parentReplyUserId != replyUserId:
                        if qnas.pub_user == parentReplyUserId:
                            if parentReplyUserId != 0:
                                Notification.objects.create(user=parentReplyUserId, types='002',
                                                            message='someone re-replies to your reply on N.B.hoods',
                                                            url='/qnas_view/' + str(qnas.id),
                                                            params='',
                                                            preview=responseForm.data['context'][:100])
                                parentReplyUser.notification_cnt += 1
                                parentReplyUser.save()
                        else:
                            if qnas.pub_user != 0:
                                Notification.objects.create(user=qnas.pub_user, types='001',
                                                            message='someone replies to your post on N.B.hoods',
                                                            url='/qnas_view/' + str(qnas.id),
                                                            params='',
                                                            preview=responseForm.data['context'][:100])
                                pubUser.notification_cnt += 1
                                pubUser.save()
                            if parentReplyUserId != 0:
                                Notification.objects.create(user=parentReplyUserId, types='002',
                                                            message='someone re-replies to your reply on N.B.hoods',
                                                            url='/qnas_view/' + str(qnas.id),
                                                            params='',
                                                            preview=responseForm.data['context'][:100])
                                parentReplyUser.notification_cnt += 1
                                parentReplyUser.save()
                    else:
                        if qnas.pub_user != 0:
                            Notification.objects.create(user=qnas.pub_user, types='001',
                                                        message='someone replies to your post on N.B.hoods',
                                                        url='/qnas_view/' + str(qnas.id),
                                                        params='',
                                                        preview=responseForm.data['context'][:100])
                            pubUser.notification_cnt += 1
                            pubUser.save()
                else:
                    if parentReplyUserId != replyUserId:
                        if parentReplyUserId != 0:
                            Notification.objects.create(user=parentReplyUserId, types='002',
                                                        message='someone re-replies to your reply on N.B.hoods',
                                                        url='/qnas_view/' + str(qnas.id),
                                                        params='',
                                                        preview=responseForm.data['context'][:100])
                            parentReplyUser.notification_cnt += 1
                            parentReplyUser.save()

            qnas.save()
            qnasReply.save()

            post = Qnas.objects.get(id=pk)
            return redirect('qnas_view', pk=post.id)
    else:
        post = Qnas.objects.get(id=pk)
        replies = Qnas_reply.objects.filter(qnas=post.id, delete_yn='N').order_by('parent')
        form = QnasReplyForm()
        post.read_cnt += 1
        post.save()

    return render(request, 'magazine/qnas/qnas_view.html',
                  {'post': post, 'replies': replies, 'form': form})


@transaction.atomic
def qnas_notice_view(request, pk):
    if request.method == "POST":
        responseForm = QnasNoticeReplyForm(request.POST)

        if responseForm.is_valid():
            qnasNoticeId = int(responseForm.data['qnas_notice'])
            parentSeq = int(responseForm.data['parent'])
            replyUserId = int(responseForm.data['reply_user'])
            reply = Qnas_notice_reply.objects.filter(qnas_notice=qnasNoticeId).order_by(
                '-id')[:1]
            seq = 1
            if reply:
                seq = reply[0].seq
                seq += 1

            qnasNoticeReply = responseForm.save(commit=False)
            qnasNoticeReply.qnas_notice = qnasNoticeId
            qnasNoticeReply.seq = seq
            qnasNoticeReply.reply_user = replyUserId
            qnasNoticeReply.ins_user = replyUserId
            qnasNoticeReply.upt_user = replyUserId

            qnasNotice = Qnas_notice.objects.get(id=qnasNoticeId)
            qnasNotice.reply_cnt += 1
            qnasNotice.latest_reply_dttm = timezone.now()

            if parentSeq == 0:
                qnasNoticeReply.parent = seq
            else:
                qnasNoticeReply.parent = parentSeq
                parentReplyUserId = ImtBoards_reply.objects.filter(imtBoards=qnasNotice.id,
                                                                   seq=parentSeq).values(
                    'reply_user')
                parentReplyUserId = int(parentReplyUserId[0].get('reply_user'))
                parentReplyUser = User.objects.get(id=parentReplyUserId)

                if parentReplyUserId != replyUserId:
                    if parentReplyUserId != 0:
                        Notification.objects.create(user=parentReplyUserId, types='002',
                                                    message='someone re-replies to your reply on N.B.hoods',
                                                    url='/qnas_notice_view/' + str(
                                                        qnaNotice.id),
                                                    params='',
                                                    preview=responseForm.data['context'][:100])
                        parentReplyUser.notification_cnt += 1
                        parentReplyUser.save()

            qnaNotice.save()
            qnaNoticeReply.save()

            notice = Qnas_notice.objects.get(id=pk)
            return redirect('qna_notice_view', pk=notice.id)
    else:
        notice = Qnas_notice.objects.get(id=pk)
        replies = Qnas_notice_reply.objects.filter(qna_notice=notice.id, delete_yn='N').order_by(
            'parent')
        form = QnasNoticeReplyForm()
        notice.read_cnt += 1
        notice.save()

    return render(request, 'magazine/qna/qna_notice_view.html',
                  {'notice': notice, 'replies': replies, 'form': form})


# Magazines
def magazines_list(request):
    all_posts = Magazines.objects.filter(delete_yn='N').order_by('-id')

    page = int(request.GET.get('p', 1))
    pagenator = Paginator(all_posts, 10)
    posts = pagenator.get_page(page)
    return render(request, 'magazine/magazines/magazines_list.html', {'posts': posts})


def magazines_view(request, pk):
    post = Magazines.objects.get(id=pk)

    return render(request, 'magazine/magazines/magazines_view.html', {'post': post})


# Imtsofts
def imtsofts_list(request):
    all_posts = Imtsofts.objects.filter(delete_yn='N').order_by('-id')

    page = int(request.GET.get('p', 1))
    pagenator = Paginator(all_posts, 10)
    posts = pagenator.get_page(page)
    return render(request, 'magazine/imtsofts/imtsofts_list.html', {'posts': posts})


# Common
def checkPassword(request):
    try:
        passwordFromUser = request.POST.get('passwordFromUser')
        target = request.POST.get('target')
        postId = request.POST.get('postId')
        replySeq = 0
        if request.POST.get('replySeq'):
            replySeq = request.POST.get('replySeq')

        if target == 'qna_post':
            passwordFromDB = Qnas.objects.get(id=postId).password
        elif target == 'qna_reply':
            passwordFromDB = Qnas_reply.objects.get(qna=postId, seq=replySeq).password
        elif target == 'qna_notice_reply':
            passwordFromDB = Qnas_notice_reply.objects.get(qna_notice=postId, seq=replySeq).password
        elif target == 'imtBoards_post':
            passwordFromDB = ImtBoards.objects.get(id=postId).password
        elif target == 'imtBoards_reply':
            passwordFromDB = ImtBoards_reply.objects.get(imtBoards=postId, seq=replySeq).password
        elif target == 'imtBoards_notice_reply':
            passwordFromDB = ImtBoards_notice_reply.objects.get(imtBoards_notice=postId, seq=replySeq).password

        if passwordFromUser == passwordFromDB:
            return HttpResponse(200)
        else:
            return HttpResponse(304)
    except Exception as E:
        return HttpResponse(500)


def deletePost(request):
    try:
        target = request.POST.get('target')
        postId = request.POST.get('postId')
        board = ''

        if target == 'qnas':
            board = Qnas
        elif target == 'imtBoards':
            board = ImtBoards

        post = board.objects.get(id=postId)
        post.delete_yn = 'Y'
        post.save()
        return HttpResponse(200)
    except Exception as E:
        return HttpResponse(500)


def deleteReply(request):
    try:
        target = request.POST.get('target')
        postId = request.POST.get('postId')
        replySeq = request.POST.get('replySeq')
        board = ''

        if target == 'qnas':
            board = Qnas_reply
            reply = board.objects.get(qna=postId, seq=replySeq)
        elif target == 'qnas_notice':
            board = Qnas_notice_reply
            reply = board.objects.get(qna_notice=postId, seq=replySeq)
        if target == 'imtBoards':
            board = ImtBoards_reply
            reply = board.objects.get(imtBoards=postId, seq=replySeq)
        elif target == 'imtBoards_notice':
            board = ImtBoards_notice_reply
            reply = board.objects.get(imtBoards_notice=postId, seq=replySeq)

        reply.delete_yn = 'Y'
        reply.save()
        return HttpResponse(200)
    except Exception as E:
        return HttpResponse(500)


def bad_request_error_page(request, exception):
    response = render(request, 'magazine/common/400errors.html')
    response.status_code = 400
    return response


def unauthorized_error_page(request):
    response = render(request, 'magazine/common/401errors.html')
    response.status_code = 401
    return response


def forbidden_error_page(request, exception):
    response = render(request, 'magazine/common/403errors.html')
    response.status_code = 403
    return response


def page_not_found_error_page(request, exception):
    response = render(request, 'magazine/common/404errors.html')
    response.status_code = 404
    return response


def server_error_page(request):
    response = render(request, 'magazine/common/500errors.html')
    response.status_code = 500
    return response


def bad_gateway_error_page(request):
    response = render(request, 'magazine/common/502errors.html')
    response.status_code = 502
    return response


def remove_tag(content):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', content)
    return cleantext
