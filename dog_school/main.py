from __future__ import annotations
from collections.abc import Callable
from typing import Any, Protocol


class Dog:
    def __init__(self, name: str, output_channel: Callable[[str], None | str] = print):
        self.name = name
        self.output_channel = output_channel
        self.tricks = {"talk": self.talk}

    def __str__(self):
        return f"<{self.name}, the dog>"

    def talk(self):
        self.output_channel("woof woof")

    def perform_trick(self, trick_name: str, **kwargs: Any):
        try:
            self.tricks[trick_name](**kwargs)
        except KeyError:
            self.output_channel(f"{self} don't know how to {trick_name}")

    def learn_trick(self, trick_class: Trick):
        trick = trick_class(self)
        self.tricks[trick.name] = trick


class DogSchool:
    trick_classes: list[Trick]
    students: dict[int, Dog]

    def __init__(self, tricks: list[Trick]):
        self.trick_classes = tricks
        self.students = {}

    def teach(self, dog: Dog) -> int:
        dog_number = self.__add_student(dog)
        for t in self.trick_classes:
            dog.learn_trick(t)
        return dog_number

    def __add_student(self, dog) -> int:
        number = max(self.students.keys(), default=1)
        self.students[number] = dog
        return number

    def get_student_by_number(self, number: int):
        try:
            return self.students[number]
        except KeyError:
            raise ValueError(f"There is no Dog with number {number}")


class FakeDead:
    name = "fake_dead"

    def __init__(self, dog: Dog):
        self.dog = dog

    def __call__(self, **_: Any) -> Any:
        self.dog.output_channel(f"look, {self.dog} is dead")


class CatchStick:
    name = "catch_stick"

    def __init__(self, dog: Dog):
        self.dog = dog

    def __call__(self, stick: str = "some stick", **_: Any) -> Any:
        self.dog.output_channel(f"look, {self.dog} caught {stick}")


class Trick(Protocol):
    name: str

    def __init__(self, dog: Dog): ...

    def __call__(self, **kwargs: Any) -> Any: ...


if __name__ == "__main__":
    dog = Dog("Fluffy")
    dog_school = DogSchool([FakeDead, CatchStick])

    enrolling_number = dog_school.teach(dog)

    for t in dog.tricks:
        dog.perform_trick(t)

    print(dog_school.get_student_by_number(enrolling_number))
