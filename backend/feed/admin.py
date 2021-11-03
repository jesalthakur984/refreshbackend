from django.contrib import admin
from .models import Globaltag, Thought, Comment, Replycomment, Likecomment, Likethought
# Register your models here.

admin.site.register(Globaltag)
admin.site.register(Thought)
admin.site.register(Comment)
admin.site.register(Replycomment)
admin.site.register(Likethought)
admin.site.register(Likecomment)