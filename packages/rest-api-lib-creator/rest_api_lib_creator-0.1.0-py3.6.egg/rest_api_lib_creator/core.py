from io import IOBase

from requests.exceptions import HTTPError

from .utils import should_iterate
from .mixins import ListMixin, CreateMixin, RetrieveMixin, UpdateMixin, DeleteMixin


class RestApiLib(object):
    # CLASS VARIABLES

    base_api_url = None  # 'https://my.super.service/api/users'...
    nested_objects = None
    identifier_field = 'id'  # 'id', 'pk', 'uuid'...
    pretty_identifier = '{id}'  # '{id}', '{first_name} {last_name}', 'message from {source} to {target}'...
    requests_payload_mode = 'data'  # 'data' or 'json'
    list_url = None  # defaults to base_api_url
    instance_url = '{base_api_url}/{identifier}'
    request_headers = None  # defaults to {}
    request_timeout = None
    request_auth = None
    use_str_in_place_of_repr = False  # if True __repr__ will use __str__ to render output (which sometimes is handy for debugging)

    # CLASS METHODS

    @classmethod
    def list(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def retrieve(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def update(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def delete(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def get_base_api_url(cls):
        return cls.base_api_url

    @classmethod
    def get_list_url(cls):
        if cls.list_url:
            return cls.list_url
        return cls.get_base_api_url()

    @classmethod
    def get_instance_url(cls, identifier):
        return cls.instance_url.format(base_api_url=cls.base_api_url, identifier=identifier)

    @classmethod
    def get_request_headers(cls):
        return cls.request_headers or {}

    @classmethod
    def get_request_timeout(cls):
        return cls.request_timeout

    @classmethod
    def get_request_auth(cls):
        return cls.request_auth

    @classmethod
    def handle_request_exception(cls, e, method, url, request_kwargs):
        response = getattr(e, 'response', None)
        if isinstance(e, HTTPError) and (response is not None):
            raise HTTPError(response.content)

        raise e

    @classmethod
    def prepare_requests_call(cls, **kwargs):
        request_kwargs = kwargs.pop('_request_kwargs', {})
        files = request_kwargs.pop('request_files', {})

        if cls.requests_payload_mode in kwargs:
            # Move files from 'json/data' atribute to 'files' attribute
            for k, v in kwargs[cls.requests_payload_mode].items():
                if isinstance(v, IOBase):
                    files[k] = v
            for k in files:
                kwargs[cls.requests_payload_mode].pop(k)

            # Look for rich objects in data and replace them for the identifier.
            for k, v in kwargs[cls.requests_payload_mode].items():
                if isinstance(v, RestApiLib):
                    kwargs[cls.requests_payload_mode][k] = v.get_identifier()

        retval = {
            'timeout': request_kwargs.pop('request_timeout', cls.get_request_timeout()),
            'headers': request_kwargs.pop('request_headers', cls.get_request_headers()),
            'auth': request_kwargs.pop('request_auth', cls.get_request_auth()),
            'files': files,
        }
        retval.update(kwargs)
        return retval

    @classmethod
    def request(cls, method, url, **kwargs):
        kwargs = cls.prepare_requests_call(**kwargs)

        try:
            response = method(url, **kwargs)
            response.raise_for_status()
            return response
        except Exception as e:
            return cls.handle_request_exception(e, method, url, request_kwargs=kwargs)

    @classmethod
    def init_existing_object(cls, **kwargs):
        return cls(_existing_instance=True, **kwargs)

    @classmethod
    def call_endpoint(cls, method, url, **outer_kwargs):
        response_object = outer_kwargs.pop('response_object', None)

        response = cls.request(method, url, **outer_kwargs)
        if response_object:
            return response_object.init_existing_object(**response.json())
        return response

    # MAGIC METHODS

    def __init__(self, **kwargs):
        self._track_object_changes = False
        self._existing_instance = kwargs.pop('_existing_instance', False)
        self._nested_objects = self.nested_objects or {}
        self._instance_data = {}
        assert self.requests_payload_mode in ('data', 'json')

        for k, v in kwargs.items():
            if k in self._nested_objects:
                if should_iterate(v):
                    set_value = v.__class__([self._nested_objects[k](**v_child) for v_child in v])
                else:
                    set_value = self._nested_objects[k](**v)
            else:
                set_value = v

            setattr(self, k, set_value)
            self._instance_data[k] = set_value

        self._track_object_changes = True
        self._changed_data = {}

    def __setattr__(self, name, value):
        if not(name.startswith('_')) and self._track_object_changes:
            self._changed_data[name] = value
            self._instance_data[name] = value

        return super(RestApiLib, self).__setattr__(name, value)

    def __repr__(self):
        if self.use_str_in_place_of_repr:
            return self.__str__()
        return '<{}: {}>'.format(self.__class__.__name__, self.get_identifier())

    def __str__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.get_pretty_identifier())

    # REGULAR METHODS

    def get_identifier(self):
        return getattr(self, self.identifier_field)

    def get_pretty_identifier(self):
        return self.pretty_identifier.format(**self._instance_data)


class ViewsetRestApiLib(ListMixin, CreateMixin, RetrieveMixin, UpdateMixin, DeleteMixin, RestApiLib):
    pass
