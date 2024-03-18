#!/usr/bin/env python


# Copyright 2021 Google Inc. All Rights Reserved.

#

# Licensed under the Apache License, Version 2.0 (the "License");

# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at

#

#      http://www.apache.org/licenses/LICENSE-2.0

#

# Unless required by applicable law or agreed to in writing, software

# distributed under the License is distributed on an "AS IS" BASIS,

# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

# See the License for the specific language governing permissions and

# limitations under the License.


"""Google Analytics Data API sample application demonstrating the creation

of a basic report.



See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport

for more information.

"""

# [START analyticsdata_run_report]

from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.data_v1beta import BetaAnalyticsDataClient

from google.analytics.data_v1beta.types import (

    DateRange,

    Dimension,

    Metric,

    MetricType,

    RunReportRequest,

)

import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'uplifted-env-417010-e25cb9245c6a.json'


def run_sample():
    """Runs the sample."""

    # TODO(developer): Replace this variable with your Google Analytics 4

    #  property ID before running the sample.

    property_id = "431492598"

    run_report(property_id)


def run_report(property_id="431492598"):
    """Runs a report of active users grouped by country."""

    client = BetaAnalyticsDataClient()

    request = RunReportRequest(

        property=f"properties/{property_id}",

        dimensions=[Dimension(name="country")],

        metrics=[Metric(name="totalUsers")],

        date_ranges=[DateRange(start_date="2020-09-01",
                               end_date="2024-09-15")],

    )

    response = client.run_report(request)

    print_run_report_response(response)


def get_all_properties(transport: str = None) -> None:
    """
    Prints summaries of all accounts accessible by the caller.

    Args:
        transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
    """
    client = AnalyticsAdminServiceClient(transport=transport)
    results = client.list_account_summaries()

    print("Result:")
    for account_summary in results:
        print("-- Account --")
        print(f"Resource name: {account_summary.name}")
        print(f"Account name: {account_summary.account}")
        print(f"Display name: {account_summary.display_name}")
        print()
        for property_summary in account_summary.property_summaries:
            print("-- Property --")
            print(f"Property resource name: {property_summary.property}")
            print(f"Property display name: {property_summary.display_name}")
            print()


def print_run_report_response(response):
    """Prints results of a runReport call."""

    # [START analyticsdata_print_run_report_response_header]

    print(f"{response.row_count} rows received")

    for dimensionHeader in response.dimension_headers:

        print(f"Dimension header name: {dimensionHeader.name}")

    for metricHeader in response.metric_headers:

        metric_type = MetricType(metricHeader.type_).name

        print(f"Metric header name: {metricHeader.name} ({metric_type})")

    # [END analyticsdata_print_run_report_response_header]

    # [START analyticsdata_print_run_report_response_rows]

    print("Report result:")

    for rowIdx, row in enumerate(response.rows):

        print(f"\nRow {rowIdx}")

        for i, dimension_value in enumerate(row.dimension_values):

            dimension_name = response.dimension_headers[i].name

            print(f"{dimension_name}: {dimension_value.value}")

        for i, metric_value in enumerate(row.metric_values):

            metric_name = response.metric_headers[i].name

            print(f"{metric_name}: {metric_value.value}")

    # [END analyticsdata_print_run_report_response_rows]


# [END analyticsdata_run_report]


if __name__ == "__main__":

    # run_sample()
    # Account is UA; Property is GA4
    get_all_properties()
