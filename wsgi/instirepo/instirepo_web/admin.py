from django.contrib import admin
from instirepo_web.models import *

admin.site.register(UserProfiles)
admin.site.register(College)
admin.site.register(Universities)
admin.site.register(Branches)
admin.site.register(StudentYears)
admin.site.register(Batches)
admin.site.register(PostCategories)
admin.site.register(Posts)
admin.site.register(PollChoices)
admin.site.register(CommentsOnPosts)
admin.site.register(UpvotesOnPosts)
admin.site.register(PollsVotes)
admin.site.register(SavedPosts)
admin.site.register(FlaggedPosts)
admin.site.register(PostVisibility)
admin.site.register(PostSeens)
admin.site.register(UpvotesOnUsers)
admin.site.register(SavedPostVisibilities)
admin.site.register(SavedPostVisibilitiesAttributes)
admin.site.register(Messages)
