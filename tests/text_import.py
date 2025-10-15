with open("ral.txt", mode='r') as ral_table:
    colors_list = []
    for line in ral_table:
        print(line)
        splitted = line.split(';')
        color_list = (splitted[0], splitted[1], splitted[2], splitted[3].replace('\n', ''))
        colors_list.append(color_list)

print('---')
print(colors_list)