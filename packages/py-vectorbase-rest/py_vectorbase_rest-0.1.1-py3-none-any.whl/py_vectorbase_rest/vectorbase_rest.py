'''
    Copyright (C) 2018, Romain Feron
    Based on code from Steve Moss Copyright (C) 2013-2016, pyEnsemblRest
    py_vectorbase_rest is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    py_vectorbase_rest is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with py_vectorbase_rest.  If not, see <http://www.gnu.org/licenses/>.
    Configuration information for the EnsEMBL REST API
'''

import json
import re
import requests
import time
from collections import namedtuple
from py_vectorbase_rest.vectorbase_config import vectorbase_default_url
from py_vectorbase_rest.vectorbase_config import vectorbase_api_table
from py_vectorbase_rest.vectorbase_config import http_status_codes
from py_vectorbase_rest.vectorbase_config import vectorbase_header
from py_vectorbase_rest.vectorbase_config import vectorbase_content_type
from py_vectorbase_rest.vectorbase_config import vectorbase_user_agent
from py_vectorbase_rest.exceptions import VectorBaseRestError, VectorBaseRestRateLimitError, VectorBaseRestServiceUnavailable


class VectorBaseRest(object):

    def __init__(self, **kwargs):

        self.session_args = kwargs or {}

        # Rate limiting and checking parameters
        self.reqs_per_sec = 15
        self.req_count = 0
        self.last_req = 0
        self.wall_time = 1
        self.rate_reset = None
        self.rate_limit = None
        self.rate_remaining = None
        self.retry_after = None

        # Store last query parameters / results in case the query failed (for resubmission)
        self.last_url = None
        self.last_params = {}
        self.last_data = {}
        self.last_method = None
        self.last_attempt = 0
        self.last_response = None

        # Maximum number of attempts
        self.max_attempts = 5

        # Timeout value in seconds
        self.timeout = 60

        # Set default values if those values are not provided
        self.__set_default()

        # Setup requests session
        self.session = requests.Session()

        # Update headers
        self.__update_headers()

        # Automatically create class methods based on the api table
        self.__add_methods(vectorbase_api_table)

    def __set_default(self):
        '''
        Set default connection settings values
        '''
        default_base_url = vectorbase_default_url
        default_headers = vectorbase_header
        default_content_type = vectorbase_content_type
        default_proxies = {}

        if 'base_url' not in self.session_args:
            self.session_args['base_url'] = default_base_url
        if 'headers' not in self.session_args:
            self.session_args['headers'] = default_headers
        if 'User-Agent' not in self.session_args['headers']:
            self.session_args['headers'].update(default_headers)
        if 'Content-Type' not in self.session_args['headers']:
            self.session_args['headers']['Content-Type'] = default_content_type
        if 'proxies' not in self.session_args:
            self.session_args['proxies'] = default_proxies

    def __update_headers(self):
        '''Update reauest headers'''
        client_args_copy = self.session_args.copy()
        for key, val in client_args_copy.items():
            if key in ('base_url', 'proxies'):
                setattr(self.session, key, val)
                self.session_args.pop(key)
        self.session.headers.update(self.session_args.pop('headers'))

    def __add_methods(self, api_table):
        '''
        Iterate over api_table keys and add each key to class namespace
        '''
        for fun_name in api_table.keys():
            self.__dict__[fun_name] = self.register_api_func(fun_name, api_table)
            # Set __doc__ for generic class method
            if 'doc' in api_table[fun_name]:
                self.__dict__[fun_name].__doc__ = api_table[fun_name]['doc']
            # Add function name to the class methods
            self.__dict__[fun_name].__name__ = fun_name

    def register_api_func(self, api_call, api_table):
        '''
        Dynamic API function registration
        '''
        return lambda **kwargs: self.call_api_func(api_call, api_table, **kwargs)

    @staticmethod
    def __check_params(func, kwargs):
        '''
        Check API function parameters.
        Verify required parameters and raise an Exception if needed.
        '''
        mandatory_params = re.findall('\{\{(?P<m>[a-zA-Z1-9_]+)\}\}', func['url'])
        for param in mandatory_params:
            if param not in kwargs:
                raise Exception('mandatory param ''%s'' not specified' % param)
        return mandatory_params

    def call_api_func(self, api_call, api_table, **kwargs):
        '''
        Dynamic API call function
        '''
        func = api_table[api_call]  # build url from api_table kwargs
        mandatory_params = self.__check_params(func, kwargs)  # check mandatory params
        url = re.sub('\{\{(?P<m>[a-zA-Z1-9_]+)\}\}', lambda m: '%s' % kwargs.get(m.group(1)),
                     self.session.base_url + func['url'])  # resolving urls
        # Remove mandatory params from kwargs
        for param in mandatory_params:
            del(kwargs[param])

        content_type = func['content_type']  # Get content type from api table

        # Check the request type (GET or POST)
        if func['method'] == 'GET':
            # Record request parameters
            self.last_url = url
            self.last_headers = {"Content-Type": content_type}
            self.last_params = kwargs
            self.last_data = {}
            self.last_method = 'GET'
            self.last_attempt = 0
            response = self.__get_response()
        elif func['method'] == 'POST':
            # In a POST request, separate post parameters from other parameters
            data = {}
            # Pass key=value in POST data from kwargs
            for key in func['post_parameters']:
                if key in kwargs:
                    data[key] = kwargs[key]
                    del(kwargs[key])
            # Record request parameters
            self.last_url = url
            self.last_headers = {"Content-Type": content_type}
            self.last_params = kwargs
            self.last_data = data
            self.last_method = 'POST'
            self.last_attempt = 0
            response = self.__get_response()
        else:
            raise NotImplementedError('Method ''%s'' not yet implemented' % (func['method']))

        # Parse the response and returns the content
        return self.parse_response(response, content_type)

    def __get_response(self):
        '''
        Call session get and post method. Return response
        '''
        self.last_req = time.time()  # updating last_req time
        self.req_count += 1  # Increment the request counter to rate limit requests
        # Evaluate the numer of requests in a second
        if self.req_count >= self.reqs_per_sec:
            delta = time.time() - self.last_req
            # Sleep upto wall_time if there are too many requests
            if delta < self.wall_time:
                to_sleep = self.wall_time - delta
                time.sleep(to_sleep)
            self.req_count = 0

        response = None
        try:
            if self.last_method == 'GET':
                response = self.session.get(self.last_url,
                                            headers=self.last_headers,
                                            params=self.last_params,
                                            timeout=self.timeout)
            elif self.last_method == 'POST':
                response = self.session.post(self.last_url,
                                             headers=self.last_headers,
                                             data=json.dumps(self.last_data),
                                             params=self.last_params,
                                             timeout=self.timeout)
        except requests.ConnectionError as e:
            raise VectorBaseRestServiceUnavailable(e)
        except requests.Timeout as e:
            # Create a fake response in order to redo the query
            response = namedtuple('fakeResponse', ['headers', 'status_code', 'text'])
            # Add some data
            response.headers = {}
            response.status_code = 400
            response.text = json.dumps({'message': repr(e), 'error': '%s timeout' % vectorbase_user_agent})

        return response

    def parse_response(self, response, content_type='application/json'):
        '''Deal with a generic REST response'''
        self.last_response = response          # Record response for debug intent
        # initialize some values. Check if I'm rate limited
        self.rate_reset, self.rate_limit, self.rate_remaining, self.retry_after = self.__get_rate_limit(response.headers)
        # Parse status code
        if self.__check_retry(response):
            return self.__retry_request()
        if content_type == 'application/json':
            content = json.loads(response.text)
        else:
            content = response.text
        return content

    def __check_retry(self, response):
        '''Parse status code and print warnings. Return True if a retry is needed'''
        message = http_status_codes[response.status_code][1]  # default status code
        if response.status_code > 304:
            ExceptionType = VectorBaseRestError
            # Try to derive a more useful message than ensembl default message
            if response.status_code == 400:
                json_message = json.loads(response.text)
                if 'error' in json_message:
                    message = json_message['error']
            if response.status_code == 429:
                ExceptionType = VectorBaseRestRateLimitError
            raise ExceptionType(
                message,
                error_code=response.status_code,
                rate_reset=self.rate_reset,
                rate_limit=self.rate_limit,
                rate_remaining=self.rate_remaining,
                retry_after=self.retry_after)
        # Return a flag indicating whether the request was processed correctly
        return False

    @staticmethod
    def __get_rate_limit(headers):
        '''Read rate limited attributes'''
        retry_after = None
        rate_reset = None
        rate_limit = None
        rate_remaining = None

        keys = [key.lower() for key in headers.keys()]

        if 'X-RateLimit-Reset'.lower() in keys:
            rate_reset = int(headers['X-RateLimit-Reset'])
        if 'X-RateLimit-Limit'.lower() in keys:
            rate_limit = int(headers['X-RateLimit-Limit'])
        if 'X-RateLimit-Remaining'.lower() in keys:
            rate_remaining = int(headers['X-RateLimit-Remaining'])
        if 'Retry-After'.lower() in keys:
            retry_after = float(headers['Retry-After'])

        return rate_reset, rate_limit, rate_remaining, retry_after

    def __retry_request(self):
        '''Retry last request in case of failure'''
        self.last_attempt += 1
        if self.last_attempt > self.max_attempts:
            message = http_status_codes[self.last_response.status_code][1]  # Default status code
            # Parse error if possible
            json_message = json.loads(self.last_response.text)
            if 'error' in json_message:
                message = json_message['error']
            raise VectorBaseRestError('Max number of retries attempts reached. Last message was: %s'
                                   % message,
                                   error_code=self.last_response.status_code,
                                   rate_reset=self.rate_reset,
                                   rate_limit=self.rate_limit,
                                   rate_remaining=self.rate_remaining,
                                   retry_after=self.retry_after)

        # Sleep for a while. Increment on each attempt
        to_sleep = (self.wall_time + 1) * self.last_attempt
        time.sleep(to_sleep)

        if self.last_method == 'GET':
            response = self.__get_response()
        elif self.last_method == 'POST':
            response = self.__get_response()
        else:
            response = None

        return self.parse_response(response, self.last_headers['Content-Type'])
