"""
TO DO LIST:
1) Add Functionality to actually save the config file
2) Add password verification
3) Comment and clean up code
4) Find more efficient ways to do things (menuLoop etc.)
"""
# Importing Netmiko for telnet and ssh functionality.
import netmiko
# Importing getpass so that the password isn't shown when it's entered into the console
# Similar to sudo prompt in UNIX-Like OSes (Linux, MacOS, BSD etc.)
import getpass

device_info = {}

device_info["ip"] = input("Enter the IP address of the device you would like to connect to: ")
device_info["user"] = input("Enter the username: ")
device_info["passwd"] = getpass.getpass(prompt="Enter the password: ")

def telnet():
    session = netmiko.ConnectHandler(
        device_type="cisco_ios_telnet",
        host=device_info["ip"],
        username=device_info["user"],
        password=device_info["passwd"],
    )

    if session.find_prompt() != 0:
        print("Successfully Connected!")
    else:
        print("Unable to Connect")

    session.disconnect()

def ssh():
    session = netmiko.ConnectHandler(
        device_type="cisco_ios",
        host=device_info["ip"],
        username=device_info["user"],
        password=device_info["passwd"],
    )

    if session.find_prompt() != 0:
        print("Successfully Connected!")
    else:
        print("Unable to Connect")

    session.disconnect()

def save_config():
    menuLoop = 0
    while menuLoop == 0:
        connect_type = input("\nNote: Telnet is insecure and will send your config over cleartext!!!\nHow would you like to connect? (ssh/telnet): ")
        if connect_type == "ssh":
            connect_type = "cisco_ios"
            menuLoop += 1
        elif connect_type == "telnet":
            connect_type = "cisco_ios_telnet"
            menuLoop += 1
        else:
            print("Invalid Choice")
            menuLoop = 0

    session = netmiko.ConnectHandler(
        device_type=connect_type,
        host=device_info["ip"],
        username=device_info["user"],
        password=device_info["passwd"],
    )

    if session.find_prompt() != 0:
        print("\nSuccessfully Connected!")
    else:
        print("Unable to Connect")
	
	print(session.send_command('show running-show'))
	
    session.disconnect()

def menu():
    menuLoop = 0
    while menuLoop == 0:
        print("\nWhat would you like to do?")
        print("1: Telnet into the device")
        print("2: SSH into the device")
        print("3: Copy the Configuration File from the device")
        print("4: Exit")
        choice = input("Choose your option: ")
        if choice == "1":
            telnet()
            menuLoop += 1
        elif choice == "2":
            ssh()
            menuLoop += 1
        elif choice == "3":
            save_config()
            menuLoop += 1
        elif choice == "4":
            menuLoop += 1
        else:
            print("Invalid Choice")
            menuLoop = 0
