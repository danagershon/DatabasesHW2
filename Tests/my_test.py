import unittest
from datetime import date
import Solution
from Utility.ReturnValue import ReturnValue
from Tests.AbstractTest import AbstractTest

from Business.Apartment import Apartment
from Business.Owner import Owner
from Business.Customer import Customer


class TestApiBase(AbstractTest):

    def add_owners(self, owners_count):
        owners = []

        for i in range(owners_count):
            owner_id = i + 1
            owner = Owner(owner_id=owner_id, owner_name="owner " + str(owner_id))
            Solution.add_owner(owner)
            owners.append(owner)

        return owners

    def add_customers(self, customers_count):
        customers = []

        for i in range(customers_count):
            customer_id = i + 1
            customer = Customer(customer_id=customer_id, customer_name="customer " + str(customer_id))
            Solution.add_customer(customer)
            customers.append(customer)

        return customers

    def add_apartemnts(self, apartments_count):
        apartments = []

        for i in range(apartments_count):
            apartment_id = i + 1
            apartment = Apartment(id=apartment_id, address="address " + str(apartment_id),
                                  city="city " + str(apartment_id), country="country " + str(apartment_id),
                                  size=apartment_id*100)
            Solution.add_apartment(apartment)
            apartments.append(apartment)

        return apartments


class TestAddApi(TestApiBase):

    def test_add_owner(self):
        owner1 = Owner(1, "owner 1")
        self.assertEqual(ReturnValue.OK, Solution.add_owner(owner1), 'valid owner')

        owner0 = Owner(0, "owner 0")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_owner(owner0), 'invalid owner id')

        owner_id_none = Owner(None, "owner id None")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_owner(owner_id_none), 'owner id None')

        owner_name_none = Owner(1, None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_owner(owner_name_none), 'owner name None')

        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_owner(owner1), 'exact owner exists')

        owner1.set_owner_name("owner 1 different name")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_owner(owner1), 'owner id exists')

    def test_add_customer(self):
        c1 = Customer(1, "c1")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'valid customer')

        c0 = Customer(0, "c0")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c0), 'invalid customer id')

        customer_id_none = Customer(None, "owner id None")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(customer_id_none), 'customer id None')

        customer_name_none = Customer(1, None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(customer_name_none), 'customer name None')

        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_customer(c1), 'exact customer exists')

        c1.set_customer_name("c1 different name")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_customer(c1), 'customer id exists')

    def test_add_apartment(self):
        address1 = "a1 address"
        city1 = "a1 city"
        country1 = "a1 country"
        size1 = 20

        a1 = Apartment(id=1, address=address1, city=city1, country=country1, size=size1)
        self.assertEqual(ReturnValue.OK, Solution.add_apartment(a1), 'valid apartment')

        a1.set_id(0)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_apartment(a1), 'invalid apartment id')

        a1.set_id(None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_apartment(a1), 'invalid apartment id')
        a1.set_id(1)

        a1.set_address(None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_apartment(a1), 'apartment address None')
        a1.set_address(address1)

        a1.set_city(None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_apartment(a1), 'apartment city None')
        a1.set_city(city1)

        a1.set_country(None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_apartment(a1), 'apartment country None')
        a1.set_country(country1)

        a1.set_size(None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_apartment(a1), 'apartment size None')

        a1.set_size(0)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_apartment(a1), 'apartment size invalid')
        a1.set_size(size1)

        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_apartment(a1), 'exact apartment exists')

        a1.set_address("address 2")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_apartment(a1), 'apartment id exists')
        a1.set_address(address1)

        a1.set_id(2)
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_apartment(a1), 'apartment location exists')


class TestGetApi(TestApiBase):

    def test_get_owner(self):
        owners = self.add_owners(owners_count=5)

        for owner in owners:
            returned_owner = Solution.get_owner(owner.get_owner_id())
            self.assertEqual(owner, returned_owner, 'owner exists')

        self.assertEqual(Owner.bad_owner(), Solution.get_owner(owner_id=10), 'owner does not exist')
        self.assertEqual(Owner.bad_owner(), Solution.get_owner(owner_id=0), 'invalid owner id')

    def test_get_customer(self):
        customers = self.add_customers(customers_count=5)

        for customer in customers:
            returned_customer = Solution.get_customer(customer.get_customer_id())
            self.assertEqual(customer, returned_customer, 'customer exists')

        self.assertEqual(Customer.bad_customer(), Solution.get_customer(customer_id=10), 'customer does not exist')
        self.assertEqual(Customer.bad_customer(), Solution.get_customer(customer_id=0), 'invalid customer id')

    def test_get_apartment(self):
        apartments = self.add_apartemnts(apartments_count=5)

        for apartment in apartments:
            returned_apartment = Solution.get_apartment(apartment.get_id())
            self.assertEqual(apartment, returned_apartment, 'apartment exists')

        self.assertEqual(Apartment.bad_apartment(), Solution.get_apartment(apartment_id=10), 'apartment does not exist')
        self.assertEqual(Apartment.bad_apartment(), Solution.get_apartment(apartment_id=0), 'invalid apartment id')


