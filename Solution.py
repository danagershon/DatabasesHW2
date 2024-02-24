from typing import List, Tuple
from psycopg2 import sql
from datetime import date, datetime

import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException
from Utility.DBConnector import ResultSet

from Business.Owner import Owner
from Business.Customer import Customer
from Business.Apartment import Apartment


def run_query(query):
    conn = None
    return_val = ReturnValue.OK
    num_rows_effected = None
    entries = None

    try:
        conn = Connector.DBConnector()
        num_rows_effected, entries = conn.execute(query)

    except DatabaseException.NOT_NULL_VIOLATION as e:
        return_val = ReturnValue.BAD_PARAMS

    except DatabaseException.CHECK_VIOLATION as e:
        return_val = ReturnValue.BAD_PARAMS

    except DatabaseException.UNIQUE_VIOLATION as e:
        return_val = ReturnValue.ALREADY_EXISTS

    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return_val = ReturnValue.NOT_EXISTS

    except Exception as e:
        return_val = ReturnValue.ERROR

    finally:
        conn.close()
        return num_rows_effected, entries, return_val


# ---------------------------------- CRUD API: ----------------------------------


def create_tables():
    owner_table = "CREATE TABLE Owner(" \
                  "id INTEGER PRIMARY KEY CHECK (id > 0), " \
                  "name TEXT NOT NULL);"

    customer_table = "CREATE TABLE Customer(" \
                     "id INTEGER PRIMARY KEY CHECK (id > 0), " \
                     "name TEXT NOT NULL);"

    apartment_table = "CREATE TABLE Apartment(" \
                      "id INTEGER PRIMARY KEY CHECK (id > 0), " \
                      "address TEXT NOT NULL, " \
                      "city TEXT NOT NULL, " \
                      "country TEXT NOT NULL, " \
                      "size INTEGER NOT NULL CHECK (id > 0), " \
                      "UNIQUE (address, city, country));"

    owned_by_table = "CREATE TABLE OwnedBy(" \
                     "apartment_id INTEGER PRIMARY KEY, " \
                     "owner_id INTEGER, " \
                     "FOREIGN KEY (apartment_id) REFERENCES Apartment(id) ON DELETE CASCADE, " \
                     "FOREIGN KEY (owner_id) REFERENCES Owner(id) ON DELETE CASCADE);"

    reservations_table = "CREATE TABLE Reservations(" \
                         "customer_id INTEGER, " \
                         "apartment_id INTEGER, " \
                         "start_date DATE NOT NULL, " \
                         "end_date DATE NOT NULL, " \
                         "total_price FLOAT(2) NOT NULL CHECK (total_price > 0), " \
                         "PRIMARY KEY (customer_id, apartment_id, start_date), " \
                         "FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE, " \
                         "FOREIGN KEY (apartment_id) REFERENCES Customer(id) ON DELETE CASCADE," \
                         "CHECK (start_date < end_date));"

    reviews_table = "CREATE TABLE Reviews(" \
                    "customer_id INTEGER, " \
                    "apartment_id INTEGER, " \
                    "date DATE NOT NULL, " \
                    "rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 10), " \
                    "review_text TEXT NOT NULL, " \
                    "PRIMARY KEY (customer_id, apartment_id), " \
                    "FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE, " \
                    "FOREIGN KEY (apartment_id) REFERENCES Apartment(id) ON DELETE CASCADE);"

    query = owner_table + customer_table + apartment_table + owned_by_table + reservations_table + reviews_table

    run_query(query)


def clear_tables():
    query = "TRUNCATE Owner, Customer, Apartment, OwnedBy, Reservations, Reviews;"
    run_query(query)


def drop_tables():
    query = "DROP TABLE IF EXISTS Owner, Customer, Apartment, OwnedBy, Reservations, Reviews CASCADE;"
    run_query(query)


def add_owner(owner: Owner) -> ReturnValue:
    owner_id, name = owner.get_owner_id(), owner.get_owner_name()
    if owner_id is None or owner_id <= 0 or name is None:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("INSERT INTO Owner(id, name) VALUES({id}, {name})").format(id=sql.Literal(owner_id),
                                                                               name=sql.Literal(name))
    _, _, return_val = run_query(query)

    return return_val


def get_owner(owner_id: int) -> Owner:
    if owner_id <= 0:
        return Owner.bad_owner()

    query = sql.SQL("SELECT id, name FROM Owner WHERE id={0}").format(sql.Literal(owner_id))

    num_rows_effected, entries, return_val = run_query(query)

    if num_rows_effected == 0:
        return Owner.bad_owner()

    entry = entries[0]

    return Owner(owner_id=entry['id'], owner_name=entry['name'])


