import sys
import gspread

from cardHolder import cardHolder

from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("client_database")


print(
    """
                    ░█████╗░████████╗███╗░░░███╗
                    ██╔══██╗╚══██╔══╝████╗░████║
                    ███████║░░░██║░░░██╔████╔██║
                    ██╔══██║░░░██║░░░██║╚██╔╝██║
                    ██║░░██║░░░██║░░░██║░╚═╝░██║
                    ╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝
                   """
)


def print_menu():
    # Print options to the user
    print("Please chose from one of the follewing options...")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Show Balance")
    print("4. Exit")


def validate_card_Num():
    list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
    while True:
        card_num = input("\n𝐏𝐥𝐞𝐚𝐬𝐞 𝐢𝐧𝐬𝐞𝐫𝐭 𝐲𝐨𝐮𝐫 𝐜𝐚𝐫𝐝: ")
        user = [holder for holder in list_of_cardHolders if card_num == holder[0]]
        if card_num and len(user) > 0:
            break
        elif not card_num:
            print("\n𝐏𝐥𝐞𝐚𝐬𝐞 𝐢𝐧𝐬𝐞𝐫𝐭 𝐲𝐨𝐮𝐫 𝐜𝐚𝐫𝐝: ")
        else:
            print("Card number not recognized")
    return cardHolder(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4])


def validate_user(cardHolder):
    list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
    user = [
        holder
        for holder in list_of_cardHolders
        if cardHolder.get_cardNum() == holder[0]
    ]
    tries = 0
    while tries < 3:
        tries += 1
        pin_code = input("\n𝗣𝗹𝗲𝗮𝘀𝗲 𝗲𝗻𝘁𝗲𝗿 𝘆𝗼𝘂𝗿 𝗣𝗜𝗡: ")
        if not pin_code:
            print("\nPlease enter PIN, try again.")
            status = False
        elif not pin_code.isnumeric():
            print("\nOnly numbers allowed. Insert your card and try again.")
            status = False
            sys.exit()
        elif pin_code.isnumeric() and pin_code == user[0][1]:
            status = True
            break
        elif tries == 3:
            print("\nSorry you've exceeded you trial limit")
            status = False
            sys.exit()
        else:
            print("\nIncorrect PIN, try again.")
            status = False
    return status


def deposit(cardHolder):
    list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
    user = [
        holder
        for holder in list_of_cardHolders
        if cardHolder.get_cardNum() == holder[0]
    ]
    while True:
        amount = input("\nHow much would you like to deposit: € ")
        if not amount:
            print("\nPlease enter an amount, try again.")
            status = False
        elif not amount.isnumeric():
            print("\nEnter only amount in figures.")
            status = False
        else:
            status = True
            new_balance = float(cardHolder.get_balance()) + float(amount)
            cardHolder.set_balance(new_balance)
            cur_user = SHEET.worksheet("client").find(user[0][0])
            SHEET.worksheet("client").update_cell(cur_user.row, 5, new_balance)
            print("\nSuccessfully deposited to your account.")
            break
    return True


def withdraw(cardHolder):
    list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
    user = [
        holder
        for holder in list_of_cardHolders
        if cardHolder.get_cardNum() == holder[0]
    ]
    while True:
        amount = input("\nHow much would you like to withdraw: € ")
        if not amount:
            print("\nPlease enter an amount to withdraw, try again.")
            status = False
        elif not amount.isnumeric():
            print("\nEnter only amount in figures.")
            status = False
        elif float(cardHolder.get_balance()) < float(amount):
            print("\nInsufficient balance. Try again.")
            status = False
        else:
            status = True
            new_balance = float(cardHolder.get_balance()) - float(amount)
            cardHolder.set_balance(new_balance)
            cur_user = SHEET.worksheet("client").find(user[0][0])
            SHEET.worksheet("client").update_cell(cur_user.row, 5, new_balance)
            print("\nSuccessfully withdraw from your account.")
            break
    return True


def show_balance(cardHolder):
    list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
    user = [
        holder
        for holder in list_of_cardHolders
        if cardHolder.get_cardNum() == holder[0]
    ]
    return user[0][4]


def show_user_name(cardHolder):
    list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
    user = [
        holder
        for holder in list_of_cardHolders
        if cardHolder.get_cardNum() == holder[0]
    ]
    return user[0][2]


def main():
    """
    Runs all program functions
    """
    current_user = validate_card_Num()

    validate_user(current_user)
    # print(show_balance(current_user))

    print("\nWelcome ", show_user_name(current_user), " :)")
    option = 0
    while True:
        print_menu()
        try:
            option = int(input())
        except ValueError:
            print("\nInvalid input. Please try again.")
        if option == 1:
            deposit(current_user)
        elif option == 2:
            withdraw(current_user)
        elif option == 3:
            show_balance(current_user)
            print("\nYour current balance is: €", show_balance(current_user))
        elif option == 4:
            break
        else:
            option = 0
    print("𝐓𝐡𝐚𝐧𝐤 𝐲𝐨𝐮. 𝐇𝐚𝐯𝐞 𝐚 𝐧𝐢𝐜𝐞 𝐝𝐚𝐲❗")


main()
