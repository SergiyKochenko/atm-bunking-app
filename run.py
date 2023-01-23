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


  # print("Your current balance is: €", current_user[-1])

# if __name__ == "__main__":
#   current_user = cardHolder("","","","","")

def validate_card_Num():
  list_of_cardHolders = SHEET.worksheet('client').get_all_values()[1:]
  while True:
    try:
      debitCardNum = input("\nPlease insert your debit card: ")
        #Check against repo
      debitMatch = [holder for holder in list_of_cardHolders if debitCardNum == holder[0]]
      if(len(debitMatch) > 0):
        break
      else:
        print("Card number not recognized. Please try again.")
    except:
        print("Card number not recognized. Please try again.")
    return cardHolder(debitMatch[0][0],debitMatch[0][1], debitMatch[0][2], debitMatch[0][3], debitMatch[0][4])

  def validate_user(cardHolder):    
    while True:
      try:
        userPin = input("\nPlease enter your pin:\n ").strip()
        if userPin.isnumeric() and userPin == cardHolder.get_cardNum():
          break
        else:
          print("Invalid PIN. Please try again.")
      except:
        print("Invalid PIN. Please try again.")
    print("\nWelcome ", current_user[2], " :)")
    #   try:
    #     userPin = input("\nPlease enter your pin:\n ").strip()
    #     if userPin.isnumeric() and userPin == current_user.get_pin():
    #       break
    #     else:
    #       print("Invalid PIN. Please try again.")
    #   except:
    #       print("Invalid PIN. Please try again.")
    # print("\nWelcome ", current_user[2], " :)")

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
  list_of_cardHolders = SHEET.worksheet('client').get_all_values()[1:]
  current_user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
  print(f"Your balance is {current_user[-1]}")
# # get data fro spreadsheet
# data = client.worksheet('client').get_all_values()[1:]
# print(data)
#   #Prompt user for debit card number
#   # debitCardNum = ""
current_user = validate_card_Num()
validate_user(current_user)
# option = 0
while (True):
  print_menu()
  try:
    option = int(input())
  except:
    print("Invalid input. Please try again.")

    if (option == 1):
      deposit(current_user)
    elif (option == 2):
      withdraw(current_user)
    elif (option == 3):
      check_balance(current_user)
    elif (option == 4):
      break
    else:
      option = 0

print("\nThank you. Have a nice day :)")
  
# data = SHEET.worksheet('client').get_all_values()[1:]
# print(data)
  