import pickle

if __name__ == "__main__":
    server = ""
    while server != "q":
        server = input("What is the name of the server you will be counting? ").lower()

        try:
            chatlog = open("{}_chatlog.txt".format(server),"r")
        except FileNotFoundError:
            if server != "q":
                print("That server doesn't exist.")
            chatlog = ""
        try:
            message_amount = pickle.load(open("{}_messages.txt".format(server),"rb"))
        except FileNotFoundError:
            message_amount = {"barry chuckle bot":0}
    
        for line in chatlog:
            if line[0] == "[":
                line = line.strip()
                name = ""
                name_start = line.find("]")+1
                name_end = line.find(":",19)
                for i in range(name_start, name_end):
                    name += line[i]
                name = name.lower()
                print(name)
                try:
                    message_amount[name] += 1
                except KeyError:
                    message_amount[name] = 1

        if chatlog != "":
            print(message_amount)
            pickle.dump(message_amount, open("{}_messages.txt".format(server),"wb"))