class TestDeleteApi(TestApiBase):

    def test_delete_owner(self):
        owners = self.add_owners(owners_count=5)

        for owner in owners:
            self.assertEqual(ReturnValue.OK, Solution.delete_owner(owner.get_owner_id()), 'owner exists')
            self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_owner(owner.get_owner_id()), 'owner already deleted')

        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_owner(owner_id=10), 'owner did not exist')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.delete_owner(owner_id=0), 'invalid owner id')

    def test_delete_customer(self):
        customers = self.add_customers(customers_count=5)

        for customer in customers:
            self.assertEqual(ReturnValue.OK, Solution.delete_customer(customer.get_customer_id()), 'customer exists')
            self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_customer(customer.get_customer_id()), 'customer already deleted')

        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_customer(customer_id=10), 'customer did not exist')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.delete_customer(customer_id=0), 'invalid customer id')

    def test_delete_apartment(self):
        apartments = self.add_apartemnts(apartments_count=5)

        for apartment in apartments:
            self.assertEqual(ReturnValue.OK, Solution.delete_apartment(apartment.get_id()), 'apartment exists')
            self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_apartment(apartment.get_id()), 'apartment already deleted')

        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_apartment(apartment_id=10), 'apartment did not exist')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.delete_apartment(apartment_id=0), 'invalid apartment id')


class TestReservations(TestApiBase):

    def test_reservations(self):
        customers = self.add_customers(customers_count=2)
        apartments = self.add_apartemnts(apartments_count=2)

        for customer in customers:
            start_date = date(year=2024, month=customer.get_customer_id(), day=1)
            end_date = start_date.replace(day=10)

            for apartment in apartments:
                reservation_args = (customer.get_customer_id(), apartment.get_id(), start_date, end_date, 100)
                self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')
                self.assertEqual(ReturnValue.BAD_PARAMS, Solution.customer_made_reservation(*reservation_args), 'same reservation exists')

                new_start_date = start_date.replace(day=2)  # 2-12 overlaps with 1-10
                new_end_date = end_date.replace(day=12)
                reservation_args = (customer.get_customer_id(), apartment.get_id(), new_start_date, new_end_date, 100)
                self.assertEqual(ReturnValue.BAD_PARAMS, Solution.customer_made_reservation(*reservation_args), 'apartment not available')

                new_start_date = start_date.replace(day=10)  # 1-10 does not overlap with 10-20
                new_end_date = end_date.replace(day=20)
                reservation_args = (customer.get_customer_id(), apartment.get_id(), new_start_date, new_end_date, 100)
                self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')

                reservation_args = (customer.get_customer_id(), apartment.get_id(), new_start_date)
                self.assertEqual(ReturnValue.OK, Solution.customer_cancelled_reservation(*reservation_args), 'reservation exists')

                reservation_args = (customer.get_customer_id(), apartment.get_id(), start_date)
                self.assertEqual(ReturnValue.OK, Solution.customer_cancelled_reservation(*reservation_args), 'reservation exists')

                new_start_date = start_date.replace(day=2)  # 2-12 is available now
                new_end_date = end_date.replace(day=12)
                reservation_args = (customer.get_customer_id(), apartment.get_id(), new_start_date, new_end_date, 100)
                self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'apartment available')

        # test illegal params

        start_date = date(year=2024, month=3, day=2)
        end_date = start_date.replace(day=10)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.customer_made_reservation(0, 1, start_date, end_date, 100), 'invalid customer id')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.customer_made_reservation(1, 0, start_date, end_date, 100), 'invalid apartment id')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.customer_made_reservation(1, 1, start_date, end_date, 0), 'invalid price')

        end_date = start_date.replace(day=1)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.customer_made_reservation(1, 1, start_date, end_date, 100), 'invalid dates')
        end_date = start_date
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.customer_made_reservation(1, 1, start_date, end_date, 100), 'invalid dates')

        end_date = start_date.replace(day=10)
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_made_reservation(3, 1, start_date, end_date, 100), 'customer does not exist')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_made_reservation(1, 3, start_date, end_date, 100), 'apartment does not exist')

        start_date = date(year=2024, month=1, day=3)
        end_date = start_date.replace(day=8)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.customer_made_reservation(3, 1, start_date, end_date, 100), 'customer does not exist and apartemnt not available')

        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_cancelled_reservation(1, 1, start_date), 'reservation does not exist')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_cancelled_reservation(3, 1, start_date), 'customer does not exist')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_cancelled_reservation(1, 3, start_date), 'apartment does not exist')


