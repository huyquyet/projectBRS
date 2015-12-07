import os

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.activity.models import Activities
from app.user.models import UserProfile, Profile
from projectBRS import settings

__author__ = 'FRAMGIA\nguyen.huy.quyet'


@receiver(post_save, sender=User)
def create_super_user(sender, instance, create, raw, using, update_fields, **kwargs):
    """
    Creat a Profile for User when a newly user is created,
    """
    if not create:
        return

    if instance.is_staff:
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.save()

        profile = Profile(_id=instance.pk)
        profile.avatar = ''
        profile.full_name = ''
        profile.other_name = ''
        profile.save()

        activity = Activities(_id=instance.pk)
        activity.save()
        avatar_dir = os.path.join(settings.MEDIA_ROOT, str(instance.pk), settings.AVATAR_DIR)
        cover_dir = os.path.join(settings.MEDIA_ROOT, str(instance.pk), settings.COVER_DIR)

        try:
            os.makedirs(avatar_dir, mode=0o700)
            os.makedirs(cover_dir, mode=0o700)
        except OSError as err:
            user_profile.delete()
            profile.delete()
            activity.delete()
            print('Created user\'s error: {}'.format(err.strerror))

            # @receiver(post_delete, sender = User)
            # def delete_user(sender, instance, delete, raw)
