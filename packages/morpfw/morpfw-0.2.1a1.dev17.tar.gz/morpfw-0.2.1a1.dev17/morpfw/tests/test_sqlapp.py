import morpfw
from morpfw import sql as morpsql
from morpfw.crud.schema import Schema
import sqlalchemy as sa
import jsl
from .common import get_client
import jsonobject


class App(morpfw.SQLApp):
    pass


class Page(morpsql.Base):
    __tablename__ = 'test_page'

    title = sa.Column(sa.String(length=1024))
    body = sa.Column(sa.Text)


class PageSchema(Schema):
    title = jsonobject.StringProperty()
    body = jsonobject.StringProperty()


@App.identifierfields(schema=PageSchema)
def page_schema_identifier(schema):
    return ['uuid']


class PageCollection(morpfw.Collection):
    schema = PageSchema


class PageModel(morpfw.Model):
    schema = PageSchema


class PageStorage(morpfw.SQLStorage):
    model = PageModel
    orm_model = Page


@App.path(model=PageCollection, path='/')
def get_pagecollection(request):
    storage = PageStorage(request)
    return PageCollection(request, storage)


@App.path(model=PageModel, path='/{identifier}')
def get_page(request, identifier):
    storage = PageStorage(request)
    return storage.get(identifier)


def test_morp_framework(pgsql_db):
    c = get_client(App)

    r = c.get('/')

    assert len(r.json['schema']['properties']) == 11

    r = c.post_json(
        '/', {'title': 'Hello world', 'body': 'Lorem ipsum'})

    assert r.json['links'][0]['href'].startswith('http://localhost/')
    assert r.json['data']['title'] == 'Hello world'
    assert r.json['data']['body'] == 'Lorem ipsum'

    page_url = r.json['links'][0]['href']
    r = c.get(page_url)

    assert r.json['data']['title'] == 'Hello world'

    delete_link = r.json['links'][2]
    assert delete_link['method'] == 'DELETE'

    r = c.delete(delete_link['href'])

    r = c.get(page_url, expect_errors=True)

    assert r.status_code == 404
