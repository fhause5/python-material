## Easy Data Transformation

### <span style="color: black">&#x1F535; Let's create a project directory with a package and a models module </span>

```
mkdir -p dbexport/dbexport
cd dbexport
touch dbexport/{__init__,models}.py

Now that we have the files we need, we're ready to finalize the project with Git and a virtualenv.

The .gitignore File
For our .gitignore file, we're going to use the one for Python maintained by GitHub. We can pull this down using the following curl command:

$ curl https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore -o .gitignore
At this point it makes sense to also initialize our project as a Git repository, so let's do that:

$ git init
Using Pipenv for our Virtual Environment
Finally, we're going to use Pipenv to manage our virtual environment and development dependencies. We need SQLAlchemy to map our database tables to our model classes.

Let's initialize our environment using Python 3.7 and install SQLAlchemy and psycopg2-binary as dependencies:

pipenv install --python python3.7 SQLAlchemy psycopg2-binary

Now we're ready to make our first commit and start developing our tool:

$ git add --all .
$ git commit -m 'Initial commit'
```
### <span style="color: black">&#x1F535; Setting Up the Server </span>

> When you installing you need to name user and passsowd (NOT IT IS NOT WORKING CENTOS7)

```
$ curl -O https://raw.githubusercontent.com/linuxacademy/content-python-use-cases/master/helpers/db_setup.sh
$ chmod +x db_setup.sh
$ ./db_setup.sh


```
to connect

> postgres://USER:PASSWORD@PUBLIC_IP:PORT/DB_NAME

### <span style="color: black">&#x1F535; Configuring a Connection </span>

We want our tool to be able to create a connection to a database based on either a string that is passed in or by fetching a connection from an environment variable.

There are a few ways to do this.

We can create a "connection" to run SQL queries directly, or if we want to
work with the ORM (Object Relational Mapper), we can use a "session".

We're going to add support for both in our library.

Ideally, we'll run the connection code once when we run our program, and we'll put it in a config module so that it's obvious where we're doing the database configuration.

We'll call the primary function get_connection, and we'll create an engine function to configure the engine (which our session will need also):

>> dbexport/config.py

```
import os
from functools import lru_cache

from sqlalchemy import create_engine


@lru_cache(maxsize=32)
def engine(db_url=None):
    db_url = db_url or os.getenv("DB_URL")
    if not db_url:
        raise ValueError("database URL is required")
    print(f"Returning an engine for {db_url}")
    return create_engine(db_url)


def get_connection(db_url=None):
    return engine(db_url).connect()

```

We're doing a few different things here:

* We're caching the result of engine so that it will only configure the engine value once based on a given database URL, and subsequent calls will return the same object from the cache.
This is done by using the functools.lru_cache decorator.

* If there is no DB_URL environment variable and no string is manually passed in, then we'll raise an error because there is absolutely no way that we can connect to the database.

* The sqlalchemy.create_engine function will give us an engine configured to interact with a specific type of database (PostgreSQL, in this case), but we won't be able to interact with the database until we get a connection by using engine.connect.

Let's give this a try in the REPL by connecting to our reviews database:
```
(dbexport) $ DB_URL="postgres://admin:password@PUBLIC_IP:80/reviews" PYTHONPATH=. python

>>> from dbexport.config import engine, get_connection
>>> db = get_connection()
Returning an engine for postgres://admin:password@PUBLIC_IP:80/reviews
>>> engine() is engine()
Returning an engine for postgres://admin:password@PUBLIC_IP:80/reviews
True
>>> engine() is engine(None)
False
>>> result = db.execute("SELECT count(id) FROM reviews")
>>> row = result.first()
>>> row[0]
2997

```

Notice that although we call engine numerous times, it only prints the first time (when called by get_connection), and when we do the comparison using is, we see that two calls to the function both return the same object.

This is the result of the lru_cache decorator caching the result from the first call.

There's a difference between engine() and engine(None) — each call has a different number of arguments even though they are functionally equivalent.

We're now able to create a database connection using an environment variable, but does it still work if we don't set DB_URL in the environment? Let's exit the REPL and start it back up without setting the variable:

