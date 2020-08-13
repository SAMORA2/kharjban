import click
import sys
import jdatetime
import re
from cfonts import render

from src.db.db_operations import *
from src.db.db_setup import init_db
from init import *
from src.plot.plt_records import show_plot
from src.spider.spider import *
from src.menu.cls import clear as cls

username, user_id, wealth = 1, 2, 3


def main():
    init_db()
    print_header()
    run()


def print_header():
    output = render('k h a r j b a n', gradient=['magenta', 'cyan'], font='tiny', align='center')
    long_output = render('Spend Smarter,Save More  :)', font='console', colors=["#ffffff"], align='center')
    wel_str = render('Welcome to {Kharjban}', font='console', colors=['green'], align='center')
    print(output + long_output + wel_str)


def run():
    account_msg = input('DO YOU HAVE A kharjban ACCOUNT? (y/n) ')
    if 'y' in account_msg or 'Y' in account_msg:

        name_ans = input("\nyour name: ")
        pass_ans = input("your pass: ")
        retrieve_wealth = retrieve_user(pass_ans, name_ans)

        if retrieve_wealth:

            global username, user_id, wealth
            user_id = pass_ans
            username = name_ans
            wealth = retrieve_wealth
            init_program()

        else:
            run()

    else:
        print('\nEnter your NAME and ID to create an account...\n')
        create_account()


@click.command()
@click.option('--name', prompt='your Name',
              help='who are you?')
@click.option('--id', prompt='Your id (4 alphanumeric character)',
              help='select any id!!')
@click.option('--balance', prompt='Your balance',
              help='enter your balance')