def delete_owner(owner_id: int) -> ReturnValue:
    if owner_id <= 0:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("DELETE FROM Owner WHERE id={0}").format(sql.Literal(owner_id))

    num_rows_effected, _, return_val = run_query(query)

    if num_rows_effected == 0:
        return ReturnValue.NOT_EXISTS

    return return_val


def add_apartment(apartment: Apartment) -> ReturnValue:
    apartment_id = apartment.get_id()
    address = apartment.get_address()
    city = apartment.get_city()
    country = apartment.get_country()
    size = apartment.get_size()

    if apartment_id is None or apartment_id <= 0 or address is None or city is None or country is None or size is None \
            or size <= 0:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("INSERT INTO Apartment VALUES({id}, {address}, {city}, {country}, {size})")\
        .format(id=sql.Literal(apartment_id), address=sql.Literal(address), city=sql.Literal(city),
                country=sql.Literal(country), size=sql.Literal(size))

    _, _, return_val = run_query(query)

    return return_val


def get_apartment(apartment_id: int) -> Apartment:
    if apartment_id <= 0:
        return Apartment.bad_apartment()

    query = sql.SQL("SELECT * FROM Apartment WHERE id={0}").format(sql.Literal(apartment_id))

    num_rows_effected, entries, return_val = run_query(query)

    if num_rows_effected == 0:
        return Apartment.bad_apartment()

    entry = entries[0]

    return Apartment(id=entry['id'], address=entry['address'], city=entry['city'], country=entry['country'],
                     size=entry['size'])


def delete_apartment(apartment_id: int) -> ReturnValue:
    if apartment_id <= 0:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("DELETE FROM Apartment WHERE id={0}").format(sql.Literal(apartment_id))

    num_rows_effected, _, return_val = run_query(query)

    if num_rows_effected == 0:
        return ReturnValue.NOT_EXISTS

    return return_val


def add_customer(customer: Customer) -> ReturnValue:
    customer_id, name = customer.get_customer_id(), customer.get_customer_name()
    if customer_id is None or customer_id <= 0 or name is None:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("INSERT INTO Customer(id, name) VALUES({id}, {name})").format(id=sql.Literal(customer_id),
                                                                                  name=sql.Literal(name))
    _, _, return_val = run_query(query)

    return return_val


def get_customer(customer_id: int) -> Customer:
    if customer_id <= 0:
        return Customer.bad_customer()

    query = sql.SQL("SELECT id, name FROM Customer WHERE id={0}").format(sql.Literal(customer_id))

    num_rows_effected, entries, return_val = run_query(query)

    if num_rows_effected == 0:
        return Customer.bad_customer()

    entry = entries[0]

    return Customer(customer_id=entry['id'], customer_name=entry['name'])


def delete_customer(customer_id: int) -> ReturnValue:
    if customer_id <= 0:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("DELETE FROM Customer WHERE id={0}").format(sql.Literal(customer_id))

    num_rows_effected, _, return_val = run_query(query)

    if num_rows_effected == 0:
        return ReturnValue.NOT_EXISTS

    return return_val


def customer_made_reservation(customer_id: int, apartment_id: int, start_date: date, end_date: date, total_price: float) -> ReturnValue:
    if customer_id <= 0 or apartment_id <= 0 or start_date >= end_date or total_price <= 0:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("INSERT INTO Reservations "
                    "SELECT {customer_id}, {apartment_id}, {start_date}, {end_date}, {price} "
                    "WHERE NOT EXISTS "
                    "(SELECT * FROM Reservations "
                    " WHERE apartment_id = {apartment_id} AND start_date < {end_date} AND end_date > {start_date})")\
        .format(customer_id=sql.Literal(customer_id), apartment_id=sql.Literal(apartment_id),
                start_date=sql.Literal(start_date), end_date=sql.Literal(end_date), price=sql.Literal(total_price))

    num_rows_effected, _, return_val = run_query(query)

    if return_val == ReturnValue.OK and num_rows_effected == 0:
        return ReturnValue.BAD_PARAMS

    return return_val


def customer_cancelled_reservation(customer_id: int, apartment_id: int, start_date: date) -> ReturnValue:
    if customer_id <= 0 or apartment_id <= 0:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("DELETE FROM Reservations WHERE customer_id={0} AND apartment_id={1} AND start_date={2}")\
        .format(sql.Literal(customer_id), sql.Literal(apartment_id), sql.Literal(start_date))

    num_rows_effected, _, return_val = run_query(query)

    if num_rows_effected == 0:
        return ReturnValue.NOT_EXISTS

    return return_val


