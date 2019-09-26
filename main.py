import json
import subprocess

def replace_items(output, json_data):
    for item in json_data:

        with open("templates/" + str(item["component_name"]), 'r') as component:
            del item["component_name"]

            for line in component:
                for src, target in item.items():
                    if isinstance(target, str):
                        line = line.replace("{{" + src + "}}", target)
                    else:
                        match = "[[" + src + "]]"
                        index = line.find(match)

                        if index >-1:
                            output.write(line[:index])
                            replace_items(output, item[src])

                            line = line.replace(match, "")
                            line = line[index:]

                    #print(line + "\n")
                line += "\n"
                output.write(line)

# Adds the preamble to the new latex file
output = open("output.tex", 'w')
LaTeXpreamble = open("templates/preamble.tex", 'r')
output.write(LaTeXpreamble.read())
#output.close()

#Opens the file for rewriting in append to not overwrite preamble
#output = open("output.tex", 'a')

json_file = open("data.json", 'r')
json_data = json.load(json_file)

replace_items(output, json_data)

output.close()
