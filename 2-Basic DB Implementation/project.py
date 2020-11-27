import os
import argparse

parser = argparse.ArgumentParser(description="Storage Management System")
parser.add_argument("line", metavar="Operation Line", nargs='*', type=str)

args = parser.parse_args()




def create_type(type_name, field_names):

    catalogue = open("SystemCatalogue.txt", "r")
    catalogue_header_line = catalogue.readline()
    catalogue_header = catalogue_header_line.split(' ')
    catalogue_header = [int(i) for i in catalogue_header]

    if len(type_name)>catalogue_header[0] :
        print("error occured: typeName is too long")
        return
    elif len(field_names)>catalogue_header[2]:
        print("error occured: there is too much fields")
        return
    else:
        is_in = False
        lines = []
        for line in catalogue.readlines():
            splitted_line = line.split()
            if len(splitted_line) < 1:
                print("error occured: System Catalogue has been corrupted")
                return
            if splitted_line[0] == type_name:
                if splitted_line[3] == "True":
                    is_in = True
                    splitted_line[1] = type_name+".txt"
                    new_file = open(splitted_line[1], "w+")
                    new_file.write("Null False 0 0")
                    splitted_line[2] = len(field_names)
                    splitted_line[3] = "False"
                    line4 = ''
                    for i in field_names:
                        if line4 == '':
                            line4 = str(i)
                        else:
                            line4 = line4 + ' ' + str(i)
                    splitted_line[4] = line4
                    splitted_line = splitted_line[0:5]
                    new_line = ''
                    for i in splitted_line:
                        if new_line == '':
                            new_line = str(i)
                        else:
                            new_line = new_line + ' ' + str(i)
                    lines.append(new_line+'\n')
                else:
                    print("error occured: a type with typeName already exists")
                    return
            else:
                lines.append(line)

        if not is_in:
            catalogue.close()

            catalogue = open("SystemCatalogue.txt", "a")
            line = '\n'+ type_name + ' ' + type_name + '.txt ' + str(len(field_names)) + ' False'
            new_file = open(type_name+".txt", "w+")
            new_file.write("Null False 0 0")
            for i in field_names:
                line = line + ' ' + i
            catalogue.write(line)

        else:
            catalogue.close()

            catalogue = open("SystemCatalogue.txt", "w")
            catalogue.write(catalogue_header_line)
            for line in range(len(lines)):
                if line == len(lines)-1:
                    catalogue.write(lines[line].rstrip("\n"))
                else:
                    catalogue.write(lines[line])


def delete_type(type_name):
    catalogue = open("SystemCatalogue.txt", "r")
    catalogue_header_line = catalogue.readline()
    catalogue_header = catalogue_header_line.split(' ')
    catalogue_header = [int(i) for i in catalogue_header]

    if len(type_name)>catalogue_header[0] :
        print("error occured: typeName is too long")
        return
    else:
        is_in = False
        lines = []
        for line in catalogue.readlines():
            splitted_line = line.split()
            if len(splitted_line) < 1:
                print("error occured: System Catalogue has been corrupted")
                return

            if splitted_line[0] == type_name:
                is_in = True
                if splitted_line[3] == "True":
                    print("error occured: the "+type_name +" already deleted")
                    return
                else:
                    new_line = splitted_line[0] + ' deleted 0 True Empty\n'
                    lines.append(new_line)
            else:
                lines.append(line)

        catalogue.close()

        if is_in:
            catalogue = open("SystemCatalogue.txt", "w")
            catalogue.write(catalogue_header_line)
            for line in range(len(lines)):
                if line == len(lines) - 1:
                    catalogue.write(lines[line].rstrip("\n"))
                else:
                    catalogue.write(lines[line])
            if os.path.exists(type_name+".txt"):
                os.remove(type_name+".txt")
        else:
            print("error occured: there is no Type named " + type_name)


def list_types():
    catalogue = open("SystemCatalogue.txt", "r")
    catalogue_header_line = catalogue.readline()
    for line in catalogue.readlines():
        split_line = line.split(' ')
        output = "typeName= " + split_line[0] + " typeAdress= " + split_line[1] + " numOfFields= " +str(split_line[2])
        output = output + " isDeleted= " + split_line[3] + " keyName= " + split_line[4].rstrip("\n") + " fieldNames="
        for field in split_line[4:]:
            output = output + " " + field.rstrip("\n")
        print(output)

