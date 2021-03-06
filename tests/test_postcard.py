import unittest
import lob

class PostcardFunctions(unittest.TestCase):
    def setUp(self):
        lob.api_key = 'test_fc26575412e92e22a926bc96c857f375f8b'
        self.addr = lob.Address.list(limit=1).data[0]

    def test_list_postcards(self):
        postcards = lob.Postcard.list()
        self.assertTrue(isinstance(postcards.data[0], lob.Postcard))
        self.assertEqual(postcards.object, 'list')

    def test_list_postcards_limit(self):
        postcards = lob.Postcard.list(limit=2)
        self.assertTrue(isinstance(postcards.data[0], lob.Postcard))
        self.assertEqual(len(postcards.data), 2)

    def test_list_postcards_metadata(self):
        postcards = lob.Postcard.list(metadata={ 'campagin': 'LOB2015' })
        self.assertTrue(isinstance(postcards.data[0], lob.Postcard))
        self.assertEqual(len(postcards.data), 1)

    def test_list_postcards_fail(self):
        self.assertRaises(lob.error.InvalidRequestError, lob.Postcard.list, limit=1000)

    def test_create_postcard(self):
        postcard = lob.Postcard.create(
            to_address = self.addr.id,
            from_address = self.addr.id,
            front = '<h1>{{front_name}}</h1>',
            back = '<h1>{{back_name}}</h1>',
            data = {
                'front_name': 'Peter',
                'back_name': 'Otto'
            }
        )
        self.assertEqual(postcard.to_address.id, self.addr.id)
        self.assertEqual(postcard.from_address.id, self.addr.id)
        self.assertTrue(isinstance(postcard, lob.Postcard))


    def test_create_postcard_lob_obj(self):
        postcard = lob.Postcard.create(
            to_address = self.addr,
            from_address = self.addr,
            front = '<h1>{{front_name}}</h1>',
            back = '<h1>{{back_name}}</h1>',
            data = {
                'front_name': 'Peter',
                'back_name': 'Otto'
            }
        )
        self.assertEqual(postcard.to_address.id, self.addr.id)
        self.assertEqual(postcard.from_address.id, self.addr.id)
        self.assertTrue(isinstance(postcard, lob.Postcard))

    def test_create_postcard_inline(self):
        postcard = lob.Postcard.create(
            to_address = {
                'name': 'Lob1',
                'address_line1': '185 Berry Street',
                'address_line2': 'Suite 1510',
                'address_city': 'San Francisco',
                'address_zip': '94107',
                'address_state': 'CA'
            },
            from_address = {
                'name': 'Lob2',
                'address_line1': '185 Berry Street',
                'address_line2': 'Suite 1510',
                'address_city': 'San Francisco',
                'address_zip': '94107',
                'address_state': 'CA'
            },
            front = '<h1>{{front_name}}</h1>',
            data = {
                'front_name': 'Peter'
            },
            message = 'Hello'
        )
        self.assertEqual(postcard.to_address.name, 'Lob1')
        self.assertEqual(postcard.from_address.name, 'Lob2')
        self.assertTrue(isinstance(postcard, lob.Postcard))

    def test_create_postcard_local_file(self):
        postcard = lob.Postcard.create(
            to_address = self.addr.id,
            from_address = self.addr.id,
            front = open('tests/pc.pdf', 'rb'),
            back = open('tests/pc.pdf', 'rb')
        )
        self.assertTrue(isinstance(postcard, lob.Postcard))

    def test_create_postcard_fail(self):
        self.assertRaises(lob.error.InvalidRequestError, lob.Postcard.create)

    def test_retrieve_postcard(self):
        postcard = lob.Postcard.retrieve(id=lob.Postcard.list().data[0].id)
        self.assertTrue(isinstance(postcard, lob.Postcard))

    def test_retrieve_postcard_fail(self):
        self.assertRaises(lob.error.InvalidRequestError, lob.Postcard.retrieve, id='test')
