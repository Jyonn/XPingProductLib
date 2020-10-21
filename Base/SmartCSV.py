import csv
import codecs


def smart_csv(filename, data_list):
    keys = []
    for item in data_list:
        for k in item.keys():
            if k not in keys:
                keys.append(k)

    with open(filename, 'w') as csv_file:
        csv_file.write(codecs.BOM_UTF8.decode())
        writer = csv.writer(csv_file)

        writer.writerow(keys)
        for item in data_list:
            row = []
            for k in keys:
                row.append(item.get(k))
            writer.writerow(row)
