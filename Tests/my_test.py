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

    def add_apartemnts(self, apartments_count, same_city=False):
        apartments = []

        for i in range(apartments_count):
            apartment_id = i + 1
            address = "address " + str(apartment_id)
            city = "city " + (str(apartment_id) if not same_city else '')
            country = "country " + (str(apartment_id) if not same_city else '')
            apartment = Apartment(id=apartment_id, address=address, city=city, country=country, size=apartment_id*100)
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


class TestApartmentOwnerRating(TestApiBase):

    def test_apartment_owner_rating(self):
        customers = self.add_customers(customers_count=2)
        owners = self.add_owners(owners_count=2+1)
        apartments = self.add_apartemnts(apartments_count=2+1)

        for owner, apartment in zip(owners[:2], apartments):
            self.assertEqual(ReturnValue.OK, Solution.owner_owns_apartment(owner.get_owner_id(), apartment.get_id()), 'valid ownership')

        for customer in customers:
            start_date = date(year=2024, month=customer.get_customer_id(), day=1)
            end_date = start_date.replace(day=10)

            for apartment in apartments[:2]:
                reservation_args = (customer.get_customer_id(), apartment.get_id(), start_date, end_date, 100)
                self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')

                review_args = (customer.get_customer_id(), apartment.get_id(), end_date, customer.get_customer_id(), "review text")
                self.assertEqual(ReturnValue.OK, Solution.customer_reviewed_apartment(*review_args), 'valid review')

        for apartment in apartments[:2]:
            self.assertEqual(1.5, Solution.get_apartment_rating(apartment.get_id()))

        self.assertEqual(0, Solution.get_apartment_rating(4))  # apartment does not exist

        for owner in owners[:2]:
            self.assertEqual(1.5, Solution.get_owner_rating(owner.get_owner_id()))

        self.assertEqual(0, Solution.get_owner_rating(4))  # owner does not exist
        self.assertEqual(0, Solution.get_owner_rating(3))  # owner has no apartments

        self.assertEqual(ReturnValue.OK, Solution.owner_owns_apartment(owners[-1].get_owner_id(), apartments[-1].get_id()), 'valid ownership')
        self.assertEqual(0, Solution.get_owner_rating(3))  # owner has apartment without reviews


class TestTopCustomer(TestApiBase):

    def test_top_customer(self):
        self.assertEqual(Customer.bad_customer(), Solution.get_top_customer())  # no customers

        customers = self.add_customers(customers_count=10+1)
        apartments = self.add_apartemnts(apartments_count=10+1)

        self.assertEqual(customers[0], Solution.get_top_customer())  # customers exist but not reservations

        # customer i will make i reservations (for apartments 1 to i)

        for customer in customers[:10]:
            start_date = date(year=2024, month=customer.get_customer_id(), day=1)
            end_date = start_date.replace(day=10)

            for apartment in apartments[:customer.get_customer_id()]:
                reservation_args = (customer.get_customer_id(), apartment.get_id(), start_date, end_date, 100)
                self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')

        self.assertEqual(customers[-2], Solution.get_top_customer())  # customer 10 has most reservations (10)

        # add customer 11 reservations for all apartments (10) to tie with customer 10
        for apartment in apartments[:10]:
            start_date = date(year=2024, month=customers[-1].get_customer_id(), day=1)
            end_date = start_date.replace(day=10)
            reservation_args = (customers[-1].get_customer_id(), apartment.get_id(), start_date, end_date, 100)
            self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')

        self.assertEqual(customers[-2], Solution.get_top_customer())  # customer 10 and 11 have most reservations (10) but 10 has lower id

        # add customer 11 another reservation to make him top customer
        start_date = date(year=2024, month=customers[-1].get_customer_id(), day=1)
        end_date = start_date.replace(day=10)
        reservation_args = (customers[-1].get_customer_id(), apartments[-1].get_id(), start_date, end_date, 100)
        self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')

        self.assertEqual(customers[-1], Solution.get_top_customer())  # customer 11 has most reservations (11)


class TestReservationsPerOwner(TestApiBase):

    def test_reservation_per_owner(self):
        customers = self.add_customers(customers_count=4)
        owners = self.add_owners(owners_count=2+1)
        apartments = self.add_apartemnts(apartments_count=2+1)

        for owner, apartment in zip(owners[:2], apartments[:2]):
            self.assertEqual(ReturnValue.OK, Solution.owner_owns_apartment(owner.get_owner_id(), apartment.get_id()), 'valid ownership')

        for customer in customers:
            start_date = date(year=2024, month=customer.get_customer_id(), day=1)
            end_date = start_date.replace(day=10)

            for apartment in apartments[:2]:
                reservation_args = (customer.get_customer_id(), apartment.get_id(), start_date, end_date, 100)
                self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')

        expected_reservations_per_owner = [(owner.get_owner_name(), 4) for owner in owners[:2]]\
            + [(owners[-1].get_owner_name(), 0)]
        # owner 3 has no apartments
        self.assertEqual(set(expected_reservations_per_owner), set(Solution.reservations_per_owner()))

        self.assertEqual(ReturnValue.OK, Solution.owner_owns_apartment(owners[-1].get_owner_id(), apartments[-1].get_id()), 'valid ownership')
        # owner 3 now has an apartment w/o reservations
        self.assertEqual(set(expected_reservations_per_owner), set(Solution.reservations_per_owner()))

        same_name_owner = Owner(owner_id=4, owner_name="owner 1")
        Solution.add_owner(same_name_owner)
        # owners 1 and 4 have the same name => will have ("owner 1", owner 1 count + owner 4 count = 4 + 0) in list
        self.assertEqual(set(expected_reservations_per_owner), set(Solution.reservations_per_owner()))