class TestReviews(TestApiBase):

    def test_reviews(self):
        customers = self.add_customers(customers_count=2)
        apartments = self.add_apartemnts(apartments_count=3)

        for customer in customers:
            start_date = date(year=2024, month=customer.get_customer_id(), day=1)
            end_date = start_date.replace(day=10)

            for apartment in apartments[:2]:
                reservation_args = (customer.get_customer_id(), apartment.get_id(), start_date, end_date, 100)
                self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')

                review_args = (customer.get_customer_id(), apartment.get_id(), end_date, 1, "review text")
                self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_updated_review(*review_args), 'no existing review')

                review_args = (customer.get_customer_id(), apartment.get_id(), end_date, 10, "review text")
                self.assertEqual(ReturnValue.OK, Solution.customer_reviewed_apartment(*review_args), 'valid review')
                self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.customer_reviewed_apartment(*review_args), 'review exists')

                review_args = (customer.get_customer_id(), 3, end_date, 10, "review text")
                self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_reviewed_apartment(*review_args), 'no prior reservation')

                review_args = (customer.get_customer_id(), apartment.get_id(), end_date.replace(day=12), 1, "new review text")
                self.assertEqual(ReturnValue.OK, Solution.customer_updated_review(*review_args), 'valid review update')

                review_args = (customer.get_customer_id(), apartment.get_id(), end_date.replace(day=9), 1, "new review text")
                self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_updated_review(*review_args), 'update date is before existing review date')

        # test illegal params

        review_date = date(year=2024, month=1, day=1)

        review_args = (0, 1, review_date, 10, "review text")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.customer_reviewed_apartment(*review_args), 'invalid customer id')

        review_args = (1, 0, review_date, 10, "review text")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.customer_reviewed_apartment(*review_args), 'invalid apartment id')

        review_args = (1, 1, review_date, 11, "review text")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.customer_reviewed_apartment(*review_args), 'invalid rating')

        review_args = (3, 1, review_date, 10, "review text")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_reviewed_apartment(*review_args), 'customer does not exist')

        review_args = (1, 4, review_date, 10, "review text")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_reviewed_apartment(*review_args), 'apartment does not exist')


class TestApartmentOwnership(TestApiBase):

    def test_ownership(self):
        owners = self.add_owners(owners_count=2)
        apartments = self.add_apartemnts(apartments_count=5)

        for apartment in apartments[:4]:
            self.assertEqual(ReturnValue.OK, Solution.owner_owns_apartment(owners[0].get_owner_id(), apartment.get_id()), 'valid ownership')
            self.assertEqual(owners[0], Solution.get_apartment_owner(apartment.get_id()), 'ownership exists')

            self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.owner_owns_apartment(owners[0].get_owner_id(), apartment.get_id()), 'ownership exists')
            self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.owner_owns_apartment(owners[1].get_owner_id(), apartment.get_id()), 'owned by another')

            self.assertEqual(ReturnValue.OK, Solution.owner_drops_apartment(owners[0].get_owner_id(), apartment.get_id()), 'valid drop ownership')
            self.assertEqual(ReturnValue.NOT_EXISTS, Solution.owner_drops_apartment(owners[0].get_owner_id(), apartment.get_id()), 'ownership does not exist')
            self.assertEqual(ReturnValue.OK, Solution.owner_owns_apartment(owners[1].get_owner_id(), apartment.get_id()), 'valid ownership')

        owned_apartments = Solution.get_owner_apartments(owners[1].get_owner_id())
        self.assertEqual(len(owned_apartments), 4, 'owner 2 owns 4 apartments')
        for owned_apartment, apartment in zip(owned_apartments, apartments[:4]):
            self.assertEqual(owned_apartment, apartment, 'owner 2 owns all apartments')

        self.assertEqual([], Solution.get_owner_apartments(owners[0].get_owner_id()), 'owner 1 owns no apartments')

        # test illegal params

        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.owner_owns_apartment(owners[0].get_owner_id(), 6), 'apartment does not exist')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.owner_owns_apartment(3, 5), 'owner does not exist')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.owner_drops_apartment(owners[0].get_owner_id(), 6), 'apartment does not exist')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.owner_drops_apartment(3, 5), 'owner does not exist')


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
