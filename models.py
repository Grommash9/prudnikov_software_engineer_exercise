import copy


class CashMachine:

    coins_accepted = [0.2, 0.5, 1, 2]
    bills_accepted = [5, 10, 20]
    currency_code = '£'

    def __init__(self):
        self.__coins_storage = {}
        self.__banknote_storage = {}

    def add_coins(self, type_of_coin: float, number_of_coins: int):
        if type_of_coin not in self.coins_accepted:
            raise ValueError(f"{type_of_coin} is not in the list of accepted coins value {self.coins_accepted}")
        self.__coins_storage[type_of_coin] = self.__coins_storage.get(type_of_coin, 0) + number_of_coins

    def take_coins(self, type_of_coin: float, number_of_coins: int):
        cur_amount = self.__coins_storage.get(type_of_coin, 0)
        if number_of_coins > self.__coins_storage.get(type_of_coin, 0):
            raise ValueError('There is no this amount of coins available!')
        self.__coins_storage[type_of_coin] = cur_amount - number_of_coins

    def add_banknote(self, banknote_amount: int):
        if float(banknote_amount) not in self.bills_accepted:
            raise ValueError(f"{banknote_amount} is not in the list of accepted banknote value {self.bills_accepted}")
        self.__banknote_storage[banknote_amount] = self.__banknote_storage.get(banknote_amount, 0) + 1

    def get_coins_balance_dict(self):
        return copy.deepcopy(self.__coins_storage)

    def get_banknote_balance_dict(self):
        return copy.deepcopy(self.__banknote_storage)

    def get_str_for_money_dicts(self, dicts_to_process: list[dict]):
        balance_info = []
        for dict_to_process in dicts_to_process:
            sorted_dict_to_process = dict(sorted(dict_to_process.items()))
            for type_of_money, number_of in sorted_dict_to_process.items():
                if number_of == 0:
                    continue
                str_type_of_money = int(type_of_money) if int(type_of_money) == type_of_money else type_of_money
                balance_info.append(f'{int(number_of)} {str_type_of_money}{self.currency_code}')
        if len(balance_info) == 0:
            return 'EMPTY'
        return ', '.join(balance_info)

    def __str__(self):
        return self.get_str_for_money_dicts([self.__coins_storage, self.__banknote_storage])

    def __check_pay_possibility_using_coins_left(self, amount, exclude_coins):
        # Checking if we can pay the rest of the amount with the coins we have
        coins_balance = self.get_coins_balance_dict()
        for coins in exclude_coins:
            coins_balance.pop(coins)
        if len(coins_balance) == 0:
            return True
        for type_of_coin, number_of_coins in coins_balance.items():
            number_of_coins_to_use = amount // type_of_coin
            amount_to_pay = number_of_coins_to_use * type_of_coin
            amount -= amount_to_pay
            if amount == 0:
                return True
        return False

    def exchange(self, banknote_amount):
        if float(banknote_amount) not in self.bills_accepted:
            raise ValueError(f"{banknote_amount} is not in the list of accepted banknote value {self.bills_accepted}")

        left_to_pay, coins_to_give = banknote_amount, dict()

        sorted_dict_to_process = dict(sorted(self.__coins_storage.items()))
        for type_of_coin, number_of_coins in sorted_dict_to_process.items():
            max_coins_needed = left_to_pay // type_of_coin
            number_of_coins_to_give = number_of_coins if max_coins_needed > number_of_coins else max_coins_needed
            exclude_coins_list = list(coins_to_give.keys()) + [type_of_coin]
            while number_of_coins_to_give > 0:
                amount_left_to_pay = round(left_to_pay - type_of_coin * number_of_coins_to_give, 2)

                if self.__check_pay_possibility_using_coins_left(amount_left_to_pay, exclude_coins_list):
                    break
                number_of_coins_to_give -= 1

            left_to_pay = round(left_to_pay - type_of_coin * number_of_coins_to_give, 2)
            coins_to_give[type_of_coin] = number_of_coins_to_give
        if left_to_pay > 0:
            raise InsufficientFounds
        self.add_banknote(banknote_amount)
        for type_of_coin, number_of_coins in coins_to_give.items():
            self.take_coins(type_of_coin, number_of_coins)
        return {type_of_coin: number_of_coins for type_of_coin, number_of_coins
                in coins_to_give.items() if number_of_coins > 0}


class InsufficientFounds(Exception):
    pass
