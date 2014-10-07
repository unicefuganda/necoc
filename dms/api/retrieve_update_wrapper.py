from rest_framework_mongoengine.generics import RetrieveUpdateAPIView


class MongoRetrieveUpdateView(RetrieveUpdateAPIView):

    def pre_save(self, obj):
        if hasattr(obj, 'full_clean'):
            obj.full_clean()

