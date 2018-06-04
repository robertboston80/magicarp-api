import datetime

from magicarp.schema import input_field

from . import base


class TestTimeNormalisation(base.BaseTest):
    def test_time_normlisation_case_1(self):
        """Name: TestTimeNormalisation.test_time_normlisation_case_1
        """
        field = input_field.TimeField('time1')

        field.populate('12:15:30')

        value = datetime.timedelta(hours=12, minutes=15, seconds=30)

        self.assertEqual(field.data.seconds, value.seconds)

    def test_time_normlisation_case_2(self):
        """Name: TestTimeNormalisation.test_time_normlisation_case_2
        """
        field = input_field.TimeField('time1')

        field.populate('12:12')

        value = datetime.timedelta(hours=12, minutes=12)

        self.assertEqual(field.data.seconds, value.seconds)

    def test_time_normlisation_case_3(self):
        """Name: TestTimeNormalisation.test_time_normlisation_case_3
        """
        field = input_field.TimeField('time1')

        field.populate('12:12')

        value = datetime.timedelta(hours=12, minutes=12)

        self.assertEqual(field.data.seconds, value.seconds)

    def test_time_normlisation_case_4(self):
        """Name: TestTimeNormalisation.test_time_normlisation_case_4
        """
        field = input_field.TimeField('time1')

        field.populate('12h 13m 14s 15ms')

        value = datetime.timedelta(
            hours=12, minutes=13, seconds=14, milliseconds=15)

        self.assertEqual(field.data.seconds, value.seconds)

    def test_time_normlisation_case_5(self):
        """Name: TestTimeNormalisation.test_time_normlisation_case_5
        """
        field = input_field.TimeField('time1')

        field.populate('12h13m14s15ms')

        value = datetime.timedelta(
            hours=12, minutes=13, seconds=14, milliseconds=15)

        self.assertEqual(field.data.seconds, value.seconds)

    def test_time_normlisation_case_6(self):
        """Name: TestTimeNormalisation.test_time_normlisation_case_6
        """
        field = input_field.TimeField('time1')

        field.populate('12h:15ms:13m:14s')

        value = datetime.timedelta(
            hours=12, minutes=13, seconds=14, milliseconds=15)

        self.assertEqual(field.data.seconds, value.seconds)
