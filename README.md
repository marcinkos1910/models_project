# Django Models
## REPL
- read
- evaluate
- print
- loop

## select_related - one relation to all objects ("follows" foreign-key relationships, selecting additional related-object data when it executes its query)
## prefetch_related - does a separate lookup for each relationship, and does the "joining" in Python

## Hands-on - ability to write code from your head

# Models

## ORM - object-relational-mapping

- another name for model layer

1. Relational Data

- Rows in tables in databases
- SQL

2. Python Data

- Classes and objects, values and variables

3. ORM bridges the gap

- Model classes are mapped to tables
- SQL is generated
    - create/change tables (migrations)
    - insert/update/delete rows
- We only write python code

4. Pros/Cons

- less control over exact SQL
- slight performance loss
- can optimize queries with Django
- can run raw SQL with Django

## Django models

- mapped to DB tables
- generate UI (ModelForm)
- validate forms
- generate admin interface
- add custom methods

### Supported dbs:

- PostgreSQL, MariaDB, MySQL, Oracle, SQLite
- with packages: DB2, MS SQL, and more

## Models:

- python classes
- mapped to databases tables
- each object is a row in the table

## Migrations:

- python scripts
- keep db structure in sync with code
- auto-generated (not always )

## Relations:

- ForeignKey
- OneToOne
- ManyToMany

## Field class determines:

- [field references](https://docs.djangoproject.com/en/3.2/ref/models/fields/)
- Database column type (INTEGER, VARCHAR)
- how the field is rendered in a form
- field options:
    - db validation
    - form rendering and validation
    - default values
    - more

- storing numbers:
    - BooleanField
    - IntegerField with variants
    - FloatField
    - DecimalField

- storing text
    - CharField, (HTML: Input Text, required max_length option)
    - TextField, (HTML: TextArea)
    - EmailField
    - URLField
    - FilePathField
    - SlugField
    - GenericIPAddressField

- other common field types
    - DateField, TimeField, DateTimeField, DurationField
    - ImageField, FileField
    - JSONField
    - BinaryField

## Manager
- every model class has a Manager: objects
- we use this to run queries against the table 
- add functionality to class model
- each model class has manager through objects field
- we can create custom managers for models
- all QuerySet methods are available on the Manager (i.e. objects.count())

## QuerySet
- represent th database query
- list of objects with db data
- lazy (list(queryset), for, reduce, queryset[3])

```python

# lookup (SQL -> WHERE)
# filer and exclude use AND in WHERE clause
Product.objects.filter(name__contains="a")
Product.objects.exclude(stock_count=0, price=10)

# Raises exception if not exactly 1 match (use only for unique)
Product.objects.get(pk=1)
get_object_or_404(Product, pk=1)

```

### Lookups

- specifying more complex WHERE
- Syntax:
    - field__lookuptype=value

## Customizing Model

1. Model Meta Class
2. Custom methods
    - Fat models, skinny views (antipattern)
    - get_absolute_url()  # defines canonical url
3. Custom managers
4. Model inheritance
    - Abstract base class
        - meta abstract=True
        - parent has no table
    - Multi-table inheritance
        - each class generate table
    - Proxy
        - only change python behaviour

```python
class Product:
    class Meta:
        verbose_name = "Example Django Model"
        verbose_name_plural = "Example Django Models"
        ordering = ["name"]
```


## Optimization

- Premature Optimization is a bad thing

- QuerySet results are cached
- Reducing queries
    - select_related()
    - prefetch_related
- Running raw SQL
- DB Transactions
    - ATOMIC_REQUESTS

## Snippets

```python

# Logging all SQL (settings.py)
LOGGING = {
    "version": 1,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django.db.backends": {"level": "DEBUG"}},
    "root": {"handlers": ["console"]},
}

```

```python

# example django model
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    stock_count = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

```

```python

# create example row in table update and delete
p = Person(name="John", stock_count=3, price=20)
p.save()
p.price = 30
p.save()
p.delete()

Product.objects.bulk_create([p, p2])
```

```python

# Make field nullable (default is non-Null)
models.IntegerField(null=True)

# Allow empty values in form (not db-related)
models.CharField(blank=True)

# Default value
models.CharField(default="")

# Add unique constraint
models.CharField(unique=True)

# Add an index
models.CharField(db_index=True)

# Set a column name
models.CharField(db_column="column_name")

# Type specific option example
models.DateTimeField(auto_now=True)

# Set field label
models.CharField(verbose_name="Bank account")

# Additional help text
models.CharField(help_text="Enter your full name")
```

```python

# example django model
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)


class ProductImage(models.Model):
    # One to many relation, created by ForeignKey field on the 'many' side
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class Category(models.Model):
    # many to many relation
    # can be on either side of relation
    # join table in database
    products = models.ManyToManyField('Product')

```

```bash
python ./manage.py makemigrations app_name_optionally
python ./manage.py migrate app_name_optionally
python ./manage.py sqlmigrate app_name 0001

python ./manage.py shell

python manage.py showmigrations
python manage.py sqlmigrate my_app 0004

python manage.py makemigrations --dry-run
python manage.py makemigrations --merge

python manage.py makemigrations my_app 0004
python manage.py makemigrations my_app zero

python manage.py squashmigrations my_app 0005

python manage.py squashmigrations my_app --empty

```

```python

Product.objects.all()

# single object
Product.objects.get(pk=1)
# 0+ objects
Product.objects.filter(category='test' )


# Lookup
Product.objects.filter(category__name='test')
Product.objects.filter(category__name__contains ='test')
Product.objects.filter(category__name__contains ='test').distinct()
Product.objects.filter(name__endswith='st')
Product.objects.filter(name__contains='a', price__lt=80)
Product.objects.filter(name__contains='a', price__lt=80).count()
Product.objects.filter(name__contains='a', price__lt=80).exclude(stack_count__gt=4)

# Limiting
Product.objects.all()[:5]
Product.objects.all()[2]
Product.object.reverse()[0]
Product.object.reverse().first()
Product.object.reverse().last()

# Ordering
Product.objects.order_by("name")
Product.objects.order_by("name").values()
Product.objects.order_by("name").values("name", "price")
Product.objects.order_by("name").values_list("name", "price")
Product.objects.order_by("name").reverse()[:3]

```

# Issues
- problem with Model.objects.reverse() -> needs be checked!