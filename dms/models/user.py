from mongoengine import ReferenceField
from mongoengine.django.auth import Group, User as MongoUser


class User(MongoUser):
    group = ReferenceField(Group)

    def has_perm(self, perm, obj=None):
        has_permission_in_group = self.group is not None and len(
            [p for p in self.group.permissions if p.content_type.app_label + '.' + p.codename == perm]) > 0
        return has_permission_in_group

    class Meta:
        app_label = 'dms'