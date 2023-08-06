# Wrapper for [jsonfield](https://github.com/bradjasper/django-jsonfield) with predefined structurethat uses set of corresponding widgets for edit

Requires Django 1.8+

## Installation

```
pip install django-dictionaryfield
```

## Usage
Add "dictionaryfield" to installed apps in django settings file:

```python
INSTALLED_APPS = (
    ...
    'dictionaryfield',
    ...
)
```

### Use as model field

```python
    from collections import OrderedDict
    from django.db import models

    from dictionaryfield import DictionaryField


    class MyModel(models.Model):
        english_data = DictionaryField(
            "What is the first volume and issue in which the journal published full-text English?",
            fields=OrderedDict([
                ('volume', fields.CharField(label='Volume', required=False)),
                ('issue', fields.CharField(label='Issue', required=False))
            ])
        )
```

### Use as form field

```python
    from collections import OrderedDict
    from django.db import models

    from dictionaryfield import DictionaryFormField


    class MyForm(models.Model):
        sample_field = DictionaryFormField(
            "Sample field label",
            fields=OrderedDict([
                ('volume', fields.CharField(label='Volume', required=False)),
                ('issue', fields.CharField(label='Issue', required=False))
            ])
        )
```

### Use with bootstrap3 template tags
Dictionary field works with django-bootstrap3. In a template your should access child fields like this:

```html
    {% load bootstra3 %}

    {% bootstrap_field form.sample_field.volume %}
    {% bootstrap_field form.sample_field.issue %}
```
