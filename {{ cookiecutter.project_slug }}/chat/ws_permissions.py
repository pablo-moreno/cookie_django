from .models import Chat


class Permission(object):
    def __init__(self, scope):
        self.scope = scope

    def has_permission(self, *args, **kwargs):
        raise NotImplementedError('You must implement has_permission method!')


class Any(Permission):
    def has_permission(self, *args, **kwargs):
        return True


class IsChatMember(Permission):
    def has_permission(self):
        user = self.scope['user']
        uuid = self.scope['url_route']['kwargs']['uuid']
        chat = Chat.objects.filter(uuid=uuid)

        return chat.members.filter(user=user).exists()
