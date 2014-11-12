from mongoengine import ReferenceField
from mongoengine.django.auth import User, Group


class User(User):
    group = ReferenceField(Group)

    def has_perm(self, perm, obj=None):
        has_permission = super(User, self).has_perm(perm, obj)
        has_permission_in_group = len(
            [p for p in self.group.permissions if p.content_type.app_label + '.' + p.codename == perm]) > 0
        return has_permission or has_permission_in_group

    class Meta:
        app_label = 'dms'