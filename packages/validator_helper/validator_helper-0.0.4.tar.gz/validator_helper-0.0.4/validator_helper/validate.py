#!/usr/bin/env python

import pandas as pd
import numpy as np
import logging


def find_all_columns(csv_file, columns_to_exclude, range_fraction=0.1):
    """
    Sometimes, csv files have way too many columns to make you want to list them all. This method will create
    a list of column objects for you, excluding whatever columns are in the columns_to_exclude_list.
    If columns are numeric/ranges acceptable range is set to 10 percent (range_fraction, modify if you want) of the
    average of the field. If you need more fine-grained control over this,
    :param csv_file: Full path to csv file.
    :param columns_to_exclude: List of column headers you DO NOT want Column objects created for.
    :param range_fraction: How much numeric columns can vary by, as a fraction of the mean of the column
    :return: List of column objects to be used by a Validator
    """
    column_list = list()
    df = pd.read_csv(csv_file)
    column_headers = list(df.columns)
    for column in column_headers:
        if column not in columns_to_exclude:
            # Check if column appears to be numeric
            if np.issubdtype(df[column].dtype, np.number):
                # Find average.
                average_column_value = df[column].mean()
                # Create column with acceptable range of plus/minus of range_fraction
                acceptable_range = average_column_value * range_fraction
                # Now finally create the column.
                column_list.append(Column(name=column,
                                          column_type='Range',
                                          acceptable_range=acceptable_range))
            else:
                column_list.append(Column(name=column))
    return column_list


def percent_depth_columns(csv_file, columns_to_exclude, percent_range, depth_range):
    column_list = list()
    df = pd.read_csv(csv_file)
    column_headers = list(df.columns)
    for column in column_headers:
        if column not in columns_to_exclude:
            column_list.append(Column(name=column,
                                      column_type='Percent_Depth',
                                      percent_range=percent_range,
                                      depth_range=depth_range))
    return column_list


class Column(object):

    def __init__(self, name, column_type='Categorical', acceptable_range=None, percent_range=None, depth_range=None):
        self.name = name
        self.column_type = column_type
        self.acceptable_range = acceptable_range
        self.percent_range = percent_range
        self.depth_range = depth_range


class Validator(object):
    def __init__(self, reference_csv, test_csv, column_list, identifying_column):
        self.identifying_column = identifying_column
        self.reference_csv_df = pd.read_csv(reference_csv)
        self.test_csv_df = pd.read_csv(test_csv)
        self.column_list = column_list
        self.reference_headers = list(self.reference_csv_df.columns)
        self.test_headers = list(self.test_csv_df.columns)

    def same_columns_in_ref_and_test(self):
        if set(self.reference_headers) != set(self.test_headers):
            return False
        else:
            return True

    def all_test_columns_in_ref_and_test(self):
        all_columns_present = True
        for column in self.column_list:
            if column.name not in self.reference_headers:
                logging.warning('{} was not found in Reference CSV.'.format(column.name))
                all_columns_present = False
            if column.name not in self.test_headers:
                logging.warning('{} was not found in Test CSV.'.format(column.name))
                all_columns_present = False
        return all_columns_present

    def check_samples_present(self):
        samples_in_ref = set(self.reference_csv_df[self.identifying_column])
        samples_in_test = set(self.test_csv_df[self.identifying_column])
        if samples_in_ref != samples_in_test:
            logging.warning('Not all samples in Test set are found in Reference set.')
            logging.warning('Samples in Test but not Reference: {}'.format(samples_in_test.difference(samples_in_ref)))
            logging.warning('Samples in Reference but not Test: {}'.format(samples_in_ref.difference(samples_in_test)))
            return False
        else:
            return True

    def check_columns_match(self):
        columns_match = True
        for testindex, testrow in self.test_csv_df.iterrows():
            for refindex, refrow in self.reference_csv_df.iterrows():
                if testrow[self.identifying_column] == refrow[self.identifying_column]:
                    for column in self.column_list:
                        if pd.isna(testrow[column.name]) and pd.isna(refrow[column.name]):
                            pass  # Equality doesn't work for na values in pandas, so have to check this first.
                        elif column.column_type == 'Categorical':
                            if testrow[column.name] != refrow[column.name]:
                                logging.warning('Attribute {} does not match for sample {}'.format(column.name,
                                                                                                   testrow[self.identifying_column]))
                                columns_match = False
                        elif column.column_type == 'Range':
                            lower_bound = float(refrow[column.name]) - column.acceptable_range
                            upper_bound = float(refrow[column.name]) + column.acceptable_range
                            if not lower_bound <= float(testrow[column.name]) <= upper_bound:
                                logging.warning('Attribute {} is out of range for sample {}'.format(column.name,
                                                                                                    testrow[self.identifying_column]))
                                columns_match = False

                        elif column.column_type == 'Percent_Depth':
                            test_percent = float(testrow[column.name].split()[0].replace('%', ''))
                            test_depth = float(testrow[column.name].split()[1].replace('(', ''))
                            ref_percent = float(refrow[column.name].split()[0].replace('%', ''))
                            ref_depth = float(refrow[column.name].split()[1].replace('(', ''))
                            upper_percent_bound = ref_percent + column.percent_range
                            lower_percent_bound = ref_percent - column.percent_range
                            upper_depth_bound = ref_depth + column.depth_range
                            lower_depth_bound = ref_depth - column.depth_range
                            if not lower_depth_bound <= test_depth <= upper_depth_bound:
                                logging.warning('Depth is out of range for column {} for sample {}'.format(column.name,
                                                                                                           testrow[self.identifying_column]))
                                columns_match = False
                            if not lower_percent_bound <= test_percent <= upper_percent_bound:
                                logging.warning('Percent is out of range for column {} for sample {}'.format(column.name,
                                                                                                             testrow[self.identifying_column]))
                                columns_match = False
        return columns_match



