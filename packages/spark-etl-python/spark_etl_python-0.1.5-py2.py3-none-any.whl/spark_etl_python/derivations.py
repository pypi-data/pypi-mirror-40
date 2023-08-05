# -*- coding: utf-8 -*-
from pyspark.sql.functions import concat_ws, regexp_replace


def derive_full_address(personal_info_rdd, address_columns, full_address_column_name='full_address'):
    """
    :param personal_info_rdd: A RDD with personal info. All columns from `personal_info_rdd` must be of type string.
    :param address_columns: Must reference columns from `personal_info_rdd`.
    :param full_address_column_name:
    :return:
    """
    personal_info_rdd = personal_info_rdd.withColumn(
        full_address_column_name,
        concat_ws("", *address_columns)
    )
    personal_info_rdd = personal_info_rdd.withColumn(
        full_address_column_name,
        remove_whitespaces(full_address_column_name)
    )
    return personal_info_rdd


def remove_whitespaces(column_name):
    return regexp_replace(column_name, ' ', '')
