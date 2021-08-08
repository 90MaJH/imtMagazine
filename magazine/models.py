from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Commons
class Base_code(models.Model):
    high_cat = models.CharField(blank=True, max_length=3)
    high_cat_dscpt = models.CharField(blank=True, max_length=20)
    middle_cat = models.CharField(blank=True, max_length=3)
    middle_cat_dscpt = models.CharField(blank=True, max_length=20)
    low_cat = models.CharField(blank=True, max_length=3)
    low_cat_dscpt = models.CharField(blank=True, max_length=20)
    key = models.CharField(blank=True, max_length=3)
    value = models.CharField(blank=True, max_length=255)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " _ " + self.value

categories_imtboards = Base_code.objects.filter(high_cat='001', middle_cat='001', low_cat='001', delete_yn='N').only('key', 'value')
categories_imtboards_choices = ()
for category in categories_imtboards:
    tmp_category = (category.key, category.value)
    categories_imtboards_choices += (tmp_category,)
# categories_imtboards_choices = (('001', 'initial'),)

categories_qnas = Base_code.objects.filter(high_cat='001', middle_cat='002', low_cat='001', delete_yn='N').only('key', 'value')
categories_qnas_choices = ()
for category in categories_qnas:
    tmp_category = (category.key, category.value)
    categories_qnas_choices += (tmp_category,)
# categories_qnas_choices = (('001', 'initial'),)

notification_types = Base_code.objects.filter(high_cat='002', middle_cat='001', low_cat='001', delete_yn='N').only('key', 'value')
notification_types_choices = ()
for notification_type in notification_types:
    tmp_notification_type = (notification_type.key, notification_type.value)
    notification_types_choices += (tmp_notification_type,)
# notification_types_choices = (('001', 'initial'),)

channels = Base_code.objects.filter(high_cat='001', middle_cat='003', low_cat='001', delete_yn='N').only('key', 'value')
channels_choices = ()
for channel in channels:
    tmp_channel = (channel.key, channel.value)
    channels_choices += (tmp_channel,)
# channels_choices = (('001', 'initial'),)

# Accounts
class User(AbstractUser):
    username = models.EmailField(max_length=255, unique=True, verbose_name='email type ID')
    nickname = models.CharField(max_length=10, unique=True)
    category_imtboards_1 = models.CharField(max_length=3, default='000', choices=categories_imtboards_choices, verbose_name='select 1st favorite category')
    category_imtboards_2 = models.CharField(max_length=3, default='000', choices=categories_imtboards_choices, verbose_name='select 2nd favorite category')
    category_imtboards_3 = models.CharField(max_length=3, default='000', choices=categories_imtboards_choices, verbose_name='select 3rd favorite category')
    category_qnas_1 = models.CharField(max_length=3, default='000', choices=categories_qnas_choices, verbose_name='select 1st favorite category')
    category_qnas_2 = models.CharField(max_length=3, default='000', choices=categories_qnas_choices, verbose_name='select 2nd favorite category')
    category_qnas_3 = models.CharField(max_length=3, default='000', choices=categories_qnas_choices, verbose_name='select 3rd favorite category')
    notification_cnt = models.IntegerField(default=0)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

