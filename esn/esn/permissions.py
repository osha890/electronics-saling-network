from rest_framework.permissions import BasePermission

from employees.models import Employee


class IsActiveEmployeeOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated or not user.is_active:
            return False
        if user.is_superuser:
            return True
        return Employee.objects.filter(user=user).exists()
