import requests

from .utils import add_querystring_to_url


class ListMixin(object):
    @classmethod
    def get_objects_from_payload(cls, payload):
        return payload['results']  # DRF default

    @classmethod
    def get_list_url_(cls):
        return cls.get_list_url()

    @classmethod
    def list(cls, **kwargs):
        url = add_querystring_to_url(cls.get_list_url_(), **kwargs)
        objects = cls.get_objects_from_payload(cls.request(requests.get, url).json())
        return [cls.init_existing_object(**obj) for obj in objects]


class CreateMixin(object):
    @classmethod
    def get_create_url(cls):
        return cls.get_list_url()

    @classmethod
    def create(cls, **kwargs):
        outer_kwargs = {cls.requests_payload_mode: kwargs}
        response = cls.request(requests.post, cls.get_create_url(), **outer_kwargs)
        return cls.init_existing_object(**response.json())


class RetrieveMixin(object):
    @classmethod
    def get_retrieve_url(cls, identifier):
        return cls.get_instance_url(identifier)

    @classmethod
    def retrieve(cls, identfier):
        response = cls.request(requests.get, cls.get_retrieve_url(identfier))
        return cls.init_existing_object(**response.json())


class UpdateMixin(object):
    @classmethod
    def get_update_url(cls, identifier):
        return cls.get_instance_url(identifier)

    @classmethod
    def update(cls, identfier, **kwargs):
        outer_kwargs = {cls.requests_payload_mode: kwargs}
        response = cls.request(requests.patch, cls.get_retrieve_url(identfier), **outer_kwargs)
        return cls.init_existing_object(**response.json())

    def save(self):
        if not(self._existing_instance):
            return self.create(**self._changed_data)
        return self.update(self.get_identifier(), **self._changed_data)


class DeleteMixin(object):
    @classmethod
    def get_delete_url(cls, identifier):
        return cls.get_instance_url(identifier)

    @classmethod
    def delete(cls, identfier):
        cls.request(requests.delete, cls.get_retrieve_url(identfier))

    def destroy(self):
        return self.delete(self.get_identifier())
