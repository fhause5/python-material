import json
outputjson = "./files/outjson.txt"
output = open(outputjson, mode = 'w', encoding = 'Latin-1')

script = {
    'name': 'ihor',
    'job': 'devops',
    'company': 'epam'
}

combine = []
combine.append(script)

json.dump(combine, output)
output.close()
