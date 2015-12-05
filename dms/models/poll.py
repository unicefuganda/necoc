from django.db.models.loading import get_app
from mongoengine import *

from dms.models.base import BaseModel
from dms.utils.signal_receivers import add_yesno_categories_to_poll, auto_close_old_polls
from django.conf import settings


POLL_TYPE_CHOICES = ['yesno', 'text']

# accepted yes keywords
YES_WORDS = ['yes', 'yeah', 'yep', 'yay', 'y']

# accepted no keywords
NO_WORDS = ['no', 'nope', 'nah', 'nay',  'n']

# Poll Response Evaluation Templates
# The standard template allows for any amount of whitespace at the beginning,
# followed by the alias(es) for a particular category, followed by any non-
# alphabetical character, or the end of the message
STARTSWITH_PATTERN_TEMPLATE = '^\s*(%s)(\s|[^a-zA-Z]|$)'

CONTAINS_PATTERN_TEMPLATE = '^.*\s*(%s)(\s|[^a-zA-Z]|$)'


class Poll(BaseModel):
    name = StringField()
    question = StringField(max_length=160)
    keyword = StringField(max_length=10, unique=True)
    target_locations = ListField()
    log = StringField()
    type = StringField(max_length=5, choices=POLL_TYPE_CHOICES, default=POLL_TYPE_CHOICES[1])
    default_response = StringField(default=settings.DEFAULT_POLL_RESPONSE[1])
    open = BooleanField(default=True)

    def add_yesno_categories(self):
        app = get_app('dms')
        ResponseCategoryModel = app.poll_response.ResponseCategory

        """
        This creates a generic yes/no poll categories for a particular poll
        """
        yes_category = ResponseCategoryModel.objects(**dict(poll=self, name='yes')).first() or \
                        ResponseCategoryModel(**dict(name='yes', poll=self)).save()
        no_category = ResponseCategoryModel.objects(**dict(poll=self, name='no')).first() or \
                        ResponseCategoryModel(**dict(name='no', poll=self)).save()
        unknown_category = ResponseCategoryModel.objects(**dict(poll=self, name='unknown')).first() or \
                        ResponseCategoryModel(**dict(name='unknown', poll=self, default=True, error_category=True)).save()

        # add one rule to yes category per language
        no_words = getattr(settings, 'NO_WORDS', NO_WORDS)
        yes_words = getattr(settings, 'YES_WORDS', YES_WORDS)

        no_rule_string = '|'.join(no_words)
        yes_rule_string = '|'.join(yes_words)

        startswith_template = getattr(settings, 'STARTSWITH_PATTERN_TEMPLATE', STARTSWITH_PATTERN_TEMPLATE)

        Rule(**dict(response_category=yes_category,
                    regex=(startswith_template % yes_rule_string),
                    rule_type=Rule.TYPE_REGEX,
                    rule_string=(startswith_template % yes_rule_string))).save()

        Rule(**dict(response_category=no_category,
                    regex=(startswith_template % no_rule_string),
                    rule_type=Rule.TYPE_REGEX,
                    rule_string=(startswith_template % no_rule_string))).save()

    def is_yesno_poll(self):
        app = get_app('dms')
        ResponseCategoryModel = app.poll_response.ResponseCategory
        return ResponseCategoryModel.objects(poll=self).count() == 3 and \
               ResponseCategoryModel.objects(poll=self, name='yes').count() and \
               ResponseCategoryModel.objects(poll=self, name='no').count() and \
               ResponseCategoryModel.objects(poll=self, name='unknown').count()

    def responses(self):
        from dms.models import PollResponse
        return PollResponse.objects(poll=self)

    def number_of_responses(self):
        return self.responses().count()

class Rule(Document):
    """
    A rule is a regular expression that an incoming message text might
    satisfy to belong in a particular category.  A message must satisfy
    one or more rules to belong to a category.
    """

    contains_all_of = 1
    contains_one_of = 2

    TYPE_STARTSWITH = 'sw'
    TYPE_CONTAINS = 'c'
    TYPE_REGEX = 'r'
    RULE_CHOICES = (
        (TYPE_STARTSWITH, 'Starts With'),
        (TYPE_CONTAINS, 'Contains'),
        (TYPE_REGEX, 'Regex (advanced)')
    )

    RULE_DICTIONARY = {
        TYPE_STARTSWITH: 'Starts With',
        TYPE_CONTAINS: 'Contains',
        TYPE_REGEX: 'Regex (advanced)',
    }
    response_category = ReferenceField('ResponseCategory')
    regex = StringField(max_length=256)
    rule_type = StringField(max_length=2, choices=RULE_CHOICES)
    rule_string = StringField(max_length=256)
    # rule = IntField(choices=((contains_all_of, "contains_all_of"), (contains_one_of, "contains_one_of"),), null=True)


# If its a yes/no poll categories/buckets for yes/no responses should be created automatically
post_save.connect(add_yesno_categories_to_poll)

# We always keep settings.ALWAYS_OPEN_POLLS open and ready to receive responses at all time
# we mark the rest as closed
post_save.connect(auto_close_old_polls)