class Notification(models.Model):
    user = models.IntegerField(default=0)
    types = models.CharField(max_length=3, default='000', choices=notification_types_choices)
    message = models.CharField(max_length=50, default='')
    preview = models.CharField(max_length=100, default='')
    url = models.URLField(blank=True)
    params = models.JSONField(default='')
    read_yn = models.CharField(default='N', max_length=1)
    check_yn = models.CharField(default='N', max_length=1)
    delete_yn = models.CharField(default='N', max_length=1)
    prev_display_yn = models.CharField(default='Y', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

class Message_header(models.Model):
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

class Message_participaint(models.Model):
    msg_header = models.IntegerField(default=0)
    user = models.IntegerField(default=0)
    participaint_yn = models.CharField(default='Y', max_length=1)
    read_yn = models.CharField(default='N', max_length=1)
    new_cnt = models.IntegerField(default=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

class Message_detail(models.Model):
    msg_header = models.IntegerField(default=0)
    seq = models.IntegerField(default=0)
    user = models.IntegerField(default=0)
    context = models.CharField(default='', max_length=255)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

# ImtBoards
class ImtBoards(models.Model):
    pub_dttm = models.DateTimeField(default=timezone.now)
    pub_user = models.IntegerField(default=0, verbose_name='writer')
    pub_user_nickname = models.CharField(max_length=10, default='', verbose_name='writer')
    password = models.CharField(default='0000', max_length=4)
    category = models.CharField(max_length=3, default='000', choices=categories_imtboards_choices)
    title = models.CharField(max_length=50, default='')
    context = models.TextField()
    read_cnt = models.IntegerField(default=0)
    reply_cnt = models.IntegerField(default=0)
    latest_reply_dttm = models.DateTimeField(null=True)
    magazine_no = models.IntegerField(default=0)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " _ " + self.title


class ImtBoards_notice(models.Model):
    pub_dttm = models.DateTimeField(default=timezone.now)
    password = models.CharField(default='noko', max_length=4)
    title = models.CharField(max_length=50, default='')
    context = models.TextField()
    read_cnt = models.IntegerField(default=0)
    reply_cnt = models.IntegerField(default=0)
    latest_reply_dttm = models.DateTimeField(null=True)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " _ " + self.title


class ImtBoards_reply(models.Model):
    imtBoards = models.IntegerField(default=0)
    seq = models.IntegerField(default=1, verbose_name='replyNo')
    password = models.CharField(default='0000', max_length=4)
    reply_dttm = models.DateTimeField(default=timezone.now)
    reply_user = models.IntegerField(default=0, verbose_name='replier')
    reply_user_nickname = models.CharField(max_length=10, default='', verbose_name='replier')
    context = models.TextField()
    parent = models.IntegerField(default=0)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " _ " + self.reply_user_nickname + " : " + self.context[0:20]


class ImtBoards_notice_reply(models.Model):
    imtBoards_notice = models.IntegerField(default=0)
    seq = models.IntegerField(default=1, verbose_name='replyNo')
    password = models.CharField(default='0000', max_length=4)
    reply_dttm = models.DateTimeField(default=timezone.now)
    reply_user = models.IntegerField(default=0, verbose_name='replier')
    reply_user_nickname = models.CharField(max_length=10, default='', verbose_name='writer')
    context = models.TextField()
    parent = models.IntegerField(default=0)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " _ " + self.reply_user_nickname + " : " + self.context[0:20]


# Qnas
class Qnas(models.Model):
    pub_dttm = models.DateTimeField(default=timezone.now)
    pub_user = models.IntegerField(default=0, verbose_name='writer')
    pub_user_nickname = models.CharField(max_length=10, default='', verbose_name='writer')
    password = models.CharField(default='0000', max_length=4)
    category = models.CharField(max_length=3, default='000', choices=categories_qnas_choices)
    title = models.CharField(max_length=50, default='')
    context = models.TextField()
    read_cnt = models.IntegerField(default=0)
    reply_cnt = models.IntegerField(default=0)
    latest_reply_dttm = models.DateTimeField(null=True)
    magazine_no = models.IntegerField(default=0)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " _ " + self.title


class Qnas_notice(models.Model):
    pub_dttm = models.DateTimeField(default=timezone.now)
    password = models.CharField(default='noko', max_length=4)
    title = models.CharField(max_length=50, default='')
    context = models.TextField()
    read_cnt = models.IntegerField(default=0)
    reply_cnt = models.IntegerField(default=0)
    latest_reply_dttm = models.DateTimeField(null=True)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " _ " + self.title


class Qnas_reply(models.Model):
    qnas = models.IntegerField(default=0)
    seq = models.IntegerField(default=1, verbose_name='replyNo')
    password = models.CharField(default='0000', max_length=4)
    reply_dttm = models.DateTimeField(default=timezone.now)
    reply_user = models.IntegerField(default=0, verbose_name='replier')
    reply_user_nickname = models.CharField(max_length=10, default='', verbose_name='replier')
    context = models.TextField()
    parent = models.IntegerField(default=0)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " _ " + self.reply_user_nickname + " : " + self.context[0:20]


class Qnas_notice_reply(models.Model):
    qnas_notice = models.IntegerField(default=0)
    seq = models.IntegerField(default=1, verbose_name='replyNo')
    password = models.CharField(default='0000', max_length=4)
    reply_dttm = models.DateTimeField(default=timezone.now)
    reply_user = models.IntegerField(default=0, verbose_name='replier')
    reply_user_nickname = models.CharField(max_length=10, default='', verbose_name='writer')
    context = models.TextField()
    parent = models.IntegerField(default=0)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " _ " + self.reply_user_nickname + " : " + self.context[0:20]


# Magazines
class Magazines(models.Model):
    pub_dttm = models.DateTimeField(default=timezone.now)
    pub_user = models.IntegerField(default=0, verbose_name='writer')
    pub_user_nickname = models.CharField(max_length=10, default='MAGAZINE', verbose_name='writer')
    category_qnas = models.CharField(max_length=3, default='000', choices=categories_qnas_choices)
    category_imtboards = models.CharField(max_length=3, default='000', choices=categories_imtboards_choices)
    title = models.CharField(max_length=50, default='')
    img1 = models.ImageField(blank=True)
    img2 = models.ImageField(blank=True)
    img3 = models.ImageField(blank=True)
    img4 = models.ImageField(blank=True)
    img5 = models.ImageField(blank=True)
    qnas = models.IntegerField(default=0)
    imtBoards = models.IntegerField(default=0)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " _ " + self.title


# Imtsofts
class Imtsofts(models.Model):
    pub_dttm = models.DateTimeField(default=timezone.now)
    pub_user = models.IntegerField(default=0, verbose_name='writer')
    pub_user_nickname = models.CharField(max_length=10, default='admin', verbose_name='nickname')
    channel = models.CharField(max_length=3, default='000', choices=channels_choices)
    title = models.CharField(max_length=300, default='')
    url = models.URLField(max_length=500)
    delete_yn = models.CharField(default='N', max_length=1)
    ins_dttm = models.DateTimeField(default=timezone.now)
    ins_user = models.IntegerField(default=0)
    upt_dttm = models.DateTimeField(default=timezone.now)
    upt_user = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " _ " + self.title
