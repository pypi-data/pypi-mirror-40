#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dealstat` package."""

import pytest


from dealstat import dealstat
from dealstat import address



def test_something():
    result = dealstat.unique_id()

def test_address1():

    result = address.to_components('335 East 13th St, New York NY')

    assert result['address'] == '335 East 13th St'
    assert result['city'] == 'New York'
    assert result['state'] == 'NY'


def test_address2():

    result = address.to_components('302 Barwood Drive Fort Hayton Beach, Florida 32547')
    assert result['address'] == '302 Barwood Drive'
    assert result['city'] == 'Fort Hayton Beach'
    assert result['state'] == 'FL'

