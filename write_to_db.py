import csv
from peewee import *  # orm

db = PostgresqlDatabase(database='parser', user='postgres', password='123', host='localhost')


class Book(Model):
    title = CharField()
    image = TextField()
    price = CharField()
    status = CharField()
    link = TextField()

    class Meta:
        database = db


def main():
    db.connect()
    db.create_tables([Book])

    with open('data.csv') as file:
        order = ['title', 'image', 'price', 'status', 'link']
        reader = csv.DictReader(file, fieldnames=order)

        books = list(reader)  # conversion to list reader object

        with db.atomic():
            # # cool way
            # for row in books:
            #     Book.create(**row)

            # fastest way
            for index in range(0, len(books), 100):
                Book.insert_many(books[index:index+100]).execute()


if __name__ == '__main__':
    main()
