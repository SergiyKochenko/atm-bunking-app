import gspread

from cardHolder import cardHolder

from google.oauth2.service_account import Credentials




SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('client_database')


# client = SHEET.worksheet('client')

# cardNumber = client.col_values(1)
# print(cardNumber)
# pin = client.col_values(2)
# print(pin)
# name = client.col_values(3)
# print(name)
# surename = client.col_values(4)
# print(surename)
# balance = client.col_values(5)
# print(balance)



logo = (
      """
         AAA  TTTTTTTT MM    MM
        AAAAA    TT    MMM  MMM
       AA   AA   TT    MM MM MM
      AAAAAAAAA  TT    MM    MM
     AAA     AAA TT    MM    MM
      """  
  )
print(logo)


def print_menu():
   #Print options to the user
   print("Please chose from one of the follewing options...")
   print("1. Deposit")
   print("2. Withdraw")
   print("3. Show Balance")
   print("4. Exit")

def deposit(cardHolder):
  try:
    deposit = float(input("How much € would you like to deposit:\n "))
    cardHolder.set_balance(cardHolder.get_balance() + deposit)
    print("Thank you for your deposit. Your new balance is: €", str(cardHolder.get_balance()))
  except:
    print("Invalid input")

def withdraw(cardHolder):
  try:
    withdraw = float(input("How much € would you like to withdraw:\n "))
    #Chkesk if user has enough mony
    if(cardHolder.get_balance() < withdraw):
      print("Insufficient balance :(")
    else:
      cardHolder.set_balance(cardHolder.get_balance() - withdraw)
      print("You're good to go! Thank you :)")
  except:
    print("Invalit input")

def check_balance(cardHolder):
  print("Your current balance is: €", cardHolder.get_balance())

# if __name__ == "__main__":
#   current_user = cardHolder("","","","","")

  #Create a repo of cardholders
list_of_cardHolders = SHEET.worksheet('client').get_all_values()[1:]
#   # list_of_cardHolders.append(cardHolder("4532772818527395", 1234, "John", "Griffin", 1050.31))
#   # list_of_cardHolders.append(cardHolder("4532761841325802", 4321, "Emma", "Jones", 500.22))
#   # list_of_cardHolders.append(cardHolder("5128381368581872", 6543, "Flavia", "Jeckson", 150.79))
#   # list_of_cardHolders.append(cardHolder("6011188364697109", 8765, "Kira", "Dopkins", 950.93))
#   # list_of_cardHolders.append(cardHolder("3490693153147110", 2040, "Anna", "Watson", 10.28))


# # get data fro spreadsheet
# data = client.worksheet('client').get_all_values()[1:]
# print(data)
#   #Prompt user for debit card number
#   # debitCardNum = ""
while True:
    try:
      debitCardNum = input("\nPlease insert your debit card: ")
      #Check against repo
      debitMatch = [holder for holder in list_of_cardHolders if debitCardNum == holder[0]]
      if(len(debitMatch) > 0):
        current_user =debitMatch[0]
        break
      else:
        print("Card number not recognized. Please try again.")
    except:
      print("Card number not recognized. Please try again.")

#Prompt for PIN
is_on = True
while is_on:
  try:
    userPin = int(input("\nPlease enter your pin:\n ").strip())
    if userPin == current_user.get_pin():
      is_on = False
    else:
      print("Invalid PIN. Please try again.")
      break
  except:
    print("Invalid PIN. Please try again.")

  #Print options
  print("\nWelcome ", current_user.get_firstName(), " :)")
  option = 0
  while (True):
    print_menu()
    try:
      option = int(input())
    except:
      print("Invalid input. Please try again.")

    if(option == 1):
      deposit(current_user)
    elif(option == 2):
      withdraw(current_user)
    elif(option == 3):
      check_balance(current_user)
    elif(option == 4):
      break
    else:
      option = 0

  print("\nThank you. Have a nice day :)")
  
# data = SHEET.worksheet('client').get_all_values()[1:]
# print(data)
  