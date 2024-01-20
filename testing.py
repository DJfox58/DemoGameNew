saveFile = open("save1.txt", "r")

babo = saveFile.readlines()

saveFile.close()

listToType = ["fifty 6", "forutnee 1"]
saveFile = open("save1.txt", "w")

for item in listToType:
    saveFile.write(item + "\n")


saveFile.close()

print("BABO")
print(babo)
