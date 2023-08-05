import pytest

from pactum.fields import Field
from pactum.resources import ListResource, Resource


def test_basic_resource():
    resource = Resource(
        name="TestResource",
        fields=[],
        behaviors=[],
    )

    assert resource.name == "TestResource"
    assert len(resource.fields) == 0
    assert len(resource.behaviors) == 0


def test_basic_resource_class_definition():
    class TestResource(Resource):
        name = "TestResource"
        fields = []
        behaviors = []

    resource = TestResource()
    assert resource.name == "TestResource"
    assert len(resource.fields) == 0
    assert len(resource.behaviors) == 0


def test_basic_resource_class_definition_with_class_name():
    class MyResource(Resource):
        fields = []
        behaviors = []

    resource = MyResource()
    assert resource.name == "MyResource"
    assert len(resource.fields) == 0
    assert len(resource.behaviors) == 0


def test_access_fields_by_key():
    class MyResource(Resource):
        fields = [
            Field(name='my_field'),
            Field(name='my_other_field')
        ]

    resource = MyResource()

    assert isinstance(resource['my_field'], Field)
    assert isinstance(resource['my_other_field'], Field)

    assert resource['my_field'].name == 'my_field'
    assert resource['my_other_field'].name == 'my_other_field'

    assert resource.fields[0].parent == resource
    assert resource.fields[1].parent == resource


def test_duplicate_field_names_raises_error():
    class MyResource(Resource):
        fields = [
            Field(name='my_field'),
            Field(name='my_field')
        ]

    with pytest.raises(AttributeError):
        MyResource()


def test_subclassing_add_fields():
    class MyResource(Resource):
        fields = [
            Field(name='my_field'),
        ]

    class MySubResource(MyResource):
        fields = MyResource.fields + [
            Field(name='my_other_field')
        ]

    resource = MySubResource()

    assert isinstance(resource['my_field'], Field)
    assert resource['my_field'].name == 'my_field'

    assert isinstance(resource['my_other_field'], Field)
    assert resource['my_other_field'].name == 'my_other_field'


def test_basic_list_resource(resource):
    list_resource = ListResource(resource=resource)

    assert list_resource.name == "ListResource"
    assert list_resource.resource == resource

    assert hasattr(list_resource, 'fields') is False
    assert hasattr(list_resource, 'behaviors') is False


def test_basic_list_resource_class_definition(resource):
    base_resource = resource

    class MyListResource(ListResource):
        name = "ListResource"
        resource = base_resource

    list_resource = MyListResource()

    assert list_resource.name == "ListResource"
    assert list_resource.resource == resource

    assert hasattr(list_resource, 'fields') is False
    assert hasattr(list_resource, 'behaviors') is False


def test_fail_list_resource_with_no_resource():
    with pytest.raises(TypeError):
        ListResource(name="ListResource")
