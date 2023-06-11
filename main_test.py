import unittest
from models import CashMachine, InsufficientFounds


class ExchangeTest(unittest.TestCase):

    def test_odd_banknote_amount(self):
        my_machine = CashMachine()
        my_machine.add_coins(2, 10)
        my_machine.add_coins(1, 4)
        coins = my_machine.exchange(5)
        self.assertEqual(coins, {1: 3, 2: 1})

    def test_even_banknote(self):
        my_machine = CashMachine()
        my_machine.add_coins(1, 10)
        coins = my_machine.exchange(10)
        self.assertEqual(coins, {1: 10})

    def test_coin_nominal_join(self):
        my_machine = CashMachine()
        my_machine.coins_accepted.append(0.10)
        my_machine.add_coins(0.1, 4)
        my_machine.add_coins(0.2, 20)
        my_machine.add_coins(1, 9)
        my_machine.add_coins(2, 5)
        coins = my_machine.exchange(20)
        self.assertEqual(coins, {0.1: 4, 0.2: 18, 1: 8, 2: 4.0})

    def test_many_different_coins(self):
        my_machine = CashMachine()
        my_machine.coins_accepted.append(0.10)
        my_machine.add_coins(0.1, 5)
        my_machine.add_coins(0.5, 1)
        my_machine.add_coins(1, 9)
        my_machine.add_coins(2, 5)
        coins = my_machine.exchange(20)
        self.assertEqual(coins, {0.1: 5, 0.5: 1, 1: 9, 2: 5})

    def test_give_top_coins(self):
        my_machine = CashMachine()
        my_machine.add_coins(0.5, 1)
        my_machine.add_coins(1, 9)
        my_machine.add_coins(2, 6)
        coins = my_machine.exchange(20)
        self.assertEqual(coins, {1: 8, 2: 6})

    def test_not_enough_coins(self):
        my_machine = CashMachine()
        my_machine.add_coins(0.5, 1)
        self.assertRaises(InsufficientFounds, my_machine.exchange, 20)

    def test_min_coins_first(self):
        my_machine = CashMachine()
        my_machine.add_coins(0.5, 10)
        my_machine.add_coins(1, 9)
        my_machine.add_coins(2, 10)
        coins = my_machine.exchange(10)
        self.assertEqual(coins, {0.5: 10, 1: 5})


class TakeCoinsTest(unittest.TestCase):

    def test_enough_take_operation(self):
        my_machine = CashMachine()
        my_machine.add_coins(1, 9)
        my_machine.take_coins(1, 5)
        self.assertEqual(my_machine.get_coins_balance_dict(), {1: 4})

    def test_more_then_available(self):
        my_machine = CashMachine()
        my_machine.add_coins(1, 10)
        self.assertRaises(ValueError, my_machine.take_coins, 1, 20)

    def test_no_coins_loaded(self):
        my_machine = CashMachine()
        self.assertRaises(ValueError, my_machine.take_coins, 1, 20)

    def test_wrong_coin_value(self):
        my_machine = CashMachine()
        self.assertRaises(ValueError, my_machine.take_coins, 50, 1)


class AddBanknoteTest(unittest.TestCase):

    def test_add_banknote(self):
        my_machine = CashMachine()
        my_machine.add_banknote(20)
        self.assertEqual(my_machine.get_banknote_balance_dict(), {20: 1})

    def test_wrong_banknote_added(self):
        my_machine = CashMachine()
        self.assertRaises(ValueError, my_machine.add_banknote, 50)


class AddCoinTest(unittest.TestCase):

    def test_add_coin(self):
        my_machine = CashMachine()
        my_machine.add_coins(1, 10)
        self.assertEqual(my_machine.get_coins_balance_dict(), {1: 10})

    def test_wrong_coin_added(self):
        my_machine = CashMachine()
        self.assertRaises(ValueError, my_machine.add_coins, 50, 10)


class BalancePrintTest(unittest.TestCase):

    def test_empty_balance_print(self):
        my_machine = CashMachine()
        balance_message = str(my_machine)
        self.assertEqual('EMPTY', balance_message)

    def test_coins_and_banknote_balance_print(self):
        my_machine = CashMachine()
        my_machine.add_coins(1, 10)
        my_machine.add_banknote(20)
        my_machine.add_coins(2, 30)
        my_machine.add_coins(0.5, 20)
        self.assertEqual('20 0.5£, 10 1£, 30 2£, 1 20£', str(my_machine))
