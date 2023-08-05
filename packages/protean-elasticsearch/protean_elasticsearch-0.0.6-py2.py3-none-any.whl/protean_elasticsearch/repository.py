"""This module holds the definition of Database connectivity"""
import logging
from typing import Any

from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from protean.core.field import Auto
from protean.core.repository import BaseConnectionHandler
from protean.core.repository import BaseRepository
from protean.core.repository import BaseSchema
from protean.core.repository import Pagination
from protean.core.repository import SchemaOptions

logger = logging.getLogger('protean.elasticsearch')


class ConnectionHandler(BaseConnectionHandler):
    """Manage connections to the Elasticsearch Database"""

    def __init__(self, conn_info: dict):
        self.conn_info = conn_info

    def get_connection(self):
        """ Create the connection to the Elasticsearch instance"""
        connection = connections.create_connection(
            hosts=self.conn_info['HOSTS'],
            http_auth=(
                self.conn_info['USER'], self.conn_info['SECRET']))
        return connection


class ElasticsearchSchemaOpts(SchemaOptions):
    """ Options for the Elasticsearch repository schema"""
    def __init__(self, meta, schema_cls):
        super().__init__(meta, schema_cls)

        # Get the doc type for this schema
        self.doc_type = getattr(meta, 'doc_type', self.schema_name)


class ElasticsearchSchema(BaseSchema):
    """Schema representation for the Elasticsearch Database """
    options_cls = ElasticsearchSchemaOpts

    @classmethod
    def from_entity(cls, entity):
        """ Convert the entity to a dictionary record """
        entity_dict = {}
        for field_name in entity.meta_.declared_fields:
            entity_dict[field_name] = getattr(entity, field_name)
        return entity_dict

    @classmethod
    def to_entity(cls, item):
        """ Convert the dictionary record to an entity """
        item_dict = item.to_dict()
        id_field = cls.opts_.entity_cls.meta_.id_field
        if isinstance(id_field, Auto):
            item_dict[id_field.field_name] = item.meta.id
        return cls.opts_.entity_cls(item_dict)


class Repository(BaseRepository):
    """Repository implementation for the Elasticsearch Database"""

    def _create_object(self, schema_obj: Any):
        """ Create a new document in the elasticsearch index"""

        # Add the entity to the repository
        id_field = self.entity_cls.meta_.id_field
        identifier = schema_obj.get(id_field.field_name)
        if identifier:
            self.conn.index(
                index=self.schema_cls.opts_.schema_name,
                doc_type=self.schema_cls.opts_.doc_type,
                body=schema_obj,
                id=identifier
            )
        else:
            result = self.conn.index(
                index=self.schema_cls.opts_.schema_name,
                doc_type=self.schema_cls.opts_.doc_type,
                body=schema_obj.copy(),
            )
            schema_obj[id_field.field_name] = result['_id']
        return schema_obj

    def _filter_objects(self, page: int = 1, per_page: int = 10,
                        order_by: list = (), excludes_: dict = None,
                        **filters) -> Pagination:
        # Build the search query
        s = Search(index=self.schema_cls.opts_.schema_name,
                   doc_type=self.schema_cls.opts_.doc_type)

        # Add the filter and the exclude conditions
        id_field = self.entity_cls.meta_.id_field
        for fk, fv in filters.items():
            fk = '_id' if fk == id_field.field_name else fk
            s = s.filter('match', **{fk: fv})
        for ek, ev in excludes_.items():
            if ek == id_field.field_name:
                s = s.exclude('match', **{'_id': ev})
            else:
                if not isinstance(ev, (list, tuple)):
                    ev = [ev]
                s = s.exclude('terms', **{ek: ev})

        # Set the ordering for the results
        if order_by:
            s = s.sort(*order_by)

        # Set the limit and offset for paging
        scan = False
        if per_page is not None:
            offset = (page - 1) * per_page
            limit = page * per_page
            s = s[offset:limit]
        else:
            scan = True
        logger.debug(
            f'Filtering objects using dsl query {s.to_dict()}')

        # execute the query and build final result
        if scan:
            items = [item for item in s.scan()]
            result = Pagination(
                page=page,
                per_page=len(items),
                total=len(items),
                items=items
            )
        else:
            response = s.execute()
            result = Pagination(
                page=page,
                per_page=per_page,
                total=response.hits.total,
                items=response.hits)

        return result

    def _update_object(self, schema_obj: Any):
        """ Update an existing document in the elasticsearch index"""
        id_field = self.entity_cls.meta_.id_field
        identifier = schema_obj[id_field.field_name]
        self.conn.index(
            index=self.schema_cls.opts_.schema_name,
            doc_type=self.schema_cls.opts_.doc_type,
            body=schema_obj,
            id=identifier
        )
        return schema_obj

    def _delete_objects(self, **filters):
        """ Delete the dictionary object by its id"""

        # Delete the object and return the deletion count
        s = Search(index=self.schema_cls.opts_.schema_name,
                   doc_type=self.schema_cls.opts_.doc_type)

        # Run the filters and delete the items
        for fk, fv in filters.items():
            if fk == self.entity_cls.meta_.id_field.field_name:
                s = s.filter("match", **{'_id': fv})
            else:
                s = s.filter("match", **{fk: fv})
        response = s.delete()

        return response.total
