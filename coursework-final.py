# Importing Netmiko for telnet and ssh functionality.
import netmiko
# Importing getpass so that the password isn't shown when it's entered into the console
# Similar to sudo prompt in UNIX-Like OSes (Linux, MacOS, BSD etc.)
import getpass

# Initialising "device_info" as a dictionary, this will store all of the information.
device_info = {}
device_info["ip"] = input("Enter the IP address of the device you would like to connect to: ")
device_info["user"] = input("Enter the username: ")
# Using the aforementioned getpass for the secret and the password.
device_info["passwd"] = getpass.getpass(prompt="Enter the password: ")
device_info["secret"] = getpass.getpass(prompt="Enter the secret: ")

# Function for telnet using netmiko, incredibly easy to implement, just provide ConnectHandler
# with information on where it's connecting to and it'll do all the work for you.

def telnet():
    session = netmiko.ConnectHandler(
        device_type="cisco_ios_telnet",
        host=device_info["ip"],
        username=device_info["user"],
        password=device_info["passwd"],
        secret=device_info["secret"]
    )

# If the session is able to find the prompt, it prints "Successfully Connected!"

    if session.find_prompt() != 0:
        print("Successfully Connected!")
    else:
        print("Unable to Connect") 

# Disconnect from the session after connecting.

    session.disconnect()

# This is the function for connecting via SSH, it's incredibly similar to the
# telnet one, the only difference is using (device_type="cisco_ios") rather than
# "cisco_ios_telnet"

def ssh():
    session = netmiko.ConnectHandler(
        device_type="cisco_ios",
        host=device_info["ip"],
        username=device_info["user"],
        password=device_info["passwd"],
        secret=device_info["secret"]        
    )

    if session.find_prompt() != 0:
        print("Successfully Connected!")
    else:
        print("Unable to Connect")

    session.disconnect()

# Most of the code here is also present in the previous two functions, however it's more involved
# since it also has to write the config to a file.

def save_config():

    session = netmiko.ConnectHandler(
        device_type="cisco_ios",
        host=device_info["ip"],
        username=device_info["user"],
        password=device_info["passwd"],
        secret=device_info["secret"]
    )

    if session.find_prompt() != 0:
        print("\nSuccessfully Connected!")
    else:
        print("Unable to Connect")

    session.enable() # This is equivalent to typing "enable" in Cisco IOS, required for "show running-config" to run.

# Saves the entire configuration into this "config" variable.    
    config = session.send_command("show running-config")
	
# Asks for the filename from the username for the saved configuration
    fileName = input("What would you like this configuration file to be called: ")
    fileName += ".txt" # Adds .txt file extension, not really necessarily on Linux but if imported into Windows it's nice.

# Opens the file for writing, writes the configuration into the file, and closes it.
    file = open(fileName, "w")
    file.write(config)
    file.close()

# Confirmation message.
    print("Configuration successfully saved!")
# Disconnecting from the session again.
    session.disconnect()

# Menu system
def menu():
        print("\nWhat would you like to do?")
        print("1: Telnet into the device")
        print("2: SSH into the device")
        print("3: Copy the configuration file from the device")
        print("4: Exit")
        
        choice = input("Choose your option: ")
        
        if choice == "1":
            telnet()
        elif choice == "2":
            ssh()
        elif choice == "3":
            save_config()
        elif choice == "4":
            print("Bye Bye!")
        else:
            print("Invalid Choice")
            menu() # If the choice is invalid, it just runs the menu function again, which brings the menu up again.

menu()
