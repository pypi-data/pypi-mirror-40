from datetime import datetime, timedelta

import requests

from . import settings


class OvChipCardAccount:
    def __init__(self, auth_code):
        self.authCode = auth_code

    @property
    def cards(self, locale="nl-NL"):
        post_data = {
            "authorizationToken": self.authCode,
            "locale": locale
        }
        data = Api.make_request(endpoint="/cards/list", data=post_data)

        cards = []

        for card in data['o']:
            post_data = {"authorizationToken": self.authCode,
                         "locale": locale,
                         "mediumId": card["mediumId"]}

            card = Api.make_request("/card/", data=post_data)
            cards.append(self.Card(card["o"]["card"], self.authCode))
        return cards

    class Card:
        def __init__(self, card, auth_code):
            self.balance = card['balance']
            self.balanceDate = card['balanceDate']
            self.mediumId = card['mediumId']
            self.expiryDate = card['expiryDate']
            self.alias = card['alias']
            self.defaultCard = card['defaultCard']
            self.autoReloadEnabled = card['autoReloadEnabled']
            self.autoReloadAccountNumber = card['autoReloadAccountNumber']
            self.autoReloadAmount = card['autoReloadAmount']
            self.autoReloadPaymentMandate = card['autoReloadPaymentMandate']
            self.autoReloadThresholdAmount = card['autoReloadThresholdAmount']
            self.status = card['status']
            self.statusAnnouncement = card['statusAnnouncement']
            self.type = card['type']
            self.authCode = auth_code
            self.transactionList = None

        def __str__(self):
            card = "Cardname:{alias}\t\tBalance:{balance}\n".format(alias=self.alias, balance=int(self.balance) // 100)
            return card

        @property
        def transactions(self, locale="nl-NL"):
            if not self.transactionList:
                self.transactionList = self.TransactionList(self.mediumId, self.authCode, locale)
            return self.transactionList

        class TransactionList:
            def __init__(self, card_id, auth_code, locale="nl-NL"):
                self.mediumId = card_id
                self.authCode = auth_code
                self.transactions = list()
                self.index = 0
                self.nextOffset = 0
                self.nextRequest = {
                    'startDate': (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                    'endDate': datetime.now().strftime("%Y-%m-%d"),
                    'offset': self.nextOffset,
                    "authorizationToken": self.authCode,
                    "locale": locale,
                    "mediumId": self.mediumId
                }
                trans = Api.make_request('/transactions', self.nextRequest)
                self.transactions = [self.Transaction(t) for t in trans["o"]["records"]]
                self.nextRequest.update(trans["o"]["nextRequestContext"])

            def __iter__(self):
                self.index = 0
                return self

            def __next__(self):
                if self.index is len(self.transactions):
                    trans = Api.make_request('/transactions', self.nextRequest)
                    if not trans["o"]["nextRequestContext"]:
                        raise StopIteration
                    self.nextRequest.update(trans["o"]["nextRequestContext"])
                    self.transactions.extend([self.Transaction(t) for t in trans["o"]["records"]])
                t = self.transactions[self.index]
                self.index += 1
                return t

            class Transaction:
                def __init__(self, transaction):
                    self.checkInInfo = transaction['checkInInfo']
                    self.checkInText = transaction['checkInText']
                    self.fare = transaction['fare']
                    self.fareCalculation = transaction['fareCalculation']
                    self.fareText = transaction['fareText']
                    self.modalType = transaction['modalType']
                    self.productInfo = transaction['productInfo']
                    self.productText = transaction['productText']
                    self.pto = transaction['pto']
                    self.transactionDateTime = int(str(transaction['transactionDateTime'])[:-3])
                    self.transactionInfo = transaction['transactionInfo']
                    self.transactionName = transaction['transactionName']
                    self.ePurseMut = transaction['ePurseMut']
                    self.ePurseMutInfo = transaction['ePurseMutInfo']
                    self.transactionExplanation = transaction['transactionExplanation']
                    self.transactionPriority = transaction['transactionPriority']


class Api:
    @classmethod
    def make_request(cls, endpoint, data):
        if not endpoint.startswith("/"):
            raise Exception("Endpoint should start with '/'")
        r = requests.post("{}{}".format(settings.BASE_URL, endpoint), data=data)
        r.raise_for_status()
        return r.json()

    @classmethod
    def login(cls, username, password):
        id_token = cls.get_token(username, password)
        return OvChipCardAccount(cls.get_authorization(id_token))

    @staticmethod
    def get_token(username, password, client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET):
        post_data = {"username": username,
                     "password": password,
                     "client_id": client_id,
                     "client_secret": client_secret,
                     "grant_type": "password",
                     "scope": "openid"}

        r = requests.post(settings.OAUTH_URL, data=post_data)
        r.raise_for_status()
        data = r.json()
        if 'id_token' not in data:
            raise AuthenticationError(data['error_description'])

        return data["id_token"]

    @staticmethod
    def get_authorization(id_token):
        post_data = {"authenticationToken": id_token}
        data = Api.make_request(endpoint="/api/authorize", data=post_data)
        return data['o']

    @staticmethod
    def refresh_token(refresh_token, client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET):
        post_data = {"refresh_token": refresh_token,
                     "client_id": client_id,
                     "client_secret": client_secret,
                     "grant_type": "refresh_token"}

        r = requests.post(settings.OAUTH_URL, data=post_data).json()
        r.raise_for_status()
        return r


class AuthenticationError(Exception):
    """No token was returned during authentication."""
