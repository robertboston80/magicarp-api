from magicarp import common

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
        schema = common.response.ResourceCreated('resource_created')

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
        schema = common.response.ResourceUpdated('resource_updated')

        schema.populate(payload)

        output = schema.as_dictionary()

        self.assertEqual(len(output.keys()), 2)
        self.assertEqual(output['message'], payload['message'])
        self.assertEqual(output['url'], payload['url'])

        payload = [
            'apple', 2, 'banana', 3, 'orange', 8,
        ]

        schema = common.response.ListResponse('list_response')

        schema.populate(payload)

        output = schema.as_dictionary()

        self.assertEqual(output[0], payload[0])
        self.assertEqual(output[1], payload[1])
        self.assertEqual(output[2], payload[2])
        self.assertEqual(output[3], payload[3])
        self.assertEqual(output[4], payload[4])
        self.assertEqual(output[5], payload[5])
