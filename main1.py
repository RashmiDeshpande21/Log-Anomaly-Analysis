import sys
import re
from pydantic import BaseModel
from logparser.Brain import LogParser

from langchain_community.document_loaders import CSVLoader
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory


# Configuration for predefined log formats
log_formats = {
    'Hadoop': '<Date> <Time> <Level> <Process> <Component>: <Content> <EventId> <EventTemplate>',
    'Apache': '<Time> <Level> <Content> <EventId> <EventTemplate>',
    'BGL': '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level>: <Content> <EventId> <EventTemplate>',
    'Linux': '<Month> <Date> <Time> <Level> <Component> <PID>: <Content> <EventId> <EventTemplate>',
    'Proxifier': '<Time> <Program>: <Content> <EventId> <EventTemplate>',
    'HDFS': '<Date> <Time> <Pid> <Level> <Component>: <Content>', 
    'Other': '<Date> <Time> <Level> <Component>: <Content>'
}

def initialize_log_parser(selected_dataset, log_file, input_dir, output_dir, threshold=2, delimiter=[]):
    """
    Initializes the LogParser with the user's selected dataset and parses the log file.
    """
    log_format = log_formats[selected_dataset]
    regex = [
        r'blk_(|-)[0-9]+',  # block id
        r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)',  # IP addresses
        r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$',  # Numbers
    ]
    
    parser = LogParser(
        logname=selected_dataset,
        log_format=log_format,
        indir=input_dir,
        outdir=output_dir,
        threshold=threshold,
        delimeter=delimiter,
        rex=regex
    )
    parser.parse(log_file)
    print("Log parsing completed!")

def load_parsed_data(csv_path):
    """
    Loads the parsed CSV data into a format suitable for analysis.
    """
    loader = CSVLoader(file_path=csv_path)
    data = loader.load()
    return data

def parse_log_entry(log_entry):
    """
    Parses the log entry to isolate the core error message or pattern.
    """
    return re.sub(r'<\*>', '.*?', log_entry) 

def search_csv_for_error(error, data):
    """
    Searches structured CSV data for records that match a specific error.
    """
    matches = []
    for record in data:
        if re.search(error, record.page_content):  
            matches.append(record)
    return matches


def search_similar_issues_with_agents(matches, log_entry, memory):
    """
    Uses multiple agents to find similar issues and group them based on their similarity.
    Introduces memory for historical context and generates detailed explanations.
    """
    if not matches:
        print("No matching log entries found!")
        return []

    filtered_matches = [record for record in matches if record.page_content]
    if not filtered_matches:
        print("No valid log entries found with content.")
        return []

    # Prepare the embeddings for the content field in each matched log entry
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(filtered_matches, embeddings)


    if vector_store.index.ntotal == 0:
        print("No valid documents to index!")
        return []

    # Initialize memory using ConversationBufferMemory
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)

    # Define the tool for similarity search
    tools = [
        Tool(
            name="Log Issue Finder",
            func=vector_store.similarity_search,
            description="Find similar log issues based on error messages"
        )
    ]

    # Initialize the first agent with memory for history
    agent_1 = initialize_agent(
        tools,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        llm=ChatOpenAI(model_name="gpt-4"),
        verbose=True,
        memory=memory
    )
    
    # Instruction to agent to give detailed troubleshooting advice
    prompt = f"""
    You are a troubleshooting assistant. Given the following log entry:
    "{log_entry}",
    Find the probable cause of the error and provide steps to resolve it in the format:
    "This error is likely caused by X. To resolve it, you should check Y and adjust Z."
    """

    # Process the log entry using the first agent to generate a troubleshooting explanation
    explanation = agent_1.run(input=prompt)
    
    return explanation

# Main function
def main():
    # User selects dataset
    print("Select a dataset from the following options:")
    for i, name in enumerate(log_formats.keys(), 1):
        print(f"{i}. {name}")
    
    dataset_choice = input("Enter the number corresponding to the dataset you want to use: ")
    if dataset_choice not in map(str, range(1, len(log_formats) + 1)):
        print("Invalid choice! Exiting program.")
        sys.exit()
    
    # Prepare dataset
    dataset_names = list(log_formats.keys())
    selected_dataset = dataset_names[int(dataset_choice) - 1]
    log_file = input(f"Enter the name of the {selected_dataset} log file (e.g., '{selected_dataset}_logfile.log'): ")
    input_dir = r'C:\Users\RashmiDespande\Projects\LogAnomalyDetection\data'
    output_dir = r'C:\Users\RashmiDespande\Projects\LogAnomalyDetection\result'
    
    # Parse log file
    initialize_log_parser(selected_dataset, log_file, input_dir, output_dir)
    
    # Load parsed CSV data
    csv_path = f"{output_dir}/{selected_dataset}_2k.log_structured.csv"
    data = load_parsed_data(csv_path)
    
    # Process user query
    log_entry = input("Enter a log entry for analysis: ")
    error = parse_log_entry(log_entry)
    relevant_issues = search_csv_for_error(error, data)
    
    # Search and generate responses using multiple agents
    memory = {}  # Initialize memory for agents
    explanation = search_similar_issues_with_agents(relevant_issues, log_entry, memory)
    
    if explanation:
        print("Troubleshooting Information:")
        print(explanation)
    else:
        print("No similar issues found.")

if __name__ == "__main__":
    main()
