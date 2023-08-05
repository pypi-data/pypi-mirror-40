=====================
Serious Django: Enums
=====================

https://github.com/serioeseGmbH/serious-django-enums

serious-django-enums defines an Enum-like class, ``AutoEnum``, that intends to bring together the pattern
to define choice fields that Django uses, and intuitive usage of Enums like most people know them.

Consider the example where you've defined your choices on a ChoiceField, e.g.::

    class SomeForm(forms.Form):
        ...
	STATE_CHOICES = (
	    ("ACTIVE", "active"),
	    ("ENDED", "ended"),
	)
	field = forms.ChoiceField(choices=STATE_CHOICES, default="ACTIVE")

What this package gives you is wrapping this in a class and having it accessible as class attributes::

    class States(AutoEnum):
        choices = (
            ("ACTIVE", "active"),
            ("ENDED", "ended"),
	)

    class SomeForm(forms.Form):
        field = forms.ChoiceField(choices=States.choices, default=States.ACTIVE)

which has the advantage of being import-able from different parts of your code and not directly tied to the form, and also gives you nice-looking property access instead of dictionary-like key access.

The definition is currently extremely basic, but has suited our needs well.


Quick start
-----------

1. Install the package with pip::

    pip install serious-django-enums

2. Import ``serious_django_enums.AutoEnum`` and subclass it, defining a ``choices`` property on the class.

3. Use the auto-defined member properties of your AutoEnum-subclasses wherever you need them.
