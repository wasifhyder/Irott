from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.testing.schema import Table

Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine('mysql+mysqldb://root@localhost/wordnet')

# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
Words = Base.classes.words
Senses = Base.classes.senses
Synsets = Base.classes.synsets

session = Session(engine)


# rudimentary relationships are produced

# collection-based relationships are by default named
# "<classname>_collection"