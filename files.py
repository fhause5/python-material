from flask import Flask

inputfile = "./files/names.txt"
outputfile = "./files/output.txt"

myfile1 = open(inputfile, mode='r', encoding='latin_1')
myfile2 = open(outputfile, mode='w', encoding='latin_1')

# Add number print one person
for number, line in enumerate(myfile1, 1):
    if "Pablo" in line:
        print("Number " + str(number) + " " + line.strip())
        heis = ("Number " + str(number) + " " + line.strip())

myfile2.write("Has founded in the file " + heis )
myfile2.close
myfile1.close
