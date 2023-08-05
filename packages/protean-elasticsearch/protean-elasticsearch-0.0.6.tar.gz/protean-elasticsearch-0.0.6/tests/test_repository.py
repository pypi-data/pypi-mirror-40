"""Module to test Repository Classes and Functionality"""
import pytest
from protean.conf import active_config
from protean.core import field
from protean.core.entity import Entity
from protean.core.exceptions import ObjectNotFoundError
from protean.core.exceptions import ValidationError
from protean.core.repository import repo

from protean_elasticsearch.repository import ConnectionHandler
from protean_elasticsearch.repository import ElasticsearchSchema


class Dog(Entity):
    """This is a dummy Dog Entity class"""
    dog_id = field.Auto(identifier=True)
    name = field.String(required=True, max_length=50, unique=True)
    age = field.Integer(default=5)
    owner = field.String(required=True, max_length=15)

    def __repr__(self):
        return f'<Dog id={self.dog_id}>'


class DogSchema(ElasticsearchSchema):
    """ Schema for the Dog Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Dog
        schema_name = 'my-dogs'
        doc_type = 'dogs'


class TestConnectionHandler:
    """Class to test Connection Handler class"""

    @classmethod
    def setup_class(cls):
        """ Setup actions for this test case"""
        cls.repo_conf = active_config.REPOSITORIES['default']

    def test_init(self):
        """Test Initialization of Elasticsearch DB"""
        ch = ConnectionHandler(self.repo_conf)
        assert ch is not None

    def test_connection(self, mocker):
        """ Test the connection to the repository"""
        ch = ConnectionHandler(self.repo_conf)
        assert ch is not None

        # Mock the elasticsearch connector function
        mock_connector = mocker.patch(
            'elasticsearch_dsl.connections.connections.create_connection')
        conn = ch.get_connection()
        assert conn is not None

        mock_connector.assert_called_with(
            hosts=self.repo_conf['HOSTS'],
            http_auth=(self.repo_conf['USER'], self.repo_conf['SECRET'])
        )


class TestElasticsearchRepository:
    """Class to test Elasticsearch Repository"""

    @classmethod
    def setup_class(cls):
        """ Setup actions for this test case"""
        repo.register(DogSchema)

    @staticmethod
    def build_es_response(items, hit_only=False):
        """ Build a dummy elastic search response from the items"""
        es_response = {
            "hits": {
                "total": len(items),
                "max_score": 1,
                "hits": []
            }
        }
        for item in items:
            es_response['hits']['hits'].append({
                "_index": "my-dogs",
                "_type": "dogs",
                "_id": item['dog_id'],
                "_score": 1,
                "_source": item
            })
        if hit_only:
            return es_response['hits']['hits']
        else:
            return es_response

    def test_init(self):
        """Test ElasticsearchRepository Initialization"""
        pass

    def test_create(self, mocker):
        """ Test creating an entity in the repository"""
        # Patch the index function
        mock_index = mocker.patch(
            'elasticsearch.client.Elasticsearch.index')
        mock_index.return_value = {'_id': 'xx1xx'}

        mock_search = mocker.patch(
            'elasticsearch.client.Elasticsearch.search')
        mock_search.return_value = self.build_es_response([])

        # Create the entity and validate the results
        dog = repo.DogSchema.create(name='Johnny', owner='John')
        assert dog is not None
        assert dog.dog_id == 'xx1xx'

        mock_index.assert_called_with(
            body={'age': 5, 'dog_id': None, 'name': 'Johnny', 'owner': 'John'},
            index='my-dogs',
            doc_type='dogs'
        )
        mock_search.assert_called_with(
            body={'query': {'bool': {'filter': [{'match': {'name': 'Johnny'}}]}},
                  'from': 0, 'size': 1},
            doc_type=['dogs'],
            index=['my-dogs'])

    def test_create_duplicate(self, mocker):
        """ Test creating a duplicate entity in the repository"""
        # Mock the search and index functions
        mock_search = mocker.patch(
            'elasticsearch.client.Elasticsearch.search')
        mock_search.return_value = self.build_es_response([
            {'age': 5, 'dog_id': 1, 'name': 'Johnny', 'owner': 'John'}
        ])

        # Create the entity and validate the results
        with pytest.raises(ValidationError) as e_info:
            repo.DogSchema.create(dog_id=1, name='Johnny', owner='John')
        assert e_info.value.normalized_messages == {
            'dog_id': ['`my-dogs` with this `dog_id` already exists.']}

        # Create the dog now
        mock_search.return_value = self.build_es_response([])
        # Patch the index function
        mock_index = mocker.patch(
            'elasticsearch.client.Elasticsearch.index')
        mock_index.return_value = {'_id': 'xx1xx'}

        dog = repo.DogSchema.create(dog_id=1, name='Johnny', owner='John')
        assert dog is not None
        assert dog.dog_id == 1
        mock_index.assert_called_with(
            body={'age': 5, 'dog_id': 1, 'name': 'Johnny', 'owner': 'John'},
            index='my-dogs',
            doc_type='dogs',
            id=1
        )

    def test_update(self, mocker):
        """ Test updating an entity in the repository"""
        # Mock the search and index functions
        def search_side_effect(*args, **kwargs):
            if {'match': {'name': 'Johnny'}} in \
                    kwargs['body']['query']['bool']['filter']:
                return TestElasticsearchRepository.build_es_response([])
            else:
                return TestElasticsearchRepository.build_es_response([
                    {'age': 5, 'dog_id': 'xx1xx', 'name': 'Johnny', 'owner': 'John'}
                ])
        mock_search = mocker.patch(
            'elasticsearch.client.Elasticsearch.search')
        mock_search.side_effect = search_side_effect

        # Mock the index function
        mock_index = mocker.patch(
            'elasticsearch.client.Elasticsearch.index')
        mock_index.return_value = {'_id': 'xx1xx'}

        # Update the entity and validate the results
        dog = repo.DogSchema.update(identifier='xx1xx', data=dict(owner='Mary'))
        assert dog is not None
        assert dog.owner == 'Mary'

        # Make sure that the correct calls were made
        mock_index.assert_called_with(
            body={'age': 5, 'dog_id': 'xx1xx', 'name': 'Johnny',
                  'owner': 'Mary'},
            index='my-dogs',
            doc_type='dogs',
            id='xx1xx'
        )
        mock_search.assert_any_call(
            body={'query': {'bool': {'filter': [{'match': {'_id': 'xx1xx'}}]}},
                  'from': 0, 'size': 1},
            doc_type=['dogs'],
            index=['my-dogs']
        )

        # Test again for non exist item update
        mock_search.side_effect = None
        mock_search.return_value = self.build_es_response([])
        with pytest.raises(ObjectNotFoundError):
            repo.DogSchema.update(identifier='xx1xx', data=dict(owner='Mary'))

    def test_filter(self, mocker):
        """ Test reading entities from the repository"""
        # Mock the search functions
        mock_search = mocker.patch(
            'elasticsearch.client.Elasticsearch.search')
        mock_search.return_value = self.build_es_response([
            {'age': 5, 'dog_id': 1, 'name': 'Johnny', 'owner': 'John'},
            {'age': 4, 'dog_id': 2, 'name': 'Boxy', 'owner': 'John'},
            {'age': 2, 'dog_id': 3, 'name': 'Gooey', 'owner': 'John'},
        ])

        # Filter the entity and validate the results
        dogs = repo.DogSchema.filter(page=2, per_page=15, order_by='-age',
                                     excludes_={'name': 'Boxy'},
                                     owner='John')
        assert dogs is not None
        assert dogs.total == 3
        mock_search.assert_called_with(
            body={
                'query': {'bool': {'filter': [
                    {'match': {'owner': 'John'}},
                    {'bool': {'must_not': [{'terms': {'name': ['Boxy']}}]}}
                ]}},
                'sort': [{'age': {'order': 'desc'}}],
                'from': 15,
                'size': 15,
            },
            doc_type=['dogs'],
            index=['my-dogs']
        )

    def test_filter_all(self, mocker):
        """ Test reading all entities from the repository"""
        # Mock the search functions
        mock_scan = mocker.patch(
            'elasticsearch_dsl.search.scan')
        mock_scan.return_value = self.build_es_response([
            {'age': 5, 'dog_id': 1, 'name': 'Johnny', 'owner': 'John'},
            {'age': 4, 'dog_id': 2, 'name': 'Boxy', 'owner': 'John'},
            {'age': 2, 'dog_id': 3, 'name': 'Gooey', 'owner': 'John'},
        ], hit_only=True)

        # Filter the entity and validate the results
        dogs = repo.DogSchema.filter(page=2, per_page=None,
                                     excludes_={'name': 'Boxy'},
                                     owner='John')
        assert dogs is not None
        assert dogs.total == 3
        mock_scan.assert_called_with(
            repo.DogSchema.conn,
            query={
                'query': {'bool': {'filter': [
                    {'match': {'owner': 'John'}},
                    {'bool': {'must_not': [{'terms': {'name': ['Boxy']}}]}}
                ]}}
            },
            doc_type=['dogs'],
            index=['my-dogs']
        )

    def test_delete(self, mocker):
        """ Test deleting an entity from the repository"""
        # Mock the search functions
        mock_delete = mocker.patch(
            'elasticsearch.client.Elasticsearch.delete_by_query')
        mock_delete.return_value = {'total': 1}

        # Filter the entity and validate the results
        cnt = repo.DogSchema.delete(1)
        assert cnt == 1
        mock_delete.assert_called_with(
            body={'query': {'bool': {'filter': [{'match': {'_id': 1}}]}}},
            doc_type=['dogs'],
            index=['my-dogs']
        )

        # Set a non Auto id field and test
        DogSchema.opts_.entity_cls.id_field = \
            'dog_id', field.Integer(identifier=True)
        cnt = repo.DogSchema.delete(1)
        assert cnt == 1
