from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL


all_books = [
    {
        "name": "White Tiger",
        "author": "Arvind Adiga"
    },
    {
        "name": "Animal Farm",
        "author": "George Orwell"
    }
]


app = Flask(__name__)
api = Api(app, version='1.0', title='Book Api', description='An Api for Books')
CORS(app)

book_model = api.model('book', {
    'name': fields.String('Name of the book.'),
    'author': fields.String('Name of the author.')
})

person_model = api.model('data',{
    'nama': fields.String('Nama fotograper'),
    'umur': fields.String('Umur fotograper'),
    'harga': fields.String('Harga fotograper')
})

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'fg'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
parser = api.parser()
parser.add_argument('author', type=str, required=True, help='name of the author', location='form')

@api.route('/books')
class AllBooks(Resource):

    @api.marshal_with(book_model, envelope='data')
    def get(self):
        """
        get all the books
        """
        return all_books, 200

    @api.expect(book_model)
    def post(self):
        """
        add new book to the list
        """
        new_book = api.payload
        all_books.append(new_book)
        return {'result': 'Book added'}, 201

@api.route('/author/<author>')
class Author(Resource):

    @api.marshal_with(book_model, envelope='data')
    def get(self, author):
        """
        get all the books by the author
        """
        result = [book for book in all_books if book['author'] == author]
        return result

@api.route('/book/<book_name>')
class Book(Resource):

    def get(self, book_name):
        """
        get details of particular book
        """
        result = [book for book in all_books if book['name'] == book_name]
        return result

    @api.doc(parser=parser)
    def put(self, book_name):
        """
        Change the book details
        """
        args = parser.parse_args()
        for index, book in enumerate(all_books):
            if book['name'] == book_name:
                all_books[index]['author'] = args['author']
                return book, 201
        return None, 201

    def delete(self, book_name):
        """
        delete the book
        """
        for index, book in enumerate(all_books):
            if book['name'] == book_name:
                del all_books[index]
                return {"response": "book deleted"}, 204
        return None, 404
@api.route('/persons')
class AllPerson(Resource):

    @api.marshal_with(person_model, envelope='data')
    def get(self):
        cur = mysql.connect().cursor()
        cur.execute('''select * from fg.fotografer''')
        r = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
        return r, 200
        # return all_books, 200

if __name__ == '__main__':
    app.run(debug=True)