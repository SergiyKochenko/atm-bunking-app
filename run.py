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
  print("\nPlease chose from one of the follewing options...")
  print("1. Deposit")
  print("2. Withdraw")
  print("3. Show Balance")
  print("4. Exit")

def validate_card_Num():
    list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
    while True:
      card_num = input("\nEnter card number: ")
      user = [ holder for holder in list_of_cardHolders if card_num == holder[0]]
      if card_num and len(user) > 0:
        break
      elif not card_num:
        print("Please enter card number")
      else:
        print("Card number not recognized")
    return cardHolder(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4])

def validate_user(cardHolder):
  list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
  user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
  tries = 0
  while tries < 3:
    tries += 1
    pin_code = input("\nEnter PIN: ")
    if not pin_code:
      print("please enter pin, try again")
      status = False
    elif not pin_code.isnumeric():
      print("Only numbers allowed")
      status = False
    elif pin_code.isnumeric() and pin_code == user[0][1]:
      status = True
      break
    elif tries == 3:
      print("Sorry you've exceede you trial limit")
      status = False
      break
    else:
      print("Incorrect pin.")
      status = False
    
  return status


def deposit(cardHolder):
  list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
  user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
  while True:
    amount = input("How much € would you like to deposit: ")
    if not amount:
      print("Please enter an amount, try again.")
      status = False
    elif not amount.isnumeric():
      print("Enter only amount in figures.")
      status = False
    else:
      status = True
      new_balance = float(cardHolder.get_balance()) + float(amount)
      cardHolder.set_balance(new_balance)
      cur_user = SHEET.worksheet('client').find(user[0][0])
      SHEET.worksheet('client').update_cell(cur_user.row, 5, new_balance)
      print("\nSuccessfully deposited to your account.")
      break
  return True

def withdraw(cardHolder):
  list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
  user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
  while True:
    amount = input("Enter amount: ")
    if not amount:
      print("Please enter an amount you would like to withdraw, try again.")
      status = False
    elif not amount.isnumeric():
      print("Enter only amount in figures.")
      status = False
    elif float(cardHolder.get_balance()) < float(amount):
      print("Insoffician balance. Try again.")
      status = False

    else:
      status = True
      new_balance = float(cardHolder.get_balance()) - float(amount)
      cardHolder.set_balance(new_balance)
      cur_user = SHEET.worksheet('client').find(user[0][0])
      SHEET.worksheet('client').update_cell(cur_user.row, 5, new_balance)
      print("Successfully withdraw from your account.")
      break
  return True


def show_balance(cardHolder):
  list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
  user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
  return user[0][4]

def show_user_name(cardHolder):
  list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
  user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
  return user[0][2]

current_user = validate_card_Num()

print(validate_user(current_user))
print(show_balance(current_user))



print("\nWelcome ", show_user_name(current_user), " :)")
option = 0
while True:
    print_menu()
    try:
        option = int(input())
    except ValueError:
        print("Invalid input. Please try again.")
    if option == 1:
        deposit(current_user)
    elif option == 2:
        withdraw(current_user)
    elif option == 3:
        show_balance(current_user)
        print("Your current balance is: €", show_balance(current_user))
    elif option == 4:
        break
    else:
        option = 0
print("\nThank you. Have a nice day :)")
