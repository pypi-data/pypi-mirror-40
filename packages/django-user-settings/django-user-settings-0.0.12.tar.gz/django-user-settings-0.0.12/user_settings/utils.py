from .models import UserSettings
from django.contrib.auth import get_user_model
from django.core.cache import cache

UserModel = get_user_model()

CACHE_PREFIX = "US_%s_%s"

CACHE_TIMEOUT = None


def get_user_setting(key, default_value=None, **kwargs):

    user = None
    if 'request' in kwargs:
        request = kwargs['request']
        user = request.user
        created_by = user

    if 'uid' in kwargs:
        if kwargs['uid'] is None or \
                kwargs['uid'] == '':
            user = None
        else:
            user = UserModel.objects.filter(id=kwargs['uid']).first()

    user_id = user.id if user is not None else None

    setting = cache.get(CACHE_PREFIX % (key, user_id))
    if setting:
        return setting

    user_setting = UserSettings.objects.filter(
        key=key, user_id=user_id).order_by('-created_at').first()
    if not user_setting:
        user_setting = UserSettings(key=key, value=default_value)
    user_setting_dict = user_setting.to_dict()
    cache.set((CACHE_PREFIX % (key, user_id)), user_setting_dict, CACHE_TIMEOUT)
    return user_setting_dict


def set_user_setting(key, value, **kwargs):
    user = None
    by_user = None
    if 'request' in kwargs:
        request = kwargs['request']
        user = request.user
        by_user = user
    if 'uid' in kwargs:
        if kwargs['uid'] is None or \
                kwargs['uid'] == '':
            user = None
        else:
            user = UserModel.objects.filter(id=kwargs['uid']).first()

    setting = get_user_setting(key, None, **kwargs)
    print("hihi", setting)
    if setting['id'] is not None:
        setting['value'] = value
        setting['modified_by'] = user
        setting['user'] = user
        user_setting = UserSettings.objects.filter(
            id=setting['id']).order_by('-created_at').first()
        if user_setting:
            user_setting.value = value
            user_setting.modified_by = by_user
            user_setting.user = user
            user_setting.save()
        else:
            # if this user setting somehow being cached but does not appear in database,
            # clear cache
            cache.delete((CACHE_PREFIX % (key, user.id if user.id else None)), version=None)
    else:
        # create
        user_setting = UserSettings.objects.create(
            key=key, value=value, created_by=by_user, user=user)

    if user_setting:
        cache.delete((CACHE_PREFIX % (key, user.id if user.id else None)), version=None)
        return True
    else:
        return False
