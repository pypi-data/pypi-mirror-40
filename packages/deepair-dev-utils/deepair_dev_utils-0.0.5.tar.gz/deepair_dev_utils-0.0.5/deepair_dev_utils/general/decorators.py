# Copyright 2018 Deep Air. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""general decorators"""
from __future__ import print_function
from __future__ import absolute_import

import datetime
from colorama import *
from functools import wraps


def function_logger(orig_func):
    '''
        Create a file with function.log (if possible)
        otherwise with unknown_function.log and record
        the arguments passed for the function

        example:
        @function_logger
        def target_function(...):
            ...
    '''
    import logging

    # retrieving function name
    try:
        function_name = orig_func.__name__
    except:
        function_name = 'unknown_function'

    logging.basicConfig(filename='{}.log'.format(
        function_name), level=logging.INFO)

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        logging.info(
            'Ran with args: {}, and kwargs: {}'.format(args, kwargs))
        return orig_func(*args, **kwargs)

    return wrapper


def function_timer(orig_func):
    '''
        Displays runtime on console

        example:
        @function_timer
        def target_function(...):
            ...
    '''
    import time

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1

        # retrieving function name
        try:
            function_name = orig_func.__name__
        except:
            function_name = 'unknown function'

        # message styling
        log_time = Fore.RED + '[' + datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S') + ']: '+Fore.RESET
        msg = log_time + \
            '{0}{1}{2} exe time: {3}{4:>3.6f}{5} sec'

        # print message
        print(msg.format(Fore.CYAN, function_name, Fore.RESET,
                         Fore.BLUE, t2, Fore.RESET))

        return result

    return wrapper
