# PaloScripts
Various scripts for Palo Alto

# deduplicateTrafficLogs.py

This script deduplicates traffic log export from Palo Alto firewall by identifying unique flows and aggregating byte and connection counts.
The flows are matched on source/destination IP, source user, application and destination port.
The bytes column sums all traffic from deduplicated entries. The count column indicates how many entries were deduplicated into one.

To export full logs from Panorama:
Can be done via GUI from Monitor tab, however for large logs this can be slow and prone to timeout.
Better to use CLI:
> scp export log traffic query "( rule eq 'RULE NAME' )" to username@hostname:filename.csv start-time equal 2025/04/01@01:00:00 end-time equal 2025/05/06@14:00:00
This will export traffic logs for the specified rule and time period to the specified SCP server.
With the exported CSV file, run this script as follows:
python deduplicateTrafficLogs.py <sourceCSV> <destinationCSV>
