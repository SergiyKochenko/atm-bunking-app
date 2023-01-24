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

client = SHEET.worksheet('client')

cardNumber = client.col_values(1)
# print(cardNumber)
pin = client.col_values(2)
# print(pin)
name = client.col_values(3)
# print(name)
surename = client.col_values(4)
# print(surename)
balance = client.col_values(5)
# print(balance)
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


def deposit(cardHolder):
  try:
    deposit = float(input("How much € would you like to deposit: "))
    cardHolder.set_balance(cardHolder.get_balance() + deposit)
    message = "Thank you for your deposit. Your new balance is: €"
    print(message, str(cardHolder.get_balance()))
  except ValueError():
    print("Invalid input")


def withdraw(cardHolder):
  try:
    withdraw = float(input("How much € would you like to withdraw: "))
    # Check if user has enough money
    if (cardHolder.get_balance() < withdraw):
      print("Insufficient balance :(")
    else:
      cardHolder.set_balance(cardHolder.get_balance() - withdraw)
      print("You're good to go! Thank you :)")
  except ValueError():
    print("Invalit input")


def check_balance(cardHolder):
  print("Your current balance is: €", cardHolder.get_balance())


if __name__ == "__main__":
  current_user = cardHolder("", "", "", "", "")

  # Create a repo of cardholders
  list_of_cardHolders = []
  list_of_cardHolders.append(cardHolder("4532772818527395", 1234, "John", "Griffin", 1050.30))
  list_of_cardHolders.append(cardHolder("4532761841325802", 4321, "Emma", "Jones", 500.22))
  list_of_cardHolders.append(cardHolder("5128381368581872", 6543, "Flavia", "Jeckson", 150.79))
  list_of_cardHolders.append(cardHolder("6011188364697109", 8765, "Kira", "Dopkins", 950.93))
  list_of_cardHolders.append(cardHolder("3490693153147110", 2040, "Anna", "Watson", 10.28))

  # Prompt user for debit card number
  debitCardNum = ""
  while True:
    try:
      debitCardNum = input("\n𝐏𝐥𝐞𝐚𝐬𝐞 𝐢𝐧𝐬𝐞𝐫𝐭 𝐲𝐨𝐮𝐫 𝐝𝐞𝐛𝐢𝐭 𝐜𝐚𝐫𝐝: ")
      # Check against repo
      debitMatch = [holder for holder in list_of_cardHolders if holder.cardNum == debitCardNum]
      if (len(debitMatch) > 0):
        current_user = debitMatch[0]
        break
      else:
        print("Card number not recognized. Please try again.")
    except ValueError():
      print("Card number not recognized. Please try again.")

  # Prompt for PIN
  is_on = True
  while is_on:
    try:
      userPin = int(input("\n𝗣𝗹𝗲𝗮𝘀𝗲 𝗲𝗻𝘁𝗲𝗿 𝘆𝗼𝘂𝗿 𝗣𝗜𝗡: ").strip())
      if (current_user.get_pin() == userPin):
        is_on = False
      else:
        print("Invalid PIN. Please try again.")
        break
    except ValueError():
      print("Invalid PIN. Please try again.")

  # Print options
  print("\nWelcome ", current_user.get_firstName(), " :)")
  option = 0
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
