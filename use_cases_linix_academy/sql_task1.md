
### <span style="color: black">&#x1F535; Forum Export: Modeling Database Tables with SQLAlchemy Using Python
 </span>

ssh cloud_user@PUBLIC_IP_ADDRESS


* Create a new directory named forum with an internal directory of the same name.
```
mkdir -p forum/forum
cd forum
```

Change to the forum directory.

Make the internal forum directory a package.

```
touch forum/__init__.py
```
* Install Pipenv.

```
pip3.7 install --user -U pipenv
```

Create a virtualenv, and install SQLAlchemy and psycopg2-binary as dependencies.
pipenv --python python3.7 install SQLAlchemy psycopg2-binary
Activate the virtualenv.
```
pipenv shell
```

* Add setup.py for Humans.

```
curl -O https://raw.githubusercontent.com/navdeep-G/setup.py/master/setup.py
```

Edit the NAME and DESCRIPTION parameters of the setup.py metadata, and add the dependencies we installed to the REQUIRED list.
```
# Package meta-data.
NAME = 'forum'
DESCRIPTION = 'A model library for accessing an internal forum database'
URL = 'https://github.com/me/forum'
EMAIL = 'me@example.com'
AUTHOR = 'Awesome Soul'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'

# What packages are required for this module to be executed?
REQUIRED = ['SQLAlchemy', 'psycopg2-binary']
```

Define the Post and Comment Classes in a models Module
* Create the models.py within the forum package.

```
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Post(Base):
   __tablename__ = "posts"

   id = Column(Integer, primary_key=True)
   body = Column(Text, nullable=False)
   author_name = Column(String(50), nullable=False)
   created_on = Column(TIMESTAMP)

   comments = relationship("Comment", back_populates="post")

class Comment(Base):
   __tablename__ = "comments"

   id = Column(Integer, primary_key=True)
   post_id = Column(Integer, ForeignKey("posts.id"))
   comment = Column(Text, nullable=False)
   sentiment = Column(String(10), nullable=False)
   commenter_name = Column(String(50), nullable=False)
   created_on = Column(TIMESTAMP)

   post = relationship("Post", back_populates="comments")
```

Utilize the Library from REPL

With the virtualenv started, install the package.
pip install -e .
Load Python.
python
Open a REPL, create an engine and a session, and load in some Post and Comment objects to ensure that the library is working as expected. (For the engine, you'll need to use the username of admin, a password of password, the public IP address of the database server, port 80, and a database name of forum.)
(forum) $ python

```
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import sessionmaker
>>> from forum.models import Post, Comment
>>> engine = create_engine("postgres://admin:password@PUBLIC_IP:80/forum")
>>> Session = sessionmaker(bind=engine)
>>> session = Session()
>>> posts = session.query(Post).limit(10).all()
>>> post = posts[0]
>>> post.__dict__

{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x1057ae210>, 'body': 'Voluptatem voluptatem eius numquam neque magnam.', 'id': 1, 'created_on': datetime.datetime(2019, 7, 31, 19, 9, 28, 730416), 'author_name': 'Nelson Schacht', 'comments': [<forum.models.Comment object at 0x1057bda10>, <forum.models.Comment object at 0x1057bdad0>]}
>>> post.comments[0].__dict__
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x1057bd9d0>, 'comment': 'Aliquam sed dolor numquam non. Quiquia velit etincidunt est ipsum. Numquam tempora etincidunt velit sed quisquam. Etincidunt ipsum amet etincidunt adipisci ut modi. Numquam aliquam velit dolorem quisquam dolorem voluptatem. Dolor velit quiquia sit etincidunt eius aliquam. Est magnam aliquam eius est consectetur tempora. Quaerat modi quiquia adipisci modi quaerat tempora quisquam. Sit neque sit sed quisquam porro dolore. Labore dolorem tempora eius adipisci ipsum adipisci.', 'id': 36, 'commenter_name': 'James Chavez', 'sentiment': 'postitive', 'post_id': 1, 'created_on': datetime.datetime(2019, 7, 31, 19, 9, 28, 956082)}

```
## Conclusion

Congratulations, you've successfully completed this hands-on lab!
