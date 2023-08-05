#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `spark_etl_python` package."""

import pytest
import pandas as pd

from pandas.testing import assert_frame_equal

from spark_etl_python.derivations import derive_full_address


def assert_frame_equal_with_sort(actual, expected, keycolumns=None, ignore_rows_columns_order=True):
    """
    Assert data frames are equal, regardless of line order
    :param actual:
    :param expected:
    :param keycolumns:
    :param ignore_rows_columns_order:
    :return:
    """
    if keycolumns is None:
        keycolumns = expected.columns.tolist()

    results_sorted = actual.sort_values(by=keycolumns).reset_index(drop=True)
    expected_sorted = expected.sort_values(by=keycolumns).reset_index(drop=True)
    assert_frame_equal(results_sorted, expected_sorted, check_like=ignore_rows_columns_order)


def test_derive_full_address(spark_session):
    personal_info_df = pd.DataFrame([
        {
            'street_number': '35',
            'street': 'rue de vaugirard',
            'city': 'paris',
            'postal_code': '75001',
        },
        {
            'street_number': None,
            'street': 'rue de vaugirard',
            'city': None,
            'postal_code': '75001',
        },
    ])
    personal_info_with_fulladdress_df_expected = pd.DataFrame([
        {
            'street_number': '35',
            'street': 'rue de vaugirard',
            'city': 'paris',
            'postal_code': '75001',
            'full_address': '35ruedevaugirardparis75001',
        },
        {
            'street_number': None,
            'street': 'rue de vaugirard',
            'city': None,
            'postal_code': '75001',
            'full_address': 'ruedevaugirard75001',
        },
    ])

    personal_info_rdd = spark_session.createDataFrame(personal_info_df)
    personal_info_with_fulladdress_df_actual = derive_full_address(
        personal_info_rdd,
        ['street_number', 'street', 'city', 'postal_code']
    ).toPandas()
    assert_frame_equal_with_sort(
        personal_info_with_fulladdress_df_actual, personal_info_with_fulladdress_df_expected,
    )


def test_content():
    df_expected = pd.DataFrame({'a': [0]})
    df_actual = pd.DataFrame({'a': [0]})
    assert_frame_equal(df_expected, df_actual)

def filter_df(df):
    return df.filter(df.year >= 2000)


def test_do_filter(spark_session):
    """ test that a single event is parsed correctly
    Args:
        spark_session: test fixture SQLContext
    """
    data_pandas = pd.DataFrame({'make': ['Jaguar', 'MG', 'MINI', 'Rover', 'Lotus'],
                                'registration': ['AB98ABCD', 'BC99BCDF', 'CD00CDE', 'DE01DEF', 'EF02EFG'],
                                'year': [1998, 1999, 2000, 2001, 2002]})