class TestGetAllLocationOwners(TestApiBase):
    def testGetAllLocationOwners_whenOneOwnersHasAllApartment_shouldReturnOwner(self):
        #arrange
        owners = self.add_owners(owners_count=3)
        apartments = self.add_apartemnts(apartments_count=3)
        for apartment in apartments:
            Solution.owner_owns_apartment(owner_id=1, apartment_id=apartment.get_id())

        #act
        allLocationOwners = Solution.get_all_location_owners()

        assert len(allLocationOwners) == 1
        assert allLocationOwners[0].__eq__(owners[0])


class TestGetAllLocationOwners2(TestApiBase):

    def test_get_all_location_owners(self):
        owners = self.add_owners(owners_count=2+1)
        apartments = self.add_apartemnts(apartments_count=4, same_city=True)

        for apartment in apartments[:2]:
            self.assertEqual(ReturnValue.OK, Solution.owner_owns_apartment(owners[0].get_owner_id(), apartment.get_id()))

        for apartment in apartments[2:]:
            self.assertEqual(ReturnValue.OK, Solution.owner_owns_apartment(owners[1].get_owner_id(), apartment.get_id()))

        all_location_owners = Solution.get_all_location_owners()
        self.assertEqual(all_location_owners, owners[:2])

        # case of no owners / no owned apartments will not be tested


class TestBestValueForMoney(TestApiBase):

    def test_best_value_for_money(self):
        customers = self.add_customers(customers_count=2)
        apartments = self.add_apartemnts(apartments_count=2)

        for customer in customers:
            start_date = date(year=2024, month=customer.get_customer_id(), day=1)
            end_date = start_date.replace(day=10)

            for apartment in apartments:
                reservation_args = (customer.get_customer_id(), apartment.get_id(), start_date, end_date, 100)
                self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')

                review_args = (customer.get_customer_id(), apartment.get_id(), end_date, apartment.get_id() * 2, "review text")
                self.assertEqual(ReturnValue.OK, Solution.customer_reviewed_apartment(*review_args), 'valid review')

        self.assertEqual(apartments[-1], Solution.best_value_for_money())


class TestProfitPerYear(TestApiBase):

    def test_profit_per_year(self):
        customers = self.add_customers(customers_count=2)
        apartments = self.add_apartemnts(apartments_count=2)

        for customer in customers:
            start_date = date(year=2024, month=customer.get_customer_id(), day=1)
            end_date = start_date.replace(day=10)

            for apartment in apartments:
                reservation_args = (customer.get_customer_id(), apartment.get_id(), start_date, end_date, 100)
                self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')

        expected_profit = [(1, 0.15 * 200), (2, 0.15 * 200)] + [(month, 0.0) for month in range(3, 12+1)]
        self.assertEqual(expected_profit, Solution.profit_per_month(2024))


class TestGetApartmentRecommendation(TestApiBase):

    def test_get_apartment_recommendation(self):
        customers = self.add_customers(customers_count=2)
        apartments = self.add_apartemnts(apartments_count=2)

        start_date = date(year=2024, month=customers[0].get_customer_id(), day=1)
        end_date = start_date.replace(day=10)

        reservation_args = (customers[0].get_customer_id(), apartments[0].get_id(), start_date, end_date, 100)
        self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')

        review_args = (customers[0].get_customer_id(), apartments[0].get_id(), end_date, 6, "review text")
        self.assertEqual(ReturnValue.OK, Solution.customer_reviewed_apartment(*review_args), 'valid review')

        for apartment in apartments:
            start_date = date(year=2024, month=customers[1].get_customer_id(), day=1)
            end_date = start_date.replace(day=10)

            reservation_args = (customers[1].get_customer_id(), apartment.get_id(), start_date, end_date, 100)
            self.assertEqual(ReturnValue.OK, Solution.customer_made_reservation(*reservation_args), 'valid reservation')

            review_args = (customers[1].get_customer_id(), apartment.get_id(), end_date, 3 if apartment.get_id() == 1 else 2, "review text")
            self.assertEqual(ReturnValue.OK, Solution.customer_reviewed_apartment(*review_args), 'valid review')

        self.assertEqual([(apartments[1], 4.0)], Solution.get_apartment_recommendation(customers[0].get_customer_id()))


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
