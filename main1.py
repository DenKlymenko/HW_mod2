from collections import UserDict
from datetime import datetime
import math
import pickle
from abc import abstractclassmethod, ABC


# self.dict[list_of_commands[1]].Edit(list_of_commands[2])
class basic_change(ABC):
    def __init__(self, dict, list_of_commands):
        self.dict = dict
        self.list_of_commands = list_of_commands

    def change(self):
        self.dict[self.list_of_commands[1]].Edit(self.list_of_commands[2])


class Field:
    pass


class Name:
    value = ''

    def add(self, user_name):
        self.value = user_name


class Phone:
    value = ''
    dict_operator = ('096', '097', '098', '063', '067', '093', '050', '095', '066')

    def validate_phone(self, user_phone):
        if 9 < len(user_phone) < 14:
            if (user_phone[0:2] == '+38' and user_phone[3:5] in self.dict_operator) or \
                    (user_phone[0:2] in self.dict_operator):
                return user_phone

        return 'None'

    def add(self, user_phone):
        self.value = self.validate_phone(user_phone)


class Birthday:
    value = ''

    def validate(self, datetime_value):
        if (0 < int(datetime_value[0]) < 32) \
                and (0 < int(datetime_value[1]) < 13) \
                and (1900 < int(datetime_value[2]) < 2023):
            return True
        else:
            return False

    def add(self, birthday):
        self.value = birthday
        self.date_value = birthday.split('.')

        if self.validate(self.date_value):
            self.datetime_value = datetime(day=int(self.date_value[0]), month=int(self.date_value[1]),
                                           year=int(self.date_value[2]))
        else:
            self.datetime_value = datetime(day=1, month=1, year=1)
            self.value = ''


class Record(Field, Name, Phone, Birthday):
    def Add(self, user_name, user_phone='', user_birthday=''):
        self.name = Name()
        self.name.add(user_name)

        self.phone = Phone()

        if user_phone != '':
            self.phone.add(user_phone)
        else:
            self.phone.add("Empty")

        if user_birthday != '':
            self.birthday = Birthday()
            self.birthday.add(user_birthday)

    def Delete(self):
        self.phone.value = ''

    def Edit(self, new_phone):
        self.phone.value = new_phone

    def days_to_birthday(self):
        today_date = datetime.now()
        difference = today_date - self.birthday.datetime_value
        print(f'days to birthday: {int(math.fabs(difference.days))}')