```
(dbexport) $ PYTHONPATH=. python
>>> from dbexport.config import get_connection
>>> db_url = "postgres://admin:password@PUBLIC_IP:80/reviews"
>>> db = get_connection()
...
ValueError: database URL is required
>>> db = get_connection(db_url)
Returning an engine for postgres://admin:password@PUBLIC_IP:80/reviews

```

We're successfully raising an error if we have no URL, and we can also see that the lru_cache decorator depends on the arguments passed to the function.
### <span style="color: black">&#x1F535; Creating a Session </span>


To work with the ORM (Object Relational Mapper), we will need to create a sessionmaker and then use sessions to interact with the database.

A nice thing about sessions is that we get the benefit of transactions automatically and we can work with our eventual model objects as simple

Python objects until we need to interact with the database.

The sessionmaker function will create a new class for us that will be configured to interact with our database using the engine that we generate.

Let's create our engine function and generate a new session class:

```
dbexport/config.py

import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@lru_cache(maxsize=32)
def engine(db_url=None):
    db_url = db_url or os.getenv("DB_URL")
    if not db_url:
        raise ValueError("database URL is required")
    return create_engine(db_url)


def get_connection(db_url=None):
    return engine(db_url).connect()


@lru_cache(maxsize=32)
def session_class(db_url=None):
    return sessionmaker(bind=engine(db_url))


try:
    Session = session_class()
except:
    pass
```

Now we have a function for generating a Session class. When the file is loaded for the first time, we'll attempt to generate a default Session class assuming that the user is utilizing the DB_URL configuration value.

Let's load our module into the REPL without an environment variable set:
```
(dbexport) $ PYTHONPATH=. python
>>> from dbexport import config
Failed to create default Session class
```

