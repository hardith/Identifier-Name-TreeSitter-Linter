import csv

def export_csv(idetifier_details,output_file_path):
    try:
        if len(idetifier_details) > 0:
            keys = idetifier_details[0].keys()

            with open(output_file_path, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(idetifier_details)
    except:
        print("Error: check if the output file path is correct")



