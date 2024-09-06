import unittest
from unittest import TestCase, mock
from unittest.mock import patch

from dog_school.main import CatchStick, Dog, DogSchool, FakeDead, get_next_pk, success_or_fail


class TestTricks(TestCase):
    def setUp(self):
        self.mock_output = mock.Mock(spec=print)
        self.dog = Dog("Rex", 4, self.mock_output)

    def test_talk(self):
        self.dog.talk()
        self.mock_output.assert_called_once_with("woof woof")

    @patch("dog_school.main.success_or_fail")
    def test_perform_existing_trick(self, mock_success_or_fail):
        mock_success_or_fail.return_value = True
        self.dog.perform_trick("talk")
        self.mock_output.assert_called_once_with("woof woof")

        self.mock_output.reset_mock()

        mock_success_or_fail.return_value = False
        self.dog.perform_trick("talk")
        self.mock_output.assert_called_once_with(f"{self.dog} knows how to talk, I swear.  We should try again!")
        
    def test_perform_not_existing_trick(self):
        self.dog.perform_trick("fake_dead")
        self.mock_output.assert_called_once_with(
            f"{self.dog} doesn't know how to fake_dead"
        )

    @patch("dog_school.main.success_or_fail")
    def test_learn_trick(self, mock_success_or_fail):
        self.dog.learn_trick(FakeDead)
        mock_success_or_fail.return_value = True
        self.dog.perform_trick(FakeDead.name)
        self.mock_output.assert_called_once_with(f"look, {self.dog} is dead")

    def test_dog_school__teaches(self):
        dog_school = DogSchool(tricks=[FakeDead, CatchStick])
        dog_school.teach(self.dog)
        self.assertEqual(self.dog.obedience_level, 5)

        self.dog.perform_trick(FakeDead.name)
        self.mock_output.assert_called_once_with(f"look, {self.dog} is dead")

        self.mock_output.reset_mock()

        self.dog.perform_trick(CatchStick.name, stick="a beautiful stick")
        self.mock_output.assert_called_once_with(
            f"look, {self.dog} caught a beautiful stick"
        )


    def test_get_student_by_number(self):
        dog_school = DogSchool(tricks=[])
        dog_school.teach(self.dog)

        self.assertEqual(dog_school.students, {1: self.dog})
        self.assertEqual(dog_school.get_student_by_number(1), self.dog)
        with self.assertRaises(ValueError):
            dog_school.get_student_by_number(999)

    def test_next_pk(self):
        pk = get_next_pk({99: mock.Mock(), 1: mock.Mock(), -5: mock.Mock()})
        self.assertEqual(100, pk)
    
    @patch("random.random") 
    def test_success_or_fail(self, mock_random):
        mock_random.return_value = 0.3
        self.assertTrue(success_or_fail(5))
        self.assertFalse(success_or_fail(1))
    
if __name__ == "__main__":
    unittest.main()