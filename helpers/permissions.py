from rest_framework import permissions


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_bank_manager:
            return True
        else:
            return False
