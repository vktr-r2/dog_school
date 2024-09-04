from __future__ import annotations
from collections.abc import Callable
from typing import Any, Protocol


"""
Dog Class represents a dog that can perform tricks
Attributes
    name
    output_channel: Callable (like a function) that outputs a string.  Set to default to print function.
        - Callable represents and object that can be called like a function.  (built in function like print, user-defined function, lambda, or even instance of class that implements _call_)
        - You can call it just like a function.  It can accept args and return a value or perform an action based on those args.
        - output_channel is more of a "placeholder" or reference to any callable object.  Actual functions are specific fixed objects in Python, but Callable could point to any function or callable object
        - output_channel could be a method of a class, or instance of a callable class so it might have state.
        - USE CASE: Dependency injection - makes the Dog class more flexible and easier to test.  EX: Instead of print, in our tests we could inject a function that collects output messages to a list instead
        - USE CASE: Customize behaviour - if used in the UI, output_channel could update a test field instead of printing to console.
        - USE CASE: Logging - Allows you to easily integrate logging into your classes by passing a logging function/loggers info or error method
        - USE CASE: Multi-environ compatibility - Can use different Callables for dev, staging, prod
        - USE CASE: Asynch programming - output_channel could be asynchronous, allowing it to be non-blocking
Methods
    __init__: initializes dog w/ name, optional output channel (print is default), setuls default talk trick in dict that calls the talk method
    __str__: returns a string representation of the dog
    talk: method that makes the dog speak
    perform_trick: takes trick name and any additional args, finds corresponding trick in tricks dict and executes.  If the trick is not known, it outputs a message stating so
    learn_trick: Accepts a trick class, creates an instace of the trick associated with the dog, and adds it to the tricks dictionary
"""

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
            self.output_channel(f"{self} doesn't know how to {trick_name}")

    def learn_trick(self, trick_class: Trick):
        trick = trick_class(self)
        self.tricks[trick.name] = trick

"""
DogSchool class represents a schoole where dogs learn tricks
Attributes
    trick_classes: A list of classes that define tricks
    students: A dict mapping unique student number to Dog instance
Methods
    __init__: Initializes the schoold with a list of tricks provided, and setups empty dict for students
    teach: Takes Dog instance and teaches it all tricks in tick_classes list, then adds the dog to the school's students dict and returns unique student number
    __add_student: Private method that adds a dog to the students dictionary with a unique number
    get_student_by_number: Returns a Dog instance by its studnet number or raises error if number doesn't exist
"""

class DogSchool:
    trick_classes: list[Trick]
    students: dict[int, Dog]

    def __init__(self, tricks: list[Trick]):
        self.trick_classes = tricks
        self.students = {}

    def teach(self, dog: Dog) -> int:
        for t in self.trick_classes:
            dog.learn_trick(t)
        return self.__add_student(dog)

    def __add_student(self, dog) -> int:
        number = get_next_pk(self.students)
        self.students[number] = dog
        return number

    def get_student_by_number(self, number: int):
        try:
            return self.students[number]
        except KeyError:
            raise ValueError(f"There is no Dog with number {number}")

"""
FakeDead and CatchStick Classes represent specific tricks that a dog can learn
Attributes
    name
    dog: reference to the Dog instance performing the trick
Methods
    __init__: Initializes the trick with a reference to a Dog instance
    __call__: Executes the trick action
"""

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

class ShakeHand:
    name = "shake_hand"

    def __init__(self, dog: Dog):
        self.dog = dog

    def __call__(self, **_Any) -> Any:
        self.dog.output_channel(f"look, {self.dog} has extended a paw")


"""
Trick Protocol defines an interface or contract for all tricks.  Ensures any trick class has a name, an __init__ accepting a Dog, and a __call__ to perform the trick.
"""

class Trick(Protocol):
    name: str

    def __init__(self, dog: Dog): ...

    def __call__(self, **kwargs: Any) -> Any: ...


"""
get_next_pk is a helper function designed to return the next id in the students dict (or any dict).  Finds max existing key and adds 1.
"""
def get_next_pk(storage: dict[int, Any]) -> int:
    return max(storage.keys(), default=0) + 1


if __name__ == "__main__":
    """
    dog = Dog("Fluffy")                                             # We initalize the dog Fluffy
    dog_school = DogSchool([FakeDead, CatchStick, ShakeHand])                  # We initalize the dog school with the existing trick classes
    enrolling_number = dog_school.teach(dog)                        # We teach the dog Fluffy the tricks and assign him to an enrolling number

    for t in dog.tricks:                                            # We iterate throug Fluffy's tricks and perform them.
        dog.perform_trick(t)

    print(dog_school.get_student_by_number(enrolling_number))       # We print the Fluffy object
    """

    ############### MY EXAMPLES ##########################################

    dog2 = Dog("Rover")                                                     # Initialize Rover
    dog2.tricks["talk"]()                                                   # Rover by default can talk
    dog2.perform_trick("fake_dead")                                         # Rover does not know how to fake_dead yet
    dog2.learn_trick(FakeDead)                                              # We teach Rover just to fake_dead
    dog2.perform_trick("fake_dead")                                         # Rover can fake_dead now
    dog2.perform_trick("shake_hand")                                        # Rover doesn't know how to shake_hand

    viks_dog_school = DogSchool([FakeDead, CatchStick, ShakeHand])          # a DogSchool is initialized - we teach 3 tricks
    enrolled_dog_2 = viks_dog_school.teach(dog2)                            # We send Rover to viks_dog_school to learn                            
    dog2.perform_trick("shake_hand")                                        # Rover now knows how to shake_hand
    
    for t in dog2.tricks:                                                   # Show us all your tricks Rover -> good boy
        dog2.perform_trick(t)


    """
    CURIOUS QUESTIONS:
    - Why is it better to have each trick as its own class, instead of a class with tricks listed in it?
    - My dog is not the most obedient dog in the world.  It will successfully complete a trick 4/5 times.  How can I implement this?
    - I want to reward the dog with a treat each time it completes a trick successfully.  How can I implement this?
    - Dogs like to go for a walk.  If I wanted to implement this as well, dog should be able to execute a walk, but walk should be its own class?
    """