def create_account(name, id, balance):
    check_name = bool(re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', name))
    check_pass = bool(re.fullmatch('[0-9a-z]{4}?', id))
    check_balance = bool(re.fullmatch('^[0-9]+$', balance))

    print(f'\nname is:{check_name}    id is:{check_pass}    balance is:{check_balance}')
    if check_name and check_pass and check_balance:

        bool_adding = add_user(id, name, balance)
        if bool_adding:
            global username, user_id, wealth
            user_id = id
            username = name
            wealth = balance

            init_program()
        else:
            run()
    else:
        print("""                          _____
            Please Enter |VALID| character

            """)
        create_account()


def init_program():
    global wealth
    global user_id
    running = True
    actions = ['Balance Info',
               'Payment & bill',
               'Income',
               'Payment record',
               'More',
               'Change password',
               'Delete user',
               'Log out',
               'Exit',
               'Clear console']
    while running:
        print(f"\n========================",
              jdatetime.datetime.now().strftime(f"  %a %d %b %Y     %H:%M:%S      welcome {{{username}}} :)"))
        for index, i in enumerate(actions):
            print(f"({index+1}) {i}")
        print("========================\n")

        action_choice = input("How can i help you? \n")

        if action_choice == str(1):
            temp = Person.get_balance(Person(user_id, username, wealth))

            if ',' in str(temp):
                cls()
                print(f'\n=> Your Total Balance is: {temp} IRR\n')

            else:

                temp = str("{:,.0f}".format(int(temp)))
                wealth = temp
                cls()
                print(f'\n=> Your Total Balance is: {temp} IRR\n')

        elif action_choice == str(2):
            print('(1) Add Transaction')
            print('(2) Edit Transaction')
            print('(3) Delete Transaction')

            user_input = input("\nEnter your choice?  ")
            if user_input == '1':
                category_ans = str(input("\nyour category:"))
                cost_ans = str(input("your cost:"))
                date_ans = jdatetime.datetime.now().strftime(f"%d-%b-%Y %H:%M:%S")
                if type(wealth) == str:
                    wealth = wealth.split(',')
                    wealth = ''.join(wealth)
                if category_ans.isalpha() and cost_ans.isdigit() and int(wealth) - int(cost_ans) > 0:

                    wealth = add_payment(user_id, username, wealth, category_ans, cost_ans, date_ans)

                else:
                    if category_ans.isalpha() and cost_ans.isdigit():
                        print('\nOUT OF BUDGET !!!')
                    else:
                        print('\n   wrong format :(\n')
                    init_program()
            elif user_input == '2':

                show_payment(user_id)
                text_input = str(input("which transaction do you want to MODIFY? \n"))

                if text_input.isdigit():
                    try:
                        row_select = select_trans_row(int(text_input), user_id)
                        if not row_select:
                            pass
                        else:
                            print("\nNote =>You can leave each input to get previous value\n")
                            new_category = input("Your new category: ")

                            if not new_category:
                                new_category = row_select[0][1]

                            new_cost = input("Your new cost: ")
                            if not new_cost:
                                new_cost = row_select[0][2]

                            new_date = input("Your new date: e.g 08-Tir-1399 11:26:48 ")
                            if not new_date:
                                new_date = row_select[0][3]

                            check_category = bool(re.fullmatch('^[\w]+$', new_category))
                            check_cost = bool(re.fullmatch('^[\d]+$', new_cost))
                            check_date = bool(
                                re.fullmatch('^[0-9]{2}-[A-Za-z]{3,}-[0-9]{4}\s{1}[0-9]{2}:[0-9]{2}:[0-9]{2}',
                                             new_date))

                            if isinstance(wealth, str):
                                wealth = wealth.replace(',', "")

                            if int(new_cost) > int(wealth):
                                print(" \n OUT OF BUDGET :(")
                                init_program()
                            """this line has some confusing error"""
                            print('\n', check_category, check_cost, check_date)

                            if check_category and check_date and check_cost:

                                wealth = (int(wealth) - int(new_cost)) + row_select[0][2]
                                print(wealth)
                                update_transaction(row_select[0][0], int(new_cost), new_category, new_date, int(wealth),
                                                   user_id)

                            else:
                                print("""\n                     -------------
                    Wrong format :(
                   -------------  \n""")

                    except:
                        print("something seems wrong ,check your input format :(")

                else:
                    print('\n wrong format')

            elif user_input == '3':

                show_payment(user_id)
                text_input = str(input("which transaction do you want to DELETE?"))
                if text_input.isdigit():
                    try:
                        row_select = select_trans_row(int(text_input), user_id)

                        if row_select:
                            dlt_confirm = str(input("Do you want to delete permanently (y/n)? "))
                            if 'y' in dlt_confirm or 'Y' in dlt_confirm:
                                if isinstance(wealth, str):
                                    wealth = int(wealth.replace(',', ''))
                                wealth += row_select[0][2]

                                delete_transaction(user_id, row_select[0][0], wealth)

                        elif not row_select:
                            pass

                    except:
                        pass
                else:
                    print("wrong format :(")

            else:
                print('something got wrong :(')
                init_program()

        elif action_choice == str(3):
            amount = str(input('How much do you want to increase your income:'))
            if amount.isdigit():
                check_income = add_income(user_id, int(amount))
                if check_income:
                    wealth = check_income
                    wealth = "{:,.0f}".format(wealth)
                    print(f'\nyour new balance is: {wealth}\n')

                else:
                    pass
            else:
                print('\n   wrong format :(\n')
                init_program()

        elif action_choice == str(4):

            user_ans = input("\nDo you want to see GUI or CLI(g/c) ? ")
            if 'G' in user_ans or 'g' in user_ans:
                show_plot(user_id)
                init_program()
            else:
                show_payment(user_id)
                init_program()

        elif action_choice == str(5):
            print("""\n
    {1} Laptops Prices
    {2} CryptoCurrency prices\n""")
            user_answer = input("""
           Note => this operation needs iranian IP address
            Which one do you want to see? """)
            if user_answer == str(1):
                laptop_spider()

            elif user_answer == str(2):
                crypto_spider()

            else:
                print("\n   wrong number")

        elif action_choice == str(6):
            get_new_id = input('Your new id (4 alphanumeric character): ')
            check_pass = bool(re.fullmatch('[0-9a-z]{4}?', get_new_id))
            if check_pass and check_duplicate(get_new_id):
                update_pass(get_new_id, user_id)
                user_id = get_new_id
                print("\npassword changed successfully :)\n")
            elif not check_duplicate(get_new_id):
                print("""\n        -----------------------------
        Unfortunately This id existed :(
        -----------------------------
                \n""")
                init_program()
            else:
                print('\n wrong format :(')
                init_program()

        elif action_choice == str(7):
            insure = input("Do you want to delete permanently (y/n)? ")
            if 'y' in insure or 'Y' in insure:

                delete_user(user_id, username)
                run()

            else:
                print("\nwe are so glad that you stay with us :)\n")
                init_program()

        elif action_choice == str(8):
            print('\nHope you come back soon :)\n')
            run()
        elif action_choice == str(9):
            sys.exit()
        elif action_choice == str(10):
            cls()
        else:
            print('\n   !{Please Enter correct number}! \n')
            init_program()
