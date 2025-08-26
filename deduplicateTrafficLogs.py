
""" 
This script compresses traffic log export from Palo Alto firewall by identifying unique flows and aggregating byte and connection counts.
The bytes column sums all traffic from deduplicated entries. The count column indicates how many entries were deduplicated into one.

To export full logs from Panorama:
Can be done via GUI from Monitor tab, however for large logs this can be slow and prone to timeout.
Better to use CLI:
> scp export log traffic query "( rule eq 'RULE NAME' )" to username@hostname:filename.csv start-time equal 2025/04/01@01:00:00 end-time equal 2025/05/06@14:00:00
This will export traffic logs for the specified rule and time period to the specified SCP server.
With the exported CSV file, run this script as follows:
python deduplicateTrafficLogs.py <sourceCSV> <destinationCSV>
"""


import csv
import sys

def process_csv(source_csv, destination_csv):
    # Read source CSV file
    sourceLineCount = 0
    destinationLineCount = 0
    print('Reading source file...')
    with open(source_csv, mode='r') as file:
        reader = csv.DictReader(file)
        source_file = list(reader)
    print('Source file read complete.')
    # Define the columns for the destination CSV file
    columns = ["Source address", "Destination address", "NAT Source IP", "NAT Destination IP", "Rule", "Source User", "Destination User", "Application", "Source Zone", "Destination Zone", "Inbound Interface", "Outbound Interface", "Destination Port", "IP Protocol", "Source Country", "Destination Country", "Subcategory of app", "Category of app", "Risk of app", "Bytes", "Count"]

    # Initialize the destination file data structure
    destination_file = []

    # Process each row in the source file
    for row in source_file:
        sourceLineCount += 1
        # Check if a matching entry exists in the destination file
        match_found = False
        for dest_row in destination_file:
            if (dest_row["Source address"] == row["Source address"] and
                dest_row["Destination address"] == row["Destination address"] and
                dest_row["Source User"] == row["Source User"] and
                dest_row["Destination Port"] == row["Destination Port"]):
                # If a match is found, update the Bytes and Count columns
                dest_row["Bytes"] = int(dest_row["Bytes"]) + int(row["Bytes"])
                dest_row["Count"] = int(dest_row["Count"]) + 1
                match_found = True
                print (f'Source line {sourceLineCount} found a match')
                break

        # If no match is found, create a new row in the destination file
        if not match_found:
            new_row = {col: row[col] if col in row else "" for col in columns}
            new_row["Count"] = 1
            destination_file.append(new_row)
            destinationLineCount += 1
            print (f'Source line {sourceLineCount} created new destination line {destinationLineCount}')

    # Write the destination file to the specified CSV file
    with open(destination_csv, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(destination_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python deduplicateTrafficLogs.py <sourceCSV> <destinationCSV>")
    else:
        source_csv = sys.argv[1]
        destination_csv = sys.argv[2]
        process_csv(source_csv, destination_csv)
