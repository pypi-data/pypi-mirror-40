django-formfieldstash
*****************

.. image:: https://travis-ci.org/bnzk/django-formfieldstash.svg
    :target: https://travis-ci.org/bnzk/django-formfieldstash
.. image:: https://img.shields.io/pypi/v/django-formfieldstash.svg
    :target: https://pypi.python.org/pypi/django-formfieldstash/
.. image:: https://img.shields.io/pypi/l/django-formfieldstash.svg
    :target: https://pypi.python.org/pypi/django-formfieldstash/


show/hide modelform fields, depending on current value of a dropdown in the form. without page reload.
this is a pure javascript solution, using a modeladminmixin approach.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-formfieldstash

Add ``formfieldstash`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'formfieldstash',
    )

formfieldstash does not need it's own database tables, so no need to migrate.


Usage
------------

Have a look at ``formfieldstash/tests/test_app/admin.py`` for some examples.

.. code-block:: python

    models.py

    SELECTION_CHOICES = (
        ('', 'Empty'),
        ('horse', 'Horse'),
        ('bear', 'Bear'),
        ('octopus', 'Octopus'),
    )

    SET_CHOICES = (
        ('', 'Empty'),
        ('set1', '1'),
        ('set2', '2'),
        ('set3', '3'),
    )


    class TestModelSingle(models.Model):
        selection = models.CharField('Selection', max_length=20, blank=True, choices=SELECTION_CHOICES)
        horse = models.CharField(max_length=20, blank=True, )
        bear = models.CharField(max_length=20, blank=True, )
        octopus = models.CharField(max_length=20, blank=True, )

        def __str__(self):
            return "Single Stash Test Model: %s" % self.selection


    class TestModelAdvanced(models.Model):
        set = models.CharField('Selection', max_length=20, blank=True, choices=SET_CHOICES)
        set1_1 = models.CharField(max_length=20, blank=True, )
        set2_1 = models.CharField(max_length=20, blank=True, )
        set2_2 = models.CharField(max_length=20, blank=True, )
        set2_3 = models.CharField(max_length=20, blank=True, )
        set3_1 = models.CharField(max_length=20, blank=True, )

        def __str__(self):
            return "Test Model: %s" % self.set


    class TestInlineModel(models.Model):
        parent = models.ForeignKey(TestModelAdvanced)
        title = models.CharField(max_length=20, blank=True, )

        def __str__(self):
            return "A Simple Inline Model: %s" % self.title


    admin.py

    class TestModelAdmin(FormFieldStashMixin, admin.ModelAdmin):
        single_formfield_stash = ('selection', )

    admin.site.register(TestModelSingle, TestModelAdmin)


    class TestInlineModelInline(admin.StackedInline):
        model = TestInlineModel


    ADVANCED_STASH = {
        'set': {
            'set1': ('set1_1', '#testinlinemodel_set-group', ),
            'set2': ('set2_1', 'set2_2', 'set2_3', ),
            'set3': ('set3_1', 'set2_1', ),
        },
    }


    class TestModelAdvancedAdmin(FormFieldStashMixin, admin.ModelAdmin):
        inlines = [TestInlineModelInline, ]
        formfield_stash = ADVANCED_STASH

    admin.site.register(TestModelAdvanced, TestModelAdvancedAdmin)


Contribute
------------

Fork and code (`./manage.py runserver` brings up a test app). Either run `tox` for complete tests, or `python manage.py test
