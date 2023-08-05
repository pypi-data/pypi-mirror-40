#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `errs` package."""

import pytest


from errs import errs, ErrorResult


def test_error_result_is_not_error():
    assert(ErrorResult().check() is False)


def test_no_error_return():
    @errs
    def return_me(*args):
        return args 
    out , err = return_me(1, 2, 3)
    assert(out == (1, 2, 3))


def test_no_error():
    @errs
    def no_raises():
        return 0
    out, err = no_raises()
    assert(err.check() == False)

def test_error():
    @errs
    def raises():
        raise Exception()
        return 0
    out, err = raises()
    assert(err.check() == True)