We're seeing this message because we can't create the default engine (it's raising a ValueError). Since the creation of the default Session class is just for convenience, we'll need to implement some error handling to prevent a crash. Let's remove this print statement and load the module one last time with an environment variable:

dbexport/config.py

```
import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@lru_cache(maxsize=32)
def engine(db_url=None):
    db_url = db_url or os.getenv("DB_URL")
    if not db_url:
        raise ValueError("database URL is required")
    return create_engine(db_url)


def get_connection(db_url=None):
    return engine(db_url).connect()


@lru_cache(maxsize=32)
def session_class(db_url=None):
    return sessionmaker(bind=engine(db_url))


try:
    Session = session_class()
except:
    pass
```

```

(dbexport) $ DB_URL="postgres://admin:password@PUBLIC_IP:80/reviews" PYTHONPATH=. python
>>> from dbexport.config import Session
>>> session = Session()
>>> session
<sqlalchemy.orm.session.Session object at 0x10c0c6f28>
>>> session.bind
Engine(postgres://admin:***@keiththomps2c.mylabserver.com:80/reviews)
```

Now we have an easy way to get a Session class to create sessions that automatically connect to our database using the DB_URL. With all of this configuration in place, we're ready to start defining our models.

### <span style="color: black">&#x1F535; Understanding Our Database Schema </span>

Understanding Our Database Schema
Before we can map our database tables to models, we need to know what the database tables look like. We have two database tables that we want to map:

products — The various items that our organization sells.
reviews — Reviews for the products that our organization sells.
These database tables are relatively simple. Here's the schema for each table in SQL:
```

create table products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    level INTEGER NOT NULL,
    published BOOLEAN NOT NULL DEFAULT false,
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);
alter table products ADD CONSTRAINT level_check CHECK (
    level >= 0
    AND level <= 2
);
create table reviews (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    rating INTEGER NOT NULL,
    comment TEXT,
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);
alter table reviews add constraint rating_check CHECK (
    rating > 0
    AND rating <= 5
);
```

We need to create a class for each of our tables, and for each column, we'll need to specify an attribute using the Column class provided by SQLAlchemy.

Before all of that, though, we need to create a model base class using the declarative_base function. Here's our starting point:

dbexport/models.py

```
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    level = Column(Integer, nullable=False)
    published = Column(Boolean, nullable=False)
    created_on = Column(TIMESTAMP)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_on = Column(TIMESTAMP)
```

Notice that we're not doing anything with our database configuration. Our models can be used with any database that has these tables regardless of the database driver (PostgreSQL, MySQL, etc). We're lacking the interaction between our models, so let's work on that relationship now.

## Defining Model Relationships

When looking at our models, we can say that a product has many reviews. This is known as a "one-to-many" relationship. The other relationship types are "one-to-one" and "many-to-many".

Because the Product class has a "one-to-many" relationship with the Review class, it would make sense for us to be able to ask a Product instance for its reviews. From the database standpoint, there's nothing on the products table that gives any indication that there are reviews.

Instead, each row in the reviews database points to the associated products table using the product_id column.

Let's use the relationship capabilities of the SQLAlchemy ORM to define the relationship on both classes:

dbexport/models.py
```

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    published = Column(Boolean)
    created_on = Column(TIMESTAMP)

    reviews = relationship("Review", order_by="Review.rating", back_populates="product")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_on = Column(TIMESTAMP)

    product = relationship("Product", back_populates="reviews")
```

Now we have a great way to interact with our information, and we just need to learn how to utilize the SQLAlchemy querying interface.

### Our First SQLAlchemy Query
The Session class that we generate in the config module is what will be doing the bulk of the work of interacting with the database.

Our models are really just here to make it easier for us to conceptually work with the data. Let's load our code back into the REPL and take a look at how we can interact with the information:

```

(dbexport) $ DB_URL="postgres://admin:password@PUBLIC_IP:80/reviews" PYTHONPATH=. python

>>> from dbexport.config import Session
>>> from dbexport.models import Review, Product
>>> session = Session()
>>> from sqlalchemy import func
>>> session.query(func.count(Product.id))
<sqlalchemy.orm.query.Query object at 0x1028fe630>
>>> session.query(func.count(Product.id)).all()
[(999,)]
>>> products = session.query(Product).limit(5).all()
>>> products
[<dbexport.models.Product object at 0x10294cda0>, <dbexport.models.Product object at 0x10294ce10>, <dbexport.models.Product object at 0x10294ce80>, <dbexport.models.Product object at 0x10294cef0>, <dbexport.models.Product object at 0x10294cf60>]
>>> for product in products:
...     print(product.name)
...
unactability
sporadically
actinostomal
unsaturation
exocrine
>>> products[0].reviews
[<dbexport.models.Review object at 0x1029c78d0>, <dbexport.models.Review object at 0x1029c7940>]

```

Each time we make a query using the session.query function, it will return a query object. It will not interact with the database until we run some specific functions on the Query class, such as all.


### <span style="color: black">&#x1F535; Adding a setup.py </span>

We skipped the step where we add a setup.py to our project, but we want to be able to install our project so that it's easy to reference from scripts that we write. For the setup.py, we can use setup.py for Humans. We'll need to make some modifications, but this file will save us a lot of time.

Let's download the file and start modifying it:
```

$ curl -O https://raw.githubusercontent.com/navdeep-G/setup.py/master/setup.py

```

We need to change things in the # Package meta-data section to be about dbexport:

setup.py (partial)
```
# Package meta-data.
NAME = "dbexport"
DESCRIPTION = "Internal library for interacting with Products and Reviews database"
URL = "https://github.com/example/dbexport"
EMAIL = "me@example.com"
AUTHOR = "Awesome Soul"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.1.0"
```
What packages are required for this module to be executed?

```
REQUIRED = ["sqlalchemy", "psycopg2-binary"]
Now we can install our package:
```
```
(dbexport) $ pip install -e .

```

Writing a Script to Export CSV
Our library is very limited in scope; it only handles connecting to the database using the DB_URL environment variable convention and provides some models that map to the shape of our database tables.

For everything else that we want to do, we'll most likely just use this library in small one-off scripts.

One of our coworkers has requested a CSV file that has one line for each product that includes some standard information and also some aggregate review information.

Here's an example CSV file with a header and a single row:

```
name,level,published,created_on,review_count,avg_rating
Product 1,1,True,2019-07-10,10,4.3

```
The last two columns, review_count and avg_rating, will be calculated as part of our query. Let's start working on a script called product_csv.py. This script will have slightly more advanced SQL in it, but we'll work our way through it:

product_csv.py

```

from dbexport.config import Session
from dbexport.models import Product, Review

from sqlalchemy.sql import func

session = Session()

reviews_statement = (
    session.query(
        Review.product_id,
        func.count("*").label("review_count"),
        func.avg(Review.rating).label("avg_rating"),
    )
    .group_by(Review.product_id)
    .subquery()
)

for product, review_count, avg_rating in (
    session.query(
        Product,
        reviews_statement.c.review_count, reviews_statement.c.avg_rating
    )
    .outerjoin(reviews_statement, Product.id == reviews_statement.c.product_id)
    .limit(6)
):
    print(product)
    print(review_count)
    print(avg_rating)
```

Let's break down what we're doing after we create our session:

* We create a subquery that will calculate the average rating and count of the reviews. We then add this to the final query that we're going to make.

* We create our products query so that it returns the Product models and the calculated values for the review information. Because this query is returning more information than we defined in the Product model, SQLAlchemy will return a tuple for each row returned.

With our final query, we're leveraging the fact that a query is a generator by utilizing it directly in a for loop and unpacking the returned tuples. For our first run of this script, we've set a limit, but we'll remove this after we make sure that it can run.

```

(dbexport) $ DB_URL=$DB_URL python product_csv.py
<dbexport.models.Product object at 0x102172b38>
6
3.8333333333333333
<dbexport.models.Product object at 0x1021e7240>
6
2.1666666666666667
<dbexport.models.Product object at 0x1021e7358>
2
3.0000000000000000
<dbexport.models.Product object at 0x1021e73c8>
3
2.6666666666666667
<dbexport.models.Product object at 0x1021e7438>
3
3.0000000000000000
<dbexport.models.Product object at 0x1021e74a8>
2
1.5000000000000000
Exporting CSV

```

This looks pretty good, and now we're ready to export this information as CSV using the standard library's csv module.

product_csv.py
```
from dbexport.config import Session
from dbexport.models import Product, Review

from sqlalchemy.sql import func

import csv

csv_file = open("product_ratings.csv", mode="w")
fields = ["name", "level", "published", "created_on", "review_count", "avg_rating"]
csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
csv_writer.writeheader()

session = Session()

reviews_statement = (
    session.query(
        Review.product_id,
        func.count("*").label("review_count"),
        func.avg(Review.rating).label("avg_rating"),
    )
    .group_by(Review.product_id)
    .subquery()
)

for product, review_count, avg_rating in session.query(
    Product, reviews_statement.c.review_count, reviews_statement.c.avg_rating
).outerjoin(reviews_statement, Product.id == reviews_statement.c.product_id):
    csv_writer.writerow(
        {
            "name": product.name,
            "level": product.level,
            "published": product.published,
            "created_on": product.created_on.date(),
            "review_count": review_count or 0,
            "avg_rating": round(float(avg_rating), 4) if avg_rating else 0,
        }
    )

csv_file.close()

```

We're able to use a csv.DictWriter to write a row for each of our query rows. We need to manipulate some of the returned information (e.g., add a default if there are no reviews for a given product). We also only want to return the date for created_on instead of the full datetime.

### <span style="color: black">&#x1F535; Exporting Data as JSON </span>

The requirements for our JSON output are the same as for the CSV, except that we want to write out an array of JSON objects instead of rows. Let's start by copying the product_csv.py to product_json.py:

(dbexport) $ cp product_{csv,json}.py

Next, we're going to remove the CSV-related logic and instead build up a list of dictionaries and write them to a JSON file using the json.dump function:

product_json.py

```
from dbexport.config import Session
from dbexport.models import Product, Review

from sqlalchemy.sql import func

import json

session = Session()

reviews_statement = (
    session.query(
        Review.product_id,
        func.count("*").label("review_count"),
        func.avg(Review.rating).label("avg_rating"),
    )
    .group_by(Review.product_id)
    .subquery()
)

products = []

for product, review_count, avg_rating in session.query(
    Product, reviews_statement.c.review_count, reviews_statement.c.avg_rating
).outerjoin(reviews_statement, Product.id == reviews_statement.c.product_id):
    products.append({
        "name": product.name,
        "level": product.level,
        "published": product.published,
        "created_on": str(product.created_on.date()),
        "review_count": review_count or 0,
        "avg_rating": round(float(avg_rating), 4) if avg_rating else 0,
    })

with open("product_ratings.json", "w") as f:
    json.dump(products, f)
```

The only other change we made was with how we were writing out the created_on value.

A date object is not serializable, so we needed instead to get a str. We converted the datetime to a date and then converted that to a str.
