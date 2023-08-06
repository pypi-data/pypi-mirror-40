# Psycopg2 Wrapper

By [Gary Chambers](https://gitlab.com/amosmoses).


## Installation

    pip install psypg

or

    python ./setup.py install

## Usage Example
### In Flask
```python
from flask import Flask
from flask import g
from psypg import PgConfig
from psypg import pg_query

DBSCHEMA = 'testdb'
DBINIFILES = 'db.ini'

app = Flask(__name__)
app.config.from_object('config')
d = PgConfig(app.config['DBSCHEMA'], app.config['DBINIFILES'])

@app.before_request
def before_request():
    try:
        g.db = d.get_handle()
    except Exception as e:
        app.logger.exception(e)
        abort(503)

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/user/<int:userid>')
def index(userid):
    query = 'select * from table where id = %s'
    rows = pg_query(g.db, query, [userid], fetch_one=True)
```

## Configuration


## Information

1. I don't like ORMs
2. I don't like ad hoc queries in my application code
3. Unless it's a really simple SQL query, I obtain all data through database functions
4. So far, so good

The database isn't simply a dumb data storage mechanism.  It is **the**
authoritative source of application information and, most importantly,
the enforcer of the rules of the application (and business). The user
interface will always be driven by the database, not vice versa.  That's
not to say that the application cannot provide some means of protection
for the database, but the database shall be the arbiter of what is and
isn't permitted.

### Known Issues

If you discover any bugs, feel free to create an issue on GitHub fork and
send us a pull request.

[Issues List](https://gitlab.com/amosmoses/psypg/issues).

## Authors

* Gary Chambers (https://gitlab.com/amosmoses)

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
