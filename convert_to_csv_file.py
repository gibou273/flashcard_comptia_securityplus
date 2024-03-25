with open("data/acronyms.txt", "r") as file:
    content = file.readlines()
    with open("data/acronyms.csv", "a") as myFile:
        for line in content:
            myFile.write(",".join(line.split(" ", 1)))
