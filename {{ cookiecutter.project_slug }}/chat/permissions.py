from rest_framework.permissions import BasePermission


class ChatPermission(BasePermission):
    def has_object_permission(self, request, view, chat):
        if request.method in ('GET', ):
            return chat.members.filter(pk=request.user.pk).exists()
        elif request.method in ('PUT', 'PATCH', 'DELETE'):
            return chat.admin.pk == request.user.pk
        return False


class ChatMessagePermission(BasePermission):
    def has_object_permission(self, request, view, chat_message):
        if request.method in ('GET', ):
            return chat_message.chat.members.filter(pk=request.user.pk).exists()
        elif request.method in ('PUT', 'PATCH', 'DELETE'):
            return (
                chat_message.user.pk == request.user.pk or
                chat_message.chat.admin.pk == request.user.pk
            )
        return False
