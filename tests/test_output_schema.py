from magicarp import common
from magicarp.schema import output_field as field

from . import base


class TestOutputSchema(base.BaseTest):
    def test_common_output_schema(self):
        """Name: TestOutputSchema.test_common_output_schema
        """
        payload = {
            "message": 'Yolo archer',
            "uid": 1,
            "url": 'http://www.example.com',

        }
        schema = common.output_schema.ResourceCreated('resource_created')

        schema.populate(payload)

        output = schema.as_dictionary()

        self.assertEqual(len(output.keys()), 3)
        self.assertEqual(output['message'], payload['message'])
        self.assertEqual(output['uid'], str(payload['uid']))
        self.assertEqual(output['url'], payload['url'])

        payload = {
            "message": 'Yolo archer',
            "url": 'http://www.example.com',

        }
        schema = common.output_schema.ResourceUpdated('resource_updated')

        schema.populate(payload)

        output = schema.as_dictionary()

        self.assertEqual(len(output.keys()), 2)
        self.assertEqual(output['message'], payload['message'])
        self.assertEqual(output['url'], payload['url'])

        payload = [
            'apple', 2, 'banana', 3, 'orange', 8,
        ]

        schema = common.output_schema.ListResponse('list_response')

        schema.populate(payload)

        output = schema.as_dictionary()

        self.assertEqual(output[0], payload[0])
        self.assertEqual(output[1], str(payload[1]))
        self.assertEqual(output[2], payload[2])
        self.assertEqual(output[3], str(payload[3]))
        self.assertEqual(output[4], payload[4])
        self.assertEqual(output[5], str(payload[5]))

    def test_verify_collection_of_schema_work(self):
        """Name: TestOutputSchema.test_verify_collection_of_schema_work
        """
        class Invoice(field.SchemaField):
            fields = (
                field.IntegerField(
                    "uid", description="Unique order identifier"),
                field.IntegerField(
                    "customer_uid", description="Uid of customer"),
                field.CollectionField(
                    "products", field.IntegerField(
                        'individual_product',
                        description='Id of single product'),
                    description="List of product uids present on order"
                ),
                field.DateField("invoice_date"),
                field.DateField("creation_date"),
                field.StringField(
                    "url", description="Back reference to order"),
            )

        class ListOfInvoices(field.CollectionField):
            collection_type = Invoice

        payload = [{
            'uid': 1,
            'customer_uid': 1,
            'products': [
                1, 3, 5
            ],
            'invoice_date': '2018-01-02T13:00:00Z',
            'creation_date': '2018-01-01T13:00:00Z',
            'url': 'https://www.example.com/invoice/uid/1',
        }, {
            'uid': 2,
            'customer_uid': 53,
            'products': [
                5, 9, 12
            ],
            'invoice_date': '2018-03-02T13:00:00Z',
            'creation_date': '2018-03-01T13:00:00Z',
            'url': 'https://www.example.com/invoice/uid/1',
        }, {
            'uid': 3,
            'customer_uid': 1,
            'products': [
                3, 5, 9, 11
            ],
            'invoice_date': '2018-02-02T13:00:00Z',
            'creation_date': '2018-02-01T13:00:00Z',
            'url': 'https://www.example.com/invoice/uid/1',
        }]

        schema = ListOfInvoices('list_of_invoices')

        schema.populate(payload)

        output = schema.as_dictionary()

        self.assertEqual(output[0]['uid'], payload[0]['uid'])
        self.assertEqual(output[1]['uid'], payload[1]['uid'])
        self.assertEqual(output[2]['uid'], payload[2]['uid'])

        self.assertEqual(output[0]['invoice_date'].month, 1)
        self.assertEqual(output[1]['invoice_date'].month, 3)
        self.assertEqual(output[2]['invoice_date'].month, 2)

        self.assertEqual(output[0]['customer_uid'], payload[0]['customer_uid'])
        self.assertEqual(output[1]['customer_uid'], payload[1]['customer_uid'])
        self.assertEqual(output[2]['customer_uid'], payload[2]['customer_uid'])

    def test_verify_collections_work_multiple_way(self):
        """Name: TestOutputSchema.test_verify_collections_work_multiple_way

        We can specify collection as instance or class, both cases must work,
        but they have different description and names.
        """
        class BagOfPebbles1(field.SchemaField):
            fields = (
                field.CollectionField(
                    "pebbles", field.StringField(
                        'pebble', description='Individual pebble'),
                    description="All pebbles"
                ),
            )

        class BagOfPebbles2(field.SchemaField):
            fields = (
                field.CollectionField(
                    "pebbles", field.StringField,
                    description="All pebbles"
                ),
            )

        payload = {
            'pebbles': [
                'pink', 'yellow', 'grey', 'orange'
            ],
        }

        schema1 = BagOfPebbles1('bag_1')
        schema1.populate(payload)

        schema2 = BagOfPebbles2('bag_2')
        schema2.populate(payload)

        self.assertEqual(len(schema1.data['pebbles'].data), 4)
        self.assertEqual(len(schema2.data['pebbles'].data), 4)

        self.assertEqual(schema1.data['pebbles'].data[0].name, 'pebble')
        self.assertEqual(
            schema2.data['pebbles'].data[0].name, 'pebbles - instance - 0')

        self.assertEqual(
            schema1.data['pebbles'].data[0].description, 'Individual pebble')
        self.assertEqual(
            schema2.data['pebbles'].data[0].description,
            'All pebbles - instance - 0')

    def test_verify_schema_of_schema_works(self):
        """Name: TestOutputSchema.test_verify_schema_of_schema_works
        """
        class Player(field.SchemaField):
            fields = (
                field.IntegerField("starting_position"),
                field.StringField("nickname"),
            )

        class Match(field.SchemaField):
            fields = (
                Player('blue', description='Blue side player'),
                Player('red', description='Red side player'),
            )

        class ListOfMatches(field.CollectionField):
            collection_type = Match

        payload = [{
            'blue': {
                'starting_position': 3,
                'nickname': 'Dynamite',
            },
            'red': {
                'starting_position': 12,
                'nickname': 'Lord of the Flies',
            },
        }, {
            'blue': {
                'starting_position': 7,
                'nickname': 'Zigfried',
            },
            'red': {
                'starting_position': 9,
                'nickname': 'Hulk',
            },
        }]

        schema = ListOfMatches('agenda_for_today')

        schema.populate(payload)

        output = schema.as_dictionary()

        self.assertEqual(
            output[0]['blue']['nickname'],
            payload[0]['blue']['nickname'])
        self.assertEqual(
            output[0]['blue']['starting_position'],
            payload[0]['blue']['starting_position'])
        self.assertEqual(
            output[0]['red']['nickname'],
            payload[0]['red']['nickname'])
        self.assertEqual(
            output[0]['red']['starting_position'],
            payload[0]['red']['starting_position'])

        self.assertEqual(
            output[1]['blue']['nickname'],
            payload[1]['blue']['nickname'])
        self.assertEqual(
            output[1]['blue']['starting_position'],
            payload[1]['blue']['starting_position'])
        self.assertEqual(
            output[1]['red']['nickname'],
            payload[1]['red']['nickname'])
        self.assertEqual(
            output[1]['red']['starting_position'],
            payload[1]['red']['starting_position'])
