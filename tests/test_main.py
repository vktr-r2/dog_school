from unittest import TestCase, mock

from dog_school.main import CatchStick, Dog, DogSchool, FakeDead


class TestTricks(TestCase):
    def setUp(self):
        self.mock_output = mock.Mock(spec=print)
        self.dog = Dog("Rex", self.mock_output)

    def test_talk(self):
        self.dog.talk()
        self.mock_output.assert_called_once_with("woof woof")

    def test_perform_existing_trick(self):
        self.dog.perform_trick("talk")
        self.mock_output.assert_called_once_with("woof woof")

    def test_perform_not_existing_trick(self):
        self.dog.perform_trick("fake_dead")
        self.mock_output.assert_called_once_with(
            f"{self.dog} don't know how to fake_dead"
        )

    def test_learn_trick(self):
        self.dog.learn_trick(FakeDead)
        self.dog.perform_trick(FakeDead.name)
        self.mock_output.assert_called_once_with(f"look, {self.dog} is dead")

    def test_dog_school__teaches(self):
        dog_school = DogSchool(tricks=[FakeDead, CatchStick])
        dog_school.teach(self.dog)

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