def create_record(type_name, field_values):
    catalogue = open("SystemCatalogue.txt", "r")
    catalogue_header_line = catalogue.readline()
    catalogue_header = catalogue_header_line.split(' ')
    catalogue_header = [int(i) for i in catalogue_header]

    if len(type_name) > catalogue_header[0]:
        print("error occured: typeName is too long")
        return
    else:
        done = False
        nth_type = []
        total = []

        for line in catalogue.readlines():
            nth_type = line.split(' ')
            if nth_type[0] == type_name:
                page_pointer = nth_type[1]
                page = open(page_pointer, "r")


                while not done:
                    page_header = page.readline()
                    total.append(page_header)
                    header_index = len(total)-1
                    split_page_header = page_header.split(' ')
                    single_page = page.read(int(split_page_header[2]))

                    while split_page_header[1] == "True":
                        for page_line in single_page.split('\n'):
                            if page_line.split(' ')[0] == "False" and page_line.split(' ')[2] == field_values[0]:
                                print("error occured: there is a record with key value", field_values[0], "already")
                                return
                            elif page_line.split(' ')[0] == "True" and page_line.split(' ')[2] == field_values[0]:
                                old_size = int(page_line.split(' ')[1])
                                size_total = 0
                                for f in field_values:
                                    size_total = size_total + len(f)
                                size_total = size_total + 7 + len(field_values)
                                string_length_of_size = len(str(size_total))
                                size_total = size_total + string_length_of_size
                                new_string_length_of_size = len(str(size_total))
                                if string_length_of_size != new_string_length_of_size:
                                    size_total = size_total + 1
                                page_line = "False " + str(size_total)
                                for f in field_values:
                                    page_line = page_line + " " + f
                                done = True

                                page_size = int(split_page_header[2]) + size_total - old_size
                                total[header_index] = split_page_header[0] + " True " + str(page_size)


                            if len(page_line) > 0:
                                total.append(page_line)

                        page_header = page.readline()
                        total.append(page_header)
                        header_index = len(total) - 1
                        split_page_header = page_header.split(' ')
                        single_page = page.read(int(split_page_header[2]))

                    for page_line in single_page.split('\n'):
                        create_header = False
                        created_header = ""
                        if page_line.split(' ')[0] == "False" and page_line.split(' ')[2] == field_values[0]:
                            print("error occured: there is a record with key value", field_values[0], "already")
                            return
                        elif page_line.split(' ')[0] == "True" and page_line.split(' ')[2] == field_values[0]:
                            old_size = int(page_line.split(' ')[1])
                            size_total = 0
                            for f in field_values:
                                size_total = size_total + len(f)
                            size_total = size_total + 7 + len(field_values)
                            string_length_of_size = len(str(size_total))
                            size_total = size_total + string_length_of_size
                            new_string_length_of_size = len(str(size_total))
                            if string_length_of_size != new_string_length_of_size:
                                size_total = size_total + 1
                            page_line = "False " + str(size_total)
                            for f in field_values:
                                page_line = page_line + " " + f
                            done = True

                            page_size = int(split_page_header[2]) + size_total - old_size
                            if page_size > 200:
                                total[header_index] = str(page_size) + " True " + str(page_size)
                                created_header = "Null False 0"
                                create_header = True
                            else:
                                total[header_index] = "Null False " + str(page_size)

                        if len(page_line) > 0:
                            total.append(page_line)
                        if create_header:
                            total.append(created_header)


                    if not done:
                        create_header = False
                        created_header = ""
                        size_total = 0
                        for f in field_values:
                            size_total = size_total + len(f)
                        size_total = size_total + 7 + len(field_values)
                        string_length_of_size = len(str(size_total))
                        size_total = size_total + string_length_of_size
                        new_string_length_of_size = len(str(size_total))
                        if string_length_of_size != new_string_length_of_size:
                            size_total = size_total + 1
                        page_line = "False " + str(size_total)
                        for f in field_values:
                            page_line = page_line + " " + f
                        done = True
                        total.append(page_line)

                        page_size = int(split_page_header[2]) + size_total

                        if page_size > 200:
                            total[header_index] = str(page_size) + " True " + str(page_size)
                            create_header = True
                            created_header = "Null False 0"
                        else:
                            total[header_index] = "Null False " + str(page_size)

                        if create_header:
                            total.append(created_header)


                if done:
                    for lines in page.readlines():
                        total.append(lines)

                    catalogue.close()
                    page.close()
                    new_page = open(page_pointer, "w")

                    for i, result_line in enumerate(total):
                        if i == len(total) - 1:
                            new_page.write(result_line)
                        else:
                            new_page.write(result_line.rstrip('\n')+'\n')



