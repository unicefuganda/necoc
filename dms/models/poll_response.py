from dms.models import RapidProMessage


class PollResponse(RapidProMessage):

    def _assign_location(self):
        mobile_user = self.mobile_user()
        if mobile_user:
            return mobile_user.location