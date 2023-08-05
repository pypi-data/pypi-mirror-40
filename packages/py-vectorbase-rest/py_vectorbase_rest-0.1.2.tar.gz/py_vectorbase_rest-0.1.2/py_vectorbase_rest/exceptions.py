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

from py_vectorbase_rest.vectorbase_config import http_status_codes


class VectorBaseRestError(Exception):
    '''
        Generic error class, catch-all for most VectorBase issues.
        Special cases are handled by VectorBaseRateLimitError and VectorBaseServiceUnavailable.
    '''
    def __init__(self, msg, error_code=None, rate_reset=None, rate_limit=None, rate_remaining=None, retry_after=None):
        self.error_code = error_code

        if error_code is not None and error_code in http_status_codes:
            msg = 'VectorBase REST API returned a %s (%s): %s' % (error_code, http_status_codes[error_code][0], msg)

        super(VectorBaseRestError, self).__init__(msg)

    @property
    def msg(self):
        return self.args[0]


class VectorBaseRestRateLimitError(VectorBaseRestError):
    '''
        Raised when you've hit a rate limit.
        The amount of seconds to retry your request in will be appended to the message.
    '''
    def __init__(self, msg, error_code=None, rate_reset=None, rate_limit=None, rate_remaining=None, retry_after=None):
        if isinstance(retry_after, float):
            msg = '%s (Rate limit hit:  Retry after %d seconds)' % (msg, retry_after)

        VectorBaseRestError.__init__(self, msg, error_code=error_code)


class VectorBaseRestServiceUnavailable(VectorBaseRestError):
    '''
        Raised when the service is down.
    '''
    pass
