# core/middleware.py
"""
custom middleware that calculates and logs
the execution time of each request
"""

import time
import logging

from django.db import connection, reset_queries


def metric_middleware(get_response):
    def middleware(request):
        reset_queries()
        # get beginning statistics
        start_queries = len(connection.queries)
        start_time = time.perf_counter()
        # process the request
        response = get_response(request)
        # get ending statistics
        end_time = time.perf_counter()
        end_queries = len(connection.queries)
        # calculate_statistics
        total_time = end_time - start_time
        total_queries = end_queries - start_queries
        # log the statistics
        logger = logging.getLogger("debug")
        logger.debug(f"Request: {request.method} {request.path}")
        logger.debug(f"Number of queries: {total_queries}")
        logger.debug(f"Total time: {(total_time):.2f}s")
        return response
    return middleware
