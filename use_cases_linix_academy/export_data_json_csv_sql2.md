### <span style="color: black">&#x1F535; Forum Export: Exporting Data as JSON and CSV Using Python</span>

Create a Virtualenv and Install the forum Package
Change to the ~/forum directory.
```
cd ~/forum
```
Create a new Python 3.7 virtualenv.
```
pipenv install

```

Activate the virtualenv.
pipenv shell
Install the forum package from source.

```
pip install -e .
```
Write the Posts Query in the export_csv.py Script
Create an export_csv.py file.

touch export_csv.py
Open the file, and add the following contents:
```
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

db_url = os.environ["DB_URL"]
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

from forum.models import Post, Comment

comments = (
   session.query(Comment.post_id, func.count("*").label("comments"))
   .group_by(Comment.post_id)
   .subquery()
)

negative_comments = (
   session.query(Comment.post_id, func.count("*").label("negative_comments"))
   .filter(Comment.sentiment == "negative")
   .group_by(Comment.post_id)
   .subquery()
)

positive_comments = (
   session.query(Comment.post_id, func.count("*").label("positive_comments"))
   .filter(Comment.sentiment == "positive")
   .group_by(Comment.post_id)
   .subquery()
)

final_query = (
   session.query(
       Post,
       comments.c.comments,
       negative_comments.c.negative_comments,
       positive_comments.c.positive_comments,
   )
   .outerjoin(comments, Post.id == comments.c.post_id)
   .outerjoin(negative_comments, Post.id == negative_comments.c.post_id)
   .outerjoin(positive_comments, Post.id == positive_comments.c.post_id)
)
```

Add the CSV Export to export_csv.py
Add the following to the end of the export_csv.py file:

```
import csv

csv_file = open("forum_export.csv", mode="w")
fields = ["id", "body", "author_name", "created_on","comments", "positive_comments", "negative_comments"]
csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
csv_writer.writeheader()

for post, comments, negative_comments, positive_comments in final_query:
   csv_writer.writerow({
       "id": post.id,
       "body": post.body,
       "author_name": post.author_name,
       "created_on": post.created_on.date(),
       "comments": comments or 0,
       "positive_comments": positive_comments or 0,
       "negative_comments": negative_comments or 0
   })

csv_file.close()
```
Save and exit the export_csv.py file.

In your terminal (with the virtualenv active), run the following command:

DB_URL=postgres://admin:password@PUBLIC_IP:80/forum python export_csv.py

View the export file to verify that the script is working as expected.
less forum_export.csv

Create the export_json.py Script

Make a copy of export_csv.py, and name it export_json.py.

cp export_csv.py export_json.py

Edit the file, and replace the import csv section with the following:
```
import json

items = []

for post, comments, negative_comments, positive_comments in final_query:
   items.append({
           "id": post.id,
           "body": post.body,
           "author_name": post.author_name,
           "created_on": str(post.created_on.date()),
           "comments": comments or 0,
           "positive_comments": positive_comments or 0,
           "negative_comments": negative_comments or 0,
       })

with open("forum_export.json", mode="w") as f:
   json.dump(items, f)
```

Save and exit the export_json.py file.

In your terminal (with the virtualenv active), run the following command:

DB_URL=postgres://admin:password@PUBLIC_IP:80/forum python export_json.py

View the export file to verify that the script is working as expected.

less forum_export.json

Conclusion
Congratulations, you've successfully completed this hands-on lab!
