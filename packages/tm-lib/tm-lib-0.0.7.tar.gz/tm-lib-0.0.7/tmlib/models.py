from typing import Tuple

from mongoengine import Document, EmbeddedDocument, connect, fields

from tmlib.settings import Settings


class Checkin(EmbeddedDocument):
    symbol = fields.StringField()
    broker = fields.StringField()
    last_checkin = fields.DateTimeField()


class Registration(EmbeddedDocument):
    account_number = fields.IntField()
    broker = fields.StringField()
    rego_key = fields.StringField()
    checkins = fields.EmbeddedDocumentListField(Checkin)
    maximum_lots = fields.DecimalField()


class License(EmbeddedDocument):
    minion_name = fields.StringField()
    wp_membership_id = fields.IntField()
    minion_license = fields.StringField()
    support_expires = fields.StringField()
    account_registrations = fields.EmbeddedDocumentListField(Registration)


class Customer(Document):
    login = fields.EmailField()
    given_name = fields.StringField()
    surname = fields.StringField()
    licenses = fields.EmbeddedDocumentListField(License)

    meta = {
        'collection': 'customers',
        'indexes':
            [{
                'fields': ['login'],
                'unique': True
            }]
    }

    def __str__(self):
        return "Customer <%s>" % self.login

    def get_licence(self):
        return self.licenses[0]

    def get_account_registration(self, *, minion_name: str,
                                 account_number: int, broker_name: str) -> Registration:
        """
        Get account registration by minion name and account_number
        :param minion_name:
        :param account_number:
        :param broker_name:
        :return: Optional[Registration]
        """
        try:
            license: License = next(
                l for l in self.licenses if l.minion_name == minion_name
            )
            account_registration: Registration = next(
                ac for ac in license.account_registrations
                if ac.account_number == account_number and ac.broker == broker_name)
            return account_registration
        except (StopIteration, AttributeError) as err:
            raise Customer.DoesNotExist(str(err))


class Parameter(Document):
    note_to_me = fields.StringField()
    minion_name = fields.StringField()
    broker_name = fields.ListField()
    edition = fields.ListField()
    version = fields.StringField()
    filedata = fields.StringField()

    @classmethod
    def get_or_create(cls, minion_name: str, version: str) -> Tuple['Parameter', bool]:
        try:
            p: Parameter = cls.objects.get(minion_name=minion_name, version=version)
            created = False
        except cls.DoesNotExist:
            p: Parameter = cls(minion_name=minion_name, version=version)
            created = True
        return p, created

    meta = {
        'collection': 'parameters',
        'indexes':
            [{
                'fields': ['minion_name', 'version'],
                'unique': True
            }]
    }


connect('trading_minions', host=Settings.MONGO_URI)
