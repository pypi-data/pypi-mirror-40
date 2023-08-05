from abc import ABC, ABCMeta


class AutoEnumMetaclass(ABCMeta):
    def __init__(cls, *args, **kwargs):
        if hasattr(cls, 'choices'):
            for choice, choice_human in cls.choices:
                setattr(cls, choice, choice)


class AutoEnum(ABC, metaclass=AutoEnumMetaclass):
    """
    This is an enumeration-like base class that only requires a `choices`
    attribute to be defined on the class, and auto-generates the attributes
    required for Enum-like access on the class.

    It's always implied that the first value in each `choices` entry is both
    the stored value and the name of the attribute it's accessed with, e.g.:

    ```
    class State(AutoEnum):
        choices = (
          ("NEW", "new"),
          ("BORKED", "completely broken"),
        )
    ```

    will (implicitly) define the attributes:

    ```
    State.NEW = "NEW"
    State.BORKED = "BORKED"
    ```
    """
    pass