def delete_record(type_name, key_value):
    catalogue = open("SystemCatalogue.txt", "r")
    catalogue_header_line = catalogue.readline()
    catalogue_header = catalogue_header_line.split(' ')
    catalogue_header = [int(i) for i in catalogue_header]

    if len(type_name) > catalogue_header[0]:
        print("error occured: typeName is too long")
        return
    else:
        done = False
        nth_type = []
        total = []

        for line in catalogue.readlines():
            nth_type = line.split(' ')
            if nth_type[0] == type_name:
                page_pointer = nth_type[1]
                page = open(page_pointer, "r")

                while not done:
                    page_header = page.readline()
                    total.append(page_header)
                    header_index = len(total)-1
                    split_page_header = page_header.split(' ')
                    single_page = page.read(int(split_page_header[2]))

                    while split_page_header[1] == "True":
                        for page_line in single_page.split('\n'):
                            if page_line.split(' ')[0] == "False" and page_line.split(' ')[2] == key_value:

                                old_size = int(page_line.split(' ')[1])
                                size_total = 7 + len(key_value)
                                string_length_of_size = len(str(size_total))
                                size_total = size_total + string_length_of_size
                                new_string_length_of_size = len(str(size_total))
                                if string_length_of_size != new_string_length_of_size:
                                    size_total = size_total + 1
                                page_line = "True "+ str(size_total) + " " +key_value
                                done = True


                                page_size = int(split_page_header[2]) + size_total - old_size
                                total[header_index] = split_page_header[0] + " True " + str(page_size)


                            elif page_line.split(' ')[0] == "True" and page_line.split(' ')[2] == key_value:
                                print("error occured: the record already deleted")
                                return


                            if len(page_line) > 0:
                                total.append(page_line)

                        page_header = page.readline()
                        total.append(page_header)
                        header_index = len(total) - 1
                        split_page_header = page_header.split(' ')
                        single_page = page.read(int(split_page_header[2]))

                    for page_line in single_page.split('\n'):
                        create_header = False
                        created_header = ""
                        if page_line.split(' ')[0] == "False" and page_line.split(' ')[2] == key_value:

                            old_size = int(page_line.split(' ')[1])
                            size_total = 7 + len(key_value)
                            string_length_of_size = len(str(size_total))
                            size_total = size_total + string_length_of_size
                            new_string_length_of_size = len(str(size_total))
                            if string_length_of_size != new_string_length_of_size:
                                size_total = size_total + 1
                            page_line = "True " + str(size_total) + " " + key_value
                            done = True

                            page_size = int(split_page_header[2]) + size_total - old_size
                            total[header_index] = "Null False " + str(page_size)


                        elif page_line.split(' ')[0] == "True" and page_line.split(' ')[2] == key_value:
                            print("error occured: the record already deleted")
                            return


                        if len(page_line) > 0:
                            total.append(page_line)

                if done:
                    for lines in page.readlines():
                        total.append(lines)

                    catalogue.close()
                    page.close()
                    new_page = open(page_pointer, "w")

                    for i, result_line in enumerate(total):
                        if i == len(total) - 1:
                            new_page.write(result_line)
                        else:
                            new_page.write(result_line.rstrip('\n')+'\n')
                else:
                    print("error occured: there is no record with the key value", key_value)
                    return


