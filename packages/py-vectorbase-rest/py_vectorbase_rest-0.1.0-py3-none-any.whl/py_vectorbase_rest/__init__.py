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

from .vectorbase_rest import VectorBaseRest
from .exceptions import VectorBaseRestError, VectorBaseRestServiceUnavailable, VectorBaseRestRateLimitError
