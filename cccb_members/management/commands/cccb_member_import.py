
"""
CCCB Member import
"""

import pprint

import csv
from datetime import date

from django.core.management.base import BaseCommand

def _decode_membership_type(row):
    """
    Decode membership type: 
        'r'     Regular
        _       Reduced?
    """
    if row[5] == "r":
        return "regular"

    return "reduced"

def _decode_payment(row):
    """
    Decode payment method:
        'm'     'direct_debit', monthly
        'd'     'manual', monthly
    """
    payment = row[9]
    interval = 'monthly'
    method = 'manual'
    if payment == 'm':
        method = 'direct_debit'

    return {
        "method": method,
        "interval": interval,
        "iban": _decode_string(row[8]),
    }


def _decode_address(row):
    """Build address from fields"""
    address = [row[11], "{} {}".format(row[12], row[13])]

    return "\n".join(address)


def _decode_boolean(data):
    """Decode boolean"""
    return data == "1"


def _decode_memberships(row):
    """Decode memberships"""
    return {
        "cccb": _decode_boolean(row[17]),
        "ccc": _decode_boolean(row[18]),
    }

def _decode_date(data):
    """Decode datetime from string"""
    try:
        value = [int(v) for v in data.split(".")]
    except ValueError:
        return None

    if not value or len(value) < 3:
        return None

    return date(value[2], value[1], value[0])

def _decode_membership_start(row):
    """When did the membership start"""
    return _decode_date(row[14])


def _decode_membership_end(row):
    return _decode_date(row[15])


def _decode_string(value):
    """Decode string value"""
    if  value:
        value = value.strip()

    if not value:
        return None

    return value


def _decode_int(value):
    """Decode integer value"""
    try:
        return int(value)
    except ValueError:
        return None


def _decode_member(row):
    """Read row and get member info"""
    member = {
        "number": _decode_int(row[0]),
        "email": _decode_string(row[1]),
        "name": _decode_string(row[2]),
        "nick": _decode_string(row[3]),
        "membership": {
            "fee": _decode_int(row[4]),
            "type": _decode_membership_type(row),
            "since": _decode_membership_start(row),
            "until": _decode_membership_end(row),
            "active": _decode_boolean(row[16]),
        },
        "iban": row[7],
        "payment": _decode_payment(row),
        "address": _decode_address(row),
        "memberships": _decode_memberships(row),
    }

    return member

def _read_memberslist(filename):
    """Read the memberslist"""
    with open(filename, newline="") as f:
        reader = csv.reader(f)

        return [_decode_member(row) for row in reader][1:]


class Command(BaseCommand):
    help = "Import CCCB members from CSV"

    def add_arguments(self, parser):
        """Add cli flags"""
        parser.add_argument(
            "-f", "--filename",
            required=True,
            help="The CSV member list export")

    def handle(self, *args, **options):
        """Import members from CSV list"""
        print("Importing member from: {}".format(
            options["filename"]))

        members = _read_memberslist(options["filename"])

        pprint.pprint(members)
