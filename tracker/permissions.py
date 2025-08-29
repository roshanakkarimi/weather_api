from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if hasattr(obj, "members"):  # Project
            return user == obj.owner or user in obj.members.all()
        # Ticket/Comment -> check via related project
        project = getattr(obj, "project", getattr(obj, "ticket", None).project)
        return user == project.owner or user in project.members.all()