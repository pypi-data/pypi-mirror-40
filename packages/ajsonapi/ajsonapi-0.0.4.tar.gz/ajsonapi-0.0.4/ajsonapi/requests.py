# Copyright © 2018-2019 Roel van der Goot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Module requests deals with everything related to requests."""

from ajsonapi.document import parse as parse_document
from ajsonapi.exceptions import ErrorsException
from ajsonapi.headers import parse as parse_headers
from ajsonapi.query import parse as parse_query
from ajsonapi.uri.collection import parse_collection
from ajsonapi.uri.object import parse as parse_object
from ajsonapi.uri.relationship import parse as parse_relationship


def parse_collection_query(request):
    """Gets the resource collection and query parameters from the request."""

    parse_headers(request)
    errors = []
    try:
        collection = parse_collection(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    try:
        query = parse_query(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    if errors:
        raise ErrorsException(errors)
    return collection, query


async def parse_collection_document_query(request):
    """Gets the resource collection, the data member from the document, and
    query parameters from the request.
    """

    parse_headers(request)
    errors = []
    try:
        collection = parse_collection(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    try:
        data = await parse_document(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    try:
        query = parse_query(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    if errors:
        raise ErrorsException(errors)
    return collection, data, query


async def parse_object_query(request):
    """Gets the resource object and query parameters from the request."""

    parse_headers(request)
    errors = []
    try:
        object_ = parse_object(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    try:
        query = parse_query(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    if errors:
        raise ErrorsException(errors)
    return object_, query


async def parse_object_document_query(request):
    """Gets the resource object, the data member from the document, and query
    parameters from the request.
    """

    parse_headers(request)
    errors = []
    try:
        object_ = parse_object(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    try:
        data = await parse_document(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    try:
        query = parse_query(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    if errors:
        raise ErrorsException(errors)
    return object_, data, query


async def parse_relationship_query(request):
    """Gets the relationship and query parameters from the request."""

    parse_headers(request)
    errors = []
    try:
        relationship = parse_relationship(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    try:
        query = parse_query(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    if errors:
        raise ErrorsException(errors)
    return relationship, query


async def parse_relationship_document_query(request):
    """Gets the relationship and query parameters from the request."""

    parse_headers(request)
    errors = []
    try:
        relationship = parse_relationship(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    try:
        data = await parse_document(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    try:
        query = parse_query(request)
    except ErrorsException as err:
        errors.extend(err.errors)
    if errors:
        raise ErrorsException(errors)
    return relationship, data, query
