import netmiko
import getpass

device_info = {}
device_info["ip"] = input("Please enter the IP Address of the Device: ")
device_info["user"] = input("Please enter the Username of the Device: ")
device_info["passwd"] = getpass.getpass(prompt="Enter the password: ")
device_info["secret"] = getpass.getpass(prompt="Enter the secret: ")

def loopbackCommands(config={}):
    commands = [
        "interface loopback {}".format(config["loopbackNum"]),
        "ip address {} {}".format(config["loopbackIP"],config["loopbackSubnet"]),
    ]

    return commands

def loopback(config):
    session =  netmiko.ConnectHandler(
        device_type="cisco_ios",
        host=device_info["ip"],
        username=device_info["user"],
        password=device_info["passwd"],
        secret=device_info["secret"]) 

    if session.find_prompt() != 0:
        print("Successfully Connected!")
    else:
        print("Unable to Connect")
    
    # Converts configuration into commands that the router can use
    commands = loopbackCommands(config)

    # Sends the commands (send_config_set() = configure terminal) 
    session.send_config_set(commands)

    print("Successfully Sent Configuration!")
    loopbackVerify = session.send_command("show running-config | section interface loopback")
    session.disconnect()
    return(loopbackVerify)

def ospfCommands(config):
    commands = [
        "router ospf {}".format(config["ospf_num"]),
        "router-id {}".format(config["router_ip"]),
        "network {} {} area {}".format(config["ospf_ip"],config["ospf_subnet"],config["area_num"]),
        "end"
    ]
    return commands

def eigrpCommands(config):
    commands = [
        "router eigrp {}".format(config["eigrp_name"]),
        "address-family ipv4 autonomous-system {}".format(config["eigrp_fam"]),
        "network {} {} ".format(config["eigrp_ip"],config["eigrp_subnet"]),
        "end"
    ]
    return commands

def ripCommands(config):
    commands = [
        "router rip",
        "network {}".format(config)
    ]
    return commands

def configureProtocol(config,protocol):
    session =  netmiko.ConnectHandler(
        device_type="cisco_ios",
        host=device_info["ip"],
        username=device_info["user"],
        password=device_info["passwd"],
        secret=device_info["secret"]) 

    if session.find_prompt() != 0:
        print("Successfully Connected!")
    else:
        print("Unable to Connect")

    session.enable()
    if protocol.lower() == "ospf":
        commands = ospfCommands(config)
    elif protocol.lower() == "eigrp":
        commands = eigrpCommands(config)
    elif protocol.lower() == "rip":
        commands = ripCommands(config)
    else:
        return("Invalid Protocol")
    

    session.send_config_set(commands)
    print("Successfully sent configuration!")

    
    verification = session.send_command("show running-config | section {}".format(protocol.lower()))
    session.disconnect()
    return(verification)

def menu():
    print("\nWhat would you like to do?")
    print("1: Configure a Loopback Interface")
    print("2: Configure Dynamic Routing Protocol")
    print("3: Sequential Configuration of Network Devices")
    print("4: Exit")
        
    choice = input("Choose your option: ")

    if choice == "1": # Loopback IP Address

        config = {
            "loopbackNum":"0",
            "loopbackIP":"10.0.0.1",
            "loopbackSubnet":"255.255.255.255",
        }

        print("\nDefault Configuration")
        print("Loopback Interface {}\nIP Address: {}\nSubnet Mask: {}".format(config["loopbackNum"],config["loopbackIP"],config["loopbackSubnet"]))
        while True:
            choice = input("\nWould you like to use the default configuration, or manually enter values?\n(D)efault/(M)anual: ")
            
            if choice.lower() == "d":
                break
            if choice.lower() == "m":
                config["loopbackNum"] = input("Enter the Loopback Interface Number: ")
                config["loopbackIP"] = input("Enter the IP Address of the Loopback Interface: ")
                config["loopbackSubnet"] = input("Enter the Subnet Mask: ")
                break
            else: 
                print("Invalid Choice")

        print(loopback(config))
            
    elif choice == "2":
        print("Configurable Protocols")
        print("1: OSPF")
        print("2: EIGRP")
        print("3: RIP")
        print("4: Return to Menu")

        choice = input("Which would you like to configure? ")

        if choice == "1":
            config = {
                "ospf_num": "1",
                "router_ip":device_info["ip"],
                "ospf_ip":"192.168.178.10",
                "ospf_subnet":"0.0.0.3",
                "area_num":"0",
            }
            print("Default Configuration")
            print("\nOSPF Number: ", config["ospf_num"])
            print("Router IP: ", config["router_ip"])
            print("OSPF IP: ", config["ospf_ip"])
            print("OSPF Subnet: ", config["ospf_subnet"])
            print("Area Number: ", config["area_num"])
            
            while True:
                configChoice = input("Would you like to use the default configuration, or manually enter values?\n(D)efault/(M)anual: ")

                if configChoice.lower() == "d":
                    break                                
                elif configChoice.lower() == "m":
                    config["ospf_num"] = input("Please enter the OSPF Number (process-id): ")
                    config["ospf_ip"] = input("Please enter the IP to use with OSPF: ")
                    config["ospf_subnet"] = input("Please enter the Subnet Mask: ")
                    config["area_num"] = input("Please enter the area number: ")
                    break
                else:
                    print("Invalid Choice")
            
            print(configureProtocol(config,"ospf"))

        elif choice == "2":
            config = {
                "eigrp_name": "eigrp1",
                "eigrp_ip":"192.168.122.10",
                "eigrp_subnet":"0.0.0.3",
                "eigrp_fam":"1",
            }
            print("Default Configuration")
            print("\nEIGRP Name: ", config["eigrp_name"])
            print("EIGRP IP: ", config["eigrp_ip"])
            print("EIGRP Subnet: ", config["eigrp_subnet"])
            print("EIGRP Family: ", config["eigrp_fam"])

            while True:
                configChoice = input("Would you like to use the default configuration, or manually enter values?\n(D)efault/(M)anual: ")

                if configChoice.lower() == "d":
                    break
                elif configChoice.lower() == "m":
                    config["eigrp_name"] = input("Please enter the EIGRP Name: ")
                    config["eigrp_ip"] = input("Please enter the IP to use with EIGRP: ")
                    config["eigrp_subnet"] = input("Please enter the Subnet Mask: ")
                    config["eigrp_fam"] = input("Please enter the family number: ")
                    break
                else:
                    print("Invalid Choice")
            print(configureProtocol(config,"eigrp"))

        elif choice == "3":
            config = "192.168.43.0"

            print("Default Configuration")
            print("RIP IP: ", config)

            while True:
                configChoice = input("Would you like to use the default configuration, or manually enter values?\n(D)efault/(M)anual: ")

                if configChoice.lower() == "d":
                    break
                elif configChoice.lower() == "m":
                    config = input("Please enter the IP to use with RIP: ")
                    break
                else:
                    print("Invalid Choice")

            print(configureProtocol(config,"rip"))

        elif choice == "4": # Return to Menu
            menu()

    elif choice == "3": # Exit from Program
        print("Bye Bye!")
    else:
        menu()

menu()