def customer_reviewed_apartment(customer_id: int, apartment_id: int, review_date: date, rating: int, review_text: str) -> ReturnValue:
    if customer_id <= 0 or apartment_id <= 0 or rating < 1 or rating > 10:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("INSERT INTO Reviews "
                    "SELECT {customer_id}, {apartment_id}, {date}, {rating}, {review_text} "
                    "WHERE EXISTS "
                    "(SELECT * FROM Reservations "
                    " WHERE customer_id={customer_id} AND apartment_id={apartment_id} AND end_date <= {date})") \
        .format(customer_id=sql.Literal(customer_id), apartment_id=sql.Literal(apartment_id),
                date=sql.Literal(review_date), rating=sql.Literal(rating), review_text=sql.Literal(review_text))

    num_rows_effected, _, return_val = run_query(query)

    if return_val == ReturnValue.OK and num_rows_effected == 0:  # customer did not have a prior reservation
        return ReturnValue.NOT_EXISTS

    return return_val


def customer_updated_review(customer_id: int, apartment_id: int, update_date: date, new_rating: int, new_text: str) -> ReturnValue:
    if customer_id <= 0 or apartment_id <= 0 or new_rating < 1 or new_rating > 10:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("UPDATE Reviews "
                    "SET date={update_date}, rating={new_rating}, review_text={new_text} "
                    "WHERE customer_id={customer_id} AND apartment_id={apartment_id} AND date < {update_date}") \
        .format(update_date=sql.Literal(update_date), new_rating=sql.Literal(new_rating),
                new_text=sql.Literal(new_text), customer_id=sql.Literal(customer_id),
                apartment_id=sql.Literal(apartment_id))

    num_rows_effected, _, return_val = run_query(query)

    if return_val == ReturnValue.OK and num_rows_effected == 0:  # customer did not have an old review
        return ReturnValue.NOT_EXISTS

    return return_val


def owner_owns_apartment(owner_id: int, apartment_id: int) -> ReturnValue:
    if owner_id <= 0 or apartment_id <= 0:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("INSERT INTO OwnedBy VALUES({apartment_id}, {owner_id})")\
        .format(apartment_id=sql.Literal(apartment_id), owner_id=sql.Literal(owner_id))

    _, _, return_val = run_query(query)

    return return_val


def owner_drops_apartment(owner_id: int, apartment_id: int) -> ReturnValue:
    if owner_id <= 0 or apartment_id <= 0:
        return ReturnValue.BAD_PARAMS

    query = sql.SQL("DELETE FROM OwnedBy WHERE apartment_id={0} AND owner_id={1}")\
        .format(sql.Literal(apartment_id), sql.Literal(owner_id))

    num_rows_effected, _, return_val = run_query(query)

    if num_rows_effected == 0:
        return ReturnValue.NOT_EXISTS

    return return_val


def get_apartment_owner(apartment_id: int) -> Owner:
    if apartment_id <= 0:
        return Owner.bad_owner()

    query = sql.SQL("SELECT id, name FROM Owner "
                    "WHERE id IN (SELECT owner_id FROM OwnedBy WHERE apartment_id={0})")\
        .format(sql.Literal(apartment_id))

    num_rows_effected, entries, return_val = run_query(query)

    if num_rows_effected == 0:
        return Owner.bad_owner()

    entry = entries[0]

    return Owner(owner_id=entry['id'], owner_name=entry['name'])


def get_owner_apartments(owner_id: int) -> List[Apartment]:
    if owner_id <= 0:
        return []

    query = sql.SQL("SELECT * FROM Apartment "
                    "WHERE id IN (SELECT apartment_id FROM OwnedBy WHERE owner_id={0})") \
        .format(sql.Literal(owner_id))

    num_rows_effected, entries, return_val = run_query(query)

    return [Apartment(id=entry['id'], address=entry['address'], city=entry['city'], country=entry['country'],
                      size=entry['size']) for entry in entries]


# ---------------------------------- BASIC API: ----------------------------------

def get_apartment_rating(apartment_id: int) -> float:
    # TODO: implement
    pass


def get_owner_rating(owner_id: int) -> float:
    # TODO: implement
    pass


def get_top_customer() -> Customer:
    # TODO: implement
    pass


def reservations_per_owner() -> List[Tuple[str, int]]:
    # TODO: implement
    pass


# ---------------------------------- ADVANCED API: ----------------------------------

def get_all_location_owners() -> List[Owner]:
    # TODO: implement
    pass


def best_value_for_money() -> Apartment:
    # TODO: implement
    pass


def profit_per_month(year: int) -> List[Tuple[int, float]]:
    # TODO: implement
    pass


def get_apartment_recommendation(customer_id: int) -> List[Tuple[Apartment, float]]:
    # TODO: implement
    pass
