import sys
from logparser.Brain import LogParser

# Predefined log formats for different datasets
log_formats = {
    'Hadoop': '<Date> <Time> <Level> <Process> <Component>: <Content> <EventId> <EventTemplate>',
    'Apache': '<Time> <Level> <Content> <EventId> <EventTemplate>',
    'BGL': '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level>: <Content> <EventId> <EventTemplate>',
    'Linux': '<Month> <Date> <Time> <Level> <Component> <PID>: <Content> <EventId> <EventTemplate>',
    'Proxifier': '<Time> <Program>: <Content> <EventId> <EventTemplate>',
    'HDFS': '<Date> <Time> <Pid> <Level> <Component>: <Content>',  # New format for HDFS
    'Other': '<Date> <Time> <Level> <Component>: <Content>'  # Default format for Other
}

# Display available log formats by name (not showing the format)
print("Select a dataset from the following options:")
for i, name in enumerate(log_formats.keys(), 1):
    print(f"{i}. {name}")

# Get user input for dataset selection
dataset_choice = input("Enter the number corresponding to the dataset you want to use: ")

# Validate the input
if dataset_choice not in ['1', '2', '3', '4', '5', '6', '7']:
    print("Invalid choice! Exiting program.")
    sys.exit()

# Map numeric input to log format name
dataset_names = list(log_formats.keys())
selected_dataset = dataset_names[int(dataset_choice) - 1]
log_format = log_formats[selected_dataset]

# Get user input for log file path
log_file = input(f"Enter the name of the {selected_dataset} log file (e.g., '{selected_dataset}_logfile.log'): ")

# Default paths for input and output directories
input_dir = r'C:\Users\RashmiDespande\Projects\LogAnomalyDetection\data'
output_dir = r'C:\Users\RashmiDespande\Projects\LogAnomalyDetection\result'

# Optional: Regular expression list for optional preprocessing
regex = [
    r'blk_(|-)[0-9]+',  # block id
    r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)',  # IP
    r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$',  # Numbers
]

# Set threshold and delimeter options
threshold = 2  # Similarity threshold
delimeter = []  # Depth of all leaf nodes

# Initialize the LogParser with the user's input
parser = LogParser(logname=selected_dataset, log_format=log_format, indir=input_dir, 
                   outdir=output_dir, threshold=threshold, delimeter=delimeter, rex=regex)

# Parse the log file
parser.parse(log_file)

print("Log parsing completed!")
