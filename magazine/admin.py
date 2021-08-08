from django.contrib import admin
from django.db.models import Q
from .models import *

admin.site.register(ImtBoards)
admin.site.register(ImtBoards_reply)
admin.site.register(ImtBoards_notice)
admin.site.register(ImtBoards_notice_reply)
admin.site.register(Qnas)
admin.site.register(Qnas_reply)
admin.site.register(Qnas_notice)
admin.site.register(Qnas_notice_reply)
admin.site.register(Imtsofts)
admin.site.register(Base_code)
admin.site.register(User)
admin.site.register(Notification)
admin.site.register(Message_header)
admin.site.register(Message_detail)
admin.site.register(Message_participaint)


# admin.site.register(Magazines)
def meagazineAutoWrite(modelAdmin, request, queryset):
    for row in queryset:
        if row.qnas == 0:
            category_qnas = row.category_qnas
            category_imtboards = row.imtboards
            title = row.title
            context = '<a href="/magazines_view/' + str(row.id) + '/">You can see the MAGAZINE here</a>'

            users = User.objects.filter(delete_yn='N').filter(~Q(id=0))
            for user in users:
                user.notification_cnt += 1
                noti = Notification.objects.create(user=user.id, types='004',
                                                   message='new magazine is posted',
                                                   url='/magazines_view/' + str(row.id) + '/',
                                                   params='',
                                                   preview=row.title[:100])
                user.save()
                noti.save()

            if row.qnas == 0:
                qnas = Qnas.objects.create(pub_user_nickname='MAGAZINES', password='0311',
                                         category_imtboards=category_imtboards,
                                         title=title, context=context, magazine_no=row.id)
                row.qnas = qnas.id

            if row.imtBoards == 0:
                imtBoards = ImtBoards.objects.create(pub_user_nickname='MAGAZINES', password='0311', category=category_qnas,
                                                     title=title, context=context, magazine_no=row.id)
                row.imtBoards = imtBoards.id

            row.save()


meagazineAutoWrite.short_description = "create the post in qnas/imtBoards"


class MagazinesAdmin(admin.ModelAdmin):
    actions = [meagazineAutoWrite]


admin.site.register(Magazines, MagazinesAdmin)
