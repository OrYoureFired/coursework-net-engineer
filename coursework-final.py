# Importing Netmiko for telnet and ssh functionality.
import netmiko
# Importing getpass so that the password isn't shown when it's entered into the console
# Similar to sudo prompt in UNIX-Like OSes (Linux, MacOS, BSD etc.)
import getpass
# Library to get the difference between 2 files (required by task 2)
import difflib
import pprint
# Initialising "device_info" as a dictionary, this will store all of the information.
device_info = {}
device_info["ip"] = input("Enter the IP address of the device you would like to connect to: ")
device_info["user"] = input("Enter the username: ")
# Using the aforementioned getpass for the secret and the password.
device_info["passwd"] = getpass.getpass(prompt="Enter the password: ")
device_info["secret"] = getpass.getpass(prompt="Enter the secret: ")

# Function for telnet using netmiko, incredibly easy to implement, just provide ConnectHandler
# with information on where it's connecting to and it'll do all the work for you.
# The connection_type variable is passed through the menu, and determines whether to use
# Telnet or SSH. These used to be 2 separate function but it was trivial to combine them
# into just one.

def connection(connection_type): 
    session = netmiko.ConnectHandler(
        device_type=connection_type,
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

# Most of the code here is also present in the previous function, 
# however it's more involved since it also has to write the config to a file.

def return_configs():

    session = netmiko.ConnectHandler(
        device_type="cisco_ios",
        host=device_info["ip"],
        username=device_info["user"],
        password=device_info["passwd"],
        secret=device_info["secret"]
    )
    if session.find_prompt != 0:
        print("Successfully Connected!")
    else:
        print("Unable to connect")


    session.enable() # This is equivalent to typing "enable" in Cisco IOS, required for "show running-config" to run.
    
    # Saves both configs into variables
    run_config = session.send_command("show running-config")
    start_config = session.send_command("show startup-config")

    # And puts those variables into a list, that will be returned.
    configs = [run_config, start_config]

    # Disconnect from the router
    session.disconnect()

    # This will return a list, containing the run and start config (in that order)
    # Very convienient for task 2.
    return(configs) 

# Menu system
def menu():
        print("\nWhat would you like to do?")
        print("1: Telnet into the device")
        print("2: SSH into the device")
        print("3: Copy the configuration file from the device")
        print("4: Compare running-config with startup-config")
        print("5: Compare running-config with local backup")
        print("6: Exit")
        
        
        choice = input("Choose your option: ")
        
        if choice == "1":
            connection("cisco_ios_telnet") # Passes the string required to telnet into the device.
        elif choice == "2":
            connection("cisco_ios") # Passes the string required to SSH
        elif choice == "3":
            # This used to be part of a "save_config()" function, however I removed the save functionality
            # and implemented it within the if statement itself, in order to use the return_config function for more things
            print("Which Configuration would you like to save?")
            decision = input("Running or Startup? (R/S): ")
            # This will ask whether the user would like to save to running or startup configuration
            if decision == "r" or decision == "R":
                both_configs = return_configs() # Takes the list that is returned, and sets the chosen config to another variable to be manipulated.
                config = both_configs[0]
            elif decision == "s" or decision == "S":
                both_configs = return_configs()
                config = both_configs[1]
            else:
                print("\nInvalid Choice, Going back to Menu")
                menu()
                
            # Asks for the filename from the username for the saved configuration
            fileName = input("What would you like this configuration file to be called: ")
            fileName += ".txt" # Adds .txt file extension, not really necessarily on Linux but if imported into Windows it's nice.
            
            # Opens the file for writing, writes the configuration into the file, and closes it.
            file = open(fileName, "w")
            file.write(config)
            file.close()

            # Confirmation message.
            print("Configuration successfully saved!")

        elif choice == "4":

            configs = return_configs()
            run_config = configs[0].split('\n')
            start_config = configs[1].split('\n')

            for diff in difflib.unified_diff(run_config,start_config):
                print(diff.strip(" "))
            print("\nChanges with - are present in running-config\nChanges with + are present in startup-config\nLines with no symbol are the same.")

            decision = input("Would you like to save these changes in a file? (y/n): ")



        elif choice == "5":
            print("Compare run with local") # Placeholder
        elif choice == "6":
            print("Bye Bye!") # Passes no functions, ending the program.
        else:
            print("Invalid Choice")
            menu() # If the choice is invalid, it just runs the menu function again, which brings the menu up again.

menu()
