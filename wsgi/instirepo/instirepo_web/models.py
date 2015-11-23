from django.db import models
from django.contrib.auth.models import User


class UserProfiles(models.Model):
    # username,first_name,last_name,email,password,groups,uses_permissions,is_staff,is_active,is_superuser,last_login,date_joined
    full_name = models.CharField(max_length=255)
    userIDAuth = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    profile_details_json_object = models.TextField(null=True, blank=True)
    profile_image = models.TextField(null=True, blank=True)
    device_id = models.TextField(max_length=200, null=True, blank=True)
    is_student_coordinator = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)
    is_senior_professor = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    enrollment_number = models.CharField(max_length=255, null=True, blank=True)
    has_provided_college_details = models.BooleanField(default=False)

    college = models.ForeignKey('College', null=True)
    batch = models.ForeignKey('Batches', null=True, blank=True)
    branch = models.ForeignKey('Branches', null=True, blank=True)
    user_obj = models.ForeignKey(User, related_name='user_profile')
    university = models.ForeignKey('Universities', null=True, blank=True)
    year = models.ForeignKey('StudentYears', null=True, blank=True)

    is_email_shown_to_others = models.BooleanField(default=False)
    is_mobile_shown_to_others = models.BooleanField(default=False)
    resume = models.TextField(null=True, blank=True)
    designation = models.CharField(max_length=255, default='Student', null=True)
    about = models.TextField(null=True, blank=True)
    has_reached_post_limit = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Universities(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class College(models.Model):
    university = models.ForeignKey('Universities')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Branches(models.Model):
    branch_name = models.TextField(max_length=255)
    college = models.ForeignKey(College)

    def __str__(self):
        return self.branch_name


class StudentYears(models.Model):
    branch = models.ForeignKey(Branches)
    year_name = models.TextField(max_length=255)
    admission_year = models.IntegerField()
    passout_year = models.IntegerField()
    has_passed_out = models.BooleanField(default=False)

    def __str__(self):
        return self.year_name + ' ' + str(self.admission_year) + ' ' + str(self.passout_year)


class Batches(models.Model):
    year = models.ForeignKey(StudentYears)
    batch_name = models.TextField(max_length=255)

    def __str__(self):
        return self.batch_name


class PostCategories(models.Model):
    EVENT = 'event'
    PLACEMENT = 'placement'
    POLL = 'poll'
    OTHER = 'other'

    SPECIAL_POSTS = (
        (EVENT, 'Event'),
        (PLACEMENT, 'Placement'),
        (POLL, 'Poll'),
        (OTHER, 'Other'),
    )

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='posts_categories_images', null=True, blank=True)
    is_public = models.BooleanField(default=False)
    type = models.CharField(max_length=255, choices=SPECIAL_POSTS, default=OTHER)
    color = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Posts(models.Model):
    category = models.ForeignKey(PostCategories)
    heading = models.TextField(null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='posts_images', null=True, blank=True)
    company_name = models.TextField(null=True, blank=True)
    uploader = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    is_by_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.heading


class PollChoices(models.Model):
    post = models.ForeignKey(Posts)
    choice = models.TextField()
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice


class CommentsOnPosts(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User)
    post = models.ForeignKey(Posts)
    time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.comment


class UpvotesOnPosts(models.Model):
    is_upvote = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Posts)
    time = models.DateTimeField(auto_now=True)


class PollsVotes(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Posts)
    choice = models.ForeignKey(PollChoices)
    is_active = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice


class SavedPosts(models.Model):
    post = models.ForeignKey(Posts)
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post


class FlaggedPosts(models.Model):
    post = models.ForeignKey(Posts)
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post


class PostVisibility(models.Model):
    individual = models.ForeignKey(User, null=True, blank=True)
    batch = models.ForeignKey(Batches, null=True, blank=True)
    branch = models.ForeignKey(Branches, null=True, blank=True)
    year = models.ForeignKey(StudentYears, null=True, blank=True)
    college = models.ForeignKey(College, null=True, blank=True)
    university = models.ForeignKey(Universities, null=True, blank=True)

    post = models.ForeignKey(Posts)
    time = models.DateTimeField(auto_now=True)


class PostSeens(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Posts)
    time = models.DateTimeField(auto_now=True)


class UpvotesOnUsers(models.Model):
    user = models.ForeignKey(User, related_name='user_being_voted')
    upvoter = models.ForeignKey(User, related_name='user_who_voted')
    is_upvote = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)
