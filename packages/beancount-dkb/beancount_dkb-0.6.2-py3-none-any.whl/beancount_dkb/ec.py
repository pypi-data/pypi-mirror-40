import csv
import locale
import re
from datetime import datetime

from beancount.core import data
from beancount.core.amount import Amount
from beancount.core.number import Decimal
from beancount.ingest import importer

from ._common import InvalidFormatError, change_locale

FIELDS = (
    'Buchungstag',
    'Wertstellung',
    'Buchungstext',
    'Auftraggeber / Begünstigter',
    'Verwendungszweck',
    'Kontonummer',
    'BLZ',
    'Betrag (EUR)',
    'Gläubiger-ID',
    'Mandatsreferenz',
    'Kundenreferenz',
)


class ECImporter(importer.ImporterProtocol):
    def __init__(self, iban, account, currency='EUR',
                 numeric_locale='de_DE.UTF-8', file_encoding='utf-8'):
        self.account = account
        self.currency = currency
        self.numeric_locale = numeric_locale
        self.file_encoding = file_encoding

        self._expected_header_regex = re.compile(
            r'^"Kontonummer:";"' +
            re.escape(re.sub(r'\s+', '', iban, flags=re.UNICODE)) + r'\s',
            re.IGNORECASE
        )
        self._date_from = None
        self._date_to = None
        self._balance = None

    def file_account(self, _):
        return self.account

    def file_date(self, file_):
        self.extract(file_)

        return self._date_to

    def identify(self, file_):
        with open(file_.name, encoding=self.file_encoding) as fd:
            line = fd.readline().strip()

        return self._expected_header_regex.match(line)

    def extract(self, file_):
        entries = []
        line_index = 0
        closing_balance_index = -1

        with change_locale(locale.LC_NUMERIC, self.numeric_locale):
            with open(file_.name, encoding=self.file_encoding) as fd:
                # Header
                line = fd.readline().strip()
                line_index += 1

                if not self._expected_header_regex.match(line):
                    raise InvalidFormatError()

                # Empty line
                line = fd.readline().strip()
                line_index += 1

                if line:
                    raise InvalidFormatError()

                # Meta
                lines = [fd.readline().strip() for _ in range(3)]
                raw_meta = {}

                reader = csv.reader(lines, delimiter=';',
                                    quoting=csv.QUOTE_MINIMAL, quotechar='"')

                for line in reader:
                    key, value, _ = line
                    line_index += 1

                    if key.startswith('Von'):
                        raw_meta['Von'] = value

                        self._date_from = datetime.strptime(
                            value, '%d.%m.%Y').date()
                    elif key.startswith('Bis'):
                        raw_meta['Bis'] = value

                        self._date_to = datetime.strptime(
                            value, '%d.%m.%Y').date()
                    elif key.startswith('Kontostand vom'):
                        raw_meta['Kontostand'] = value

                        if not raw_meta.get('Bis'):
                            raise InvalidFormatError()

                        if key != 'Kontostand vom {}:'.format(raw_meta['Bis']):
                            raise InvalidFormatError()

                        self._balance = Amount(
                            locale.atof(value.rstrip(' EUR'), Decimal),
                            self.currency)
                        closing_balance_index = line_index

                # Another empty line
                line = fd.readline().strip()
                line_index += 1

                if line:
                    raise InvalidFormatError()

                # Data entries
                reader = csv.DictReader(fd, delimiter=';',
                                        quoting=csv.QUOTE_MINIMAL,
                                        quotechar='"')

                for line in reader:
                    meta = data.new_metadata(file_.name, line_index)

                    amount = None
                    if line['Betrag (EUR)']:
                        amount = Amount(locale.atof(line['Betrag (EUR)'],
                                        Decimal),
                                        self.currency)
                    date = datetime.strptime(
                        line['Buchungstag'], '%d.%m.%Y').date()

                    if line['Verwendungszweck'] == 'Tagessaldo':
                        if amount:
                            entries.append(
                                data.Balance(meta, date, self.account, amount,
                                             None, None)
                            )
                    else:
                        description = '{} {}'.format(
                            line['Buchungstext'],
                            line['Verwendungszweck']
                        )

                        postings = [
                            data.Posting(self.account, amount, None, None,
                                         None, None)
                        ]

                        entries.append(
                            data.Transaction(
                                meta, date, self.FLAG,
                                line['Auftraggeber / Begünstigter'],
                                description, data.EMPTY_SET, data.EMPTY_SET,
                                postings
                            )
                        )

                    line_index += 1

                # Closing Balance
                meta = data.new_metadata(file_.name, closing_balance_index)
                entries.append(
                    data.Balance(meta, self._date_to, self.account,
                                 self._balance, None, None)
                )

            return entries
