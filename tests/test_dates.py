import unittest
from unittest.mock import patch
from collections import namedtuple

from model.date import Date

TestDate = namedtuple('TestDate', ['id', 'display_date', 'date_range', 'date_type'])

class TestDates(unittest.TestCase):

    @patch('model.date.Date.lookupDate', return_value=None)
    @patch('model.date.Date.insert', return_value=True)
    def test_check_new(self, mock_insert, mock_lookup):
        res = Date.updateOrInsert('session', {'display_date': 'date'}, 'Date', 1)
        mock_lookup.expect_to_be_called()
        self.assertTrue(res)

    td = TestDate(
        id=1,
        display_date='test',
        date_range='[1,2)',
        date_type='tester'
    )
    @patch('model.date.Date.lookupDate', return_value=td)
    @patch('model.date.Date.update')
    def test_check_new(self, mock_update, mock_lookup):
        res = Date.updateOrInsert('session', {'display_date': 'date'}, 'Date', 1)
        mock_lookup.expect_to_be_called()
        mock_update.expect_to_be_called()
        self.assertEqual(res, None)


    @patch('model.date.Date.parseDate', return_value='[3,4)')
    def test_update_date(self, mock_parse):
        newTest = Date(
            id=1,
            display_date='test',
            date_range='[1,2)',
            date_type='tester'
        )
        newDate = {
            'display_date': 'new',
            'date_range': '[3,4)'
        }
        Date.update(newTest, newDate)
        self.assertEqual(newTest.display_date, 'new')
        self.assertEqual(newTest.date_range, '[3,4)')

    @patch('model.date.Date.parseDate', return_value='[3,4)')
    def test_insert_date(self, mock_parse):
        newDate = {
            'display_date': 'new',
            'date_range': '[3,4)',
            'date_type': 'tester'
        }
        res = Date.insert(newDate)
        self.assertEqual(res.display_date, 'new')
        self.assertEqual(res.date_range, '[3,4)')
        self.assertEqual(res.date_type, 'tester')

    def test_parse_single_date(self):
        res = Date.parseDate('2018-01-10')
        self.assertEqual(res, '[2018-01-10,)')

    def test_parse_date_list(self):
        res = Date.parseDate(['2018-01-10', '2018-01-11'])
        self.assertEqual(res, '[2018-01-10, 2018-01-11)')

    def test_parse_year(self):
        res = Date.parseDate('2018')
        self.assertEqual(res, '[2018-01-01, 2018-12-31)')

    def test_parse_month(self):
        res = Date.parseDate('2018-02')
        self.assertEqual(res, '[2018-02-01, 2018-02-28)')

    def test_parse_bad_date(self):
        res = Date.parseDate('Modnay, Dec 01, 87')
        self.assertEqual(res, None)