class AddressBook(UserDict, Record, basic_change):  # Notes
    dict = {}
    record_number = 0
    run = True

    # notes = Notes

    def iterator(self, amount_of_elements):
        dict_items = list(iter(self.dict))
        if self.record_number >= len(dict_items):
            self.record_number = 0
        for i in range(amount_of_elements):
            print(f'{self.record_number + i}) {dict_items[self.record_number + i]}: '
                  f'{self.dict[dict_items[self.record_number + i]].birthday.value}')

            if self.dict[dict_items[self.record_number + i]].phone.value:
                print(f' {self.dict[dict_items[self.record_number + i]].phone.value}')
            else:
                print('phone_list is empty!!')
        self.record_number += amount_of_elements

    def find_by_name(self, name):
        print(f'name: {name}')
        print(f'\t {self.dict[name].phone.value}')

    def find_by_phone(self, phone):
        for key, value in self.dict.items():
            if value.phone.value == phone:
                print(f'{key}:{phone}')

    def add_record(self, user_name, user_phone='', user_birthday=''):
        record = Record()
        record.Add(user_name, user_phone, user_birthday)
        self.dict.update({record.name.value: record})

    def process(self, list_of_commands):
        if len(list_of_commands) == 1:
            if list_of_commands[0] == 'hello':
                print('How can I help you?')
            elif list_of_commands[0] == 'close' or list_of_commands[0] == 'exit':
                print('Good bye!')
                self.run = False
        elif len(list_of_commands) == 2:
            if list_of_commands[0] == 'good' and list_of_commands[1] == 'bye':
                print('Good bye!')
                self.run = False

            elif list_of_commands[0] == 'search':
                for key, value in self.dict.items():
                    if list_of_commands[1] in key or list_of_commands[1] in value.birthday.value \
                            or list_of_commands[1] in value.phone.value:
                        print(f'{key}: {value.birthday.value}')
                        print(f' {value.phone.value}')

            elif list_of_commands[0] == 'open':
                self.dict = pickle.load(open(list_of_commands[1] + '.pkl', 'rb'))
            elif list_of_commands[0] == 'save':
                pickle.dump(self.dict, open(list_of_commands[1] + '.pkl', 'wb'))


            elif list_of_commands[0] == 'days_to_birthday':
                self.dict[list_of_commands[1]].days_to_birthday()
            elif list_of_commands[0] == 'iterator':
                self.iterator(int(list_of_commands[1]))


            elif list_of_commands[0] == 'show' and list_of_commands[1] == 'all':
                for key, value in self.dict.items():
                    print(f'{key}: {value.birthday.value}')
                    print(f' {value.phone.value}')
            elif list_of_commands[0] == 'add':
                self.add_record(list_of_commands[1], '', '')
            elif list_of_commands[0] == 'find_name':
                self.find_by_name(list_of_commands[1])
            elif list_of_commands[0] == 'find_phone':
                self.find_by_phone(list_of_commands[1])
            elif list_of_commands[0] == 'phone':
                print(f"{list_of_commands[1]}: ")
                for phone in self.dict[list_of_commands[1]].phone.value:
                    print(f'\t {phone.value}')
            elif list_of_commands[0] == 'delete':
                self.dict[list_of_commands[1]].Delete()
        elif len(list_of_commands) == 3:
            if list_of_commands[0] == 'add':
                self.add_record(list_of_commands[1], list_of_commands[2], '')
            elif list_of_commands[0] == 'change':
                bc = basic_change(self.dict, list_of_commands)
                bc.change()
                #self.dict[list_of_commands[1]].Edit(list_of_commands[2])
        elif len(list_of_commands) == 4:
            if list_of_commands[0] == 'add':
                self.add_record(list_of_commands[1], list_of_commands[2], list_of_commands[3])
        else:
            print('I can\'t understand you')

    def input_error(self, user_input):
        try:
            if user_input[0] == '':
                raise Exception('string cannot be empty')
            elif user_input[0] == 'days_to_birthday':
                if len(user_input) == 1:
                    raise Exception('operator days_to_birthday error: birthday was missed')
                elif len(user_input) > 2:
                    raise Exception('operator days_to_birthday error: too much args')

            elif user_input[0] == 'save':
                if len(user_input) == 1:
                    raise Exception('operator save error: file name was missed')
                elif len(user_input) > 2:
                    raise Exception('operator save error: too much args')

            elif user_input[0] == 'search':
                if len(user_input) == 1:
                    raise Exception('operator search error: key word was missed')
                elif len(user_input) > 2:
                    raise Exception('operator search error: too much args')

            elif user_input[0] == 'open':
                if len(user_input) == 1:
                    raise Exception('operator open error: file name was missed')
                elif len(user_input) > 2:
                    raise Exception('operator open error: too much args')

            elif user_input[0] == 'iterator':
                if len(user_input) == 1:
                    raise Exception('operator iterator error: amount_of_elements was missed')
                elif len(user_input) > 2:
                    raise Exception('operator iterator error: too much args')
            elif user_input[0] == 'add':
                if len(user_input) < 3:
                    raise Exception('operator add error: name or phone number were missed')
                elif len(user_input) > 4:
                    raise Exception('operator add error: too much args')
            elif user_input[0] == 'hello' and len(user_input) > 1:
                raise Exception('operator hello error: hello must be a single operator')
            elif user_input[0] == 'change':
                if len(user_input) < 3:
                    raise Exception('operator change error: name or phone number were missed')
                elif len(user_input) > 3:
                    raise Exception('operator change error: too much args')
            elif user_input[0] == 'phone':
                if len(user_input) < 2:
                    raise Exception('operator phone error: name was missed')
                elif len(user_input) > 2:
                    raise Exception('operator phone error: too much args')
            elif user_input[0] == 'show' and user_input[1] == 'all':
                if len(user_input) > 2:
                    raise Exception('operator show all error: show all must be a single operator')
            return False
        except Exception as e:
            print(e)
            return True
        except KeyError:
            return True
        except IndexError:
            return True

    def parcer(self):
        while True:
            user_input = input('>>> ').split(' ')
            if self.input_error(user_input) == False:
                return user_input
            else:
                pass


def main():
    address_book = AddressBook()

    while address_book.run:
        address_book.process(address_book.parcer())


main()
