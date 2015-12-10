import re
from django.conf import settings
from mongoengine import *
from dms.models.poll import Poll, Rule

from dms.models.message import RapidProMessageBase
from dms.utils.message_utils import fuzzy_match_strings
from dms.utils.rapidpro_message_utils import split_text
from dms.utils.signal_receivers import categorise_yesno_response


class PollResponse(RapidProMessageBase):
    poll = ReferenceField('Poll')
    categories = ReferenceField('PollResponseCategory', default=None)
    has_errors = BooleanField(default=False)

    def _assign_location(self):
        mobile_user = self.mobile_user()
        if mobile_user:
            return mobile_user.location

    def save(self, *args, **kwargs):
        self.poll = self.poll or self._assign_poll()
        return super(PollResponse, self).save(*args, **kwargs)

    def _assign_poll(self):
        text = self.split_text()
        if len(text):
            active_keywords = [poll.keyword for poll in self._open()]
            if len(active_keywords):
                for kw in active_keywords:
                    if kw in text:
                        return Poll.objects(keyword=kw).order_by('-created_at').first()
                    else:
                        return self._assign_if_is_yesno()

    def _assign_if_is_yesno(self):
        if self.text.strip() in settings.YES_WORDS or self.text.strip() in settings.NO_WORDS:
            return Poll.objects(ptype='yesno', open=True).order_by('-created_at').first()
        elif fuzzy_match_strings(self.text, settings.YES_WORDS) or fuzzy_match_strings(self.text, settings.NO_WORDS):
            return Poll.objects(ptype='yesno', open=True).order_by('-created_at').first()
        else:
            # return None
            #always asign uninteligibal responses to the last yes/no poll (possibility to distort poll results)
            return Poll.objects(ptype='yesno', open=True).order_by('-created_at').first()

    def _open(self):
        return Poll.objects(open=True).order_by('-created_at')

    def split_text(self):
        try:
            split_message = re.findall(r"[\w']+", self.text)
        except TypeError:
            split_message = []
        return map(lambda x: x.strip(), split_message)


    def _regex_compare_str(self, txt, rule):
        regex = re.compile(rule.regex, re.IGNORECASE | re.UNICODE)
        return regex.search(txt.lower())

    def poll_name(self):
        if self.poll:
            return self.poll.name

    def categories(self):
        return ResponseCategory.objects(poll=self.poll)

    def is_categorized(self):
        return PollResponseCategory.objects(poll_response=self).count() > 0

    def get_response_category(self):
        return PollResponseCategory.objects(poll_response=self).first()

    def process_response(self):
        outgoing_message = self.poll.default_response

        if self.categories().count() > 0:
            for category in self.categories():
                for rule in category.rules():
                    if self._regex_compare_str(self.text, rule):
                        PollResponseCategory(**dict(poll_response=self, response_category=category)).save()

        if not self.is_categorized():
            start_str = settings.POLL_RESPONSE_START_STR
            if self.text.lower().startswith(start_str.lower()):
                txt = self.text[len(start_str):len(self.text)].strip()
                txt = re.sub('[!@#$.,-]', '', txt)
                if self.categories().count() > 0:
                    for category in self.categories():
                        for rule in category.rules():
                            if self._regex_compare_str(txt, rule):
                                PollResponseCategory(**dict(poll_response=self, response_category=category)).save()

        #last resort, fuzzy match to yes' and nos
        if not self.is_categorized():
            for txt in self.split_text():
                if fuzzy_match_strings(txt, settings.YES_WORDS, match_ratio=96):
                    category = ResponseCategory.objects(**dict(name='yes', poll=self.poll)).first()
                    PollResponseCategory(**dict(poll_response=self, response_category=category)).save()
                    break
                elif fuzzy_match_strings(txt, settings.NO_WORDS, match_ratio=96):
                    category = ResponseCategory.objects(**dict(name='no', poll=self.poll)).first()
                    PollResponseCategory(**dict(poll_response=self, response_category=category)).save()
                    break
                else:
                    pass

        #categorization fails, give up
        if not self.is_categorized():
            unknown_category = self.categories().filter(default=True).first()
            PollResponseCategory(**dict(poll_response=self, response_category=unknown_category)).save()
            if unknown_category.error_category:
                self.has_errors = True
                outgoing_message = unknown_category.response

        self.save()

        if not outgoing_message:
            return self, None,
        else:
            return self, outgoing_message,

class ResponseCategory(Document):
    name = StringField()
    response = StringField(min_length=0)
    poll = ReferenceField('Poll')
    error_category = BooleanField(default=False)
    default = BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def rules(self):
        return Rule.objects(response_category=self)


class PollResponseCategory(Document):
    response_category = ReferenceField('ResponseCategory')
    poll_response = ReferenceField('PollResponse')

    def __unicode__(self):
        return ResponseCategory.objects(id=self.response_category.id).first()


#bucketing of yes/no poll in YES and NO buckets
post_save.connect(categorise_yesno_response)
