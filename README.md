# feedproc
Python package for xml-feeds processing.
## Usage via sqlalchemy
You can initialize feedproc with some sqlalchemy models and it will fill it with data from the feed.
Than you can save it or use somehow else.
```python
from feedproc import Parser, Source, Entity

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///foo.db', echo=True)
Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    author = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# for example get reddit feed, its structure is below
'''
<entry>
        <author>
            <name>/u/ChesyPleas</name>
            <uri>https://www.reddit.com/user/ChesyPleas</uri>
        </author>
        <category term="news" label="r/news"/>
        <content type="html">
            Some content
        </content>
        <id>t3_8mbmd4</id>
        <link href="https://www.reddit.com/r/news/comments/8mbmd4/ireland_votes_by_landslide_to_legalise_abortion/" />
        <updated>2018-05-26T17:25:01+00:00</updated>
        <title>Ireland votes by landslide to legalise abortion</title>
</entry>
'''

s1 = Source.fromHttp('https://www.reddit.com/r/news/.rss')
s1.type = 'xml'  # say feedproc the source type, may be xml, csv(in future), etc

# describe post entity with xpath expressions

entries = Entity({'./entry': {
    'author': './author/name',
    'content': './content',
    'title': './title'
}}, model=Post)
s1.bind_entity(entries)

parser = Parser()
parser.add_source(s1)
parser.run()
session.add_all(entries)
session.commit()

```