def search_record(type_name, key_value):
    catalogue = open("SystemCatalogue.txt", "r")
    catalogue_header_line = catalogue.readline()
    catalogue_header = catalogue_header_line.split(' ')
    catalogue_header = [int(i) for i in catalogue_header]

    if len(type_name) > catalogue_header[0]:
        print("error occured: typeName is too long")
        return
    else:
        done = False
        nth_type = []
        found_type = False
        found_record = []

        for line in catalogue.readlines():
            nth_type = line.split(' ')
            if nth_type[0] == type_name:
                found_type = True
                page_pointer = nth_type[1]
                page = open(page_pointer, "r")

                while not done:
                    page_header = page.readline()
                    split_page_header = page_header.split(' ')
                    single_page = page.read(int(split_page_header[2]))

                    while split_page_header[1] == "True":
                        for page_line in single_page.split('\n'):
                            if page_line.split(' ')[0] == "False" and page_line.split(' ')[2] == key_value:
                                found_record = page_line.split(' ')
                                done = True
                                break
                            elif page_line.split(' ')[0] == "True" and page_line.split(' ')[2] == key_value:
                                print("error occured: the record already deleted")
                                return


                        page_header = page.readline()
                        split_page_header = page_header.split(' ')
                        single_page = page.read(int(split_page_header[2]))

                    for page_line in single_page.split('\n'):
                        if page_line.split(' ')[0] == "False" and page_line.split(' ')[2] == key_value:
                            found_record = page_line.split(' ')
                            done = True
                            break
                        elif page_line.split(' ')[0] == "True" and page_line.split(' ')[2] == key_value:
                            print("error occured: the record already deleted")
                            return


                if done:
                    output = ""
                    output = str(type_name)+ " key->"
                    field_names = nth_type[4:]
                    field_values = found_record[2:]
                    for i in range(len(field_names)):
                        output = str(output) + " " + str(field_names[i]) + " = " + str(field_values[i])
                    print(output)
                else:
                    print("error occured: there is no record with the key value", key_value)
                    return


        if not found_type:
            print("error occured: there is no type named", type_name)


def list_all_records(type_name):
    catalogue = open("SystemCatalogue.txt", "r")
    catalogue_header_line = catalogue.readline()
    catalogue_header = catalogue_header_line.split(' ')
    catalogue_header = [int(i) for i in catalogue_header]

    if len(type_name) > catalogue_header[0]:
        print("error occured: typeName is too long")
        return
    else:
        found_type = False
        found_record = []
        records = []
        for line in catalogue.readlines():
            nth_type = line.split(' ')
            if nth_type[0] == type_name:
                found_type = True
                page_pointer = nth_type[1]
                page = open(page_pointer, "r")

                page_header = page.readline()
                split_page_header = page_header.split(' ')
                single_page = page.read(int(split_page_header[2]))

                while split_page_header[1] == "True":
                    for page_line in single_page.split('\n'):
                        if page_line.split(' ')[0] == "False":
                            found_record = page_line.split(' ')
                            records.append(found_record)

                    page_header = page.readline()
                    split_page_header = page_header.split(' ')
                    single_page = page.read(int(split_page_header[2]))

                for page_line in single_page.split('\n'):
                    if page_line.split(' ')[0] == "False":
                        found_record = page_line.split(' ')
                        records.append(found_record)



        if not found_type:
            print("error occured: there is no type named", type_name)
            return

        for element in records:
            output = ""
            output = str(type_name)+ " key->"
            field_names = nth_type[4:]
            field_values = element[2:]
            for i in range(len(field_names)):
                output = str(output) + " " + str(field_names[i]) + " = " + str(field_values[i])
            print(output)


def main():
    line = args.line
    operation = line[0]
    if operation == "createType":
        print("creating type")
        create_type(line[1], line[2:len(line)])
    elif operation == "deleteType":
        print("deleting type")
        delete_type(line[1])
    elif operation == "listAllTypes":
        print("listing all the types")
        list_types()
    elif operation == "createRecord":
        print("creating record")
        create_record(line[1], line[2:len(line)])
    elif operation == "deleteRecord":
        print("deleting record")
        delete_record(line[1], line[2])
    elif operation == "searchRecord":
        print("searching record")
        search_record(line[1], line[2])
    elif operation == "listAllRecords":
        print("listing all the records of a type")
        list_all_records(line[1])


main()