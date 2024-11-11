# Log Analysis and Anomaly Detection Using AI

## Overview

This project demonstrates how large-scale system logs can be analyzed to detect anomalies, explain errors, and suggest resolutions using AI-based approaches. The solution simulates a real-world scenario where system logs need to be processed to identify and resolve issues.

The solution integrates various techniques like prompt engineering, AI agents, and vector-based search to detect and troubleshoot errors from log files.

## Features

- **Log Parsing**: Parses log files from various formats like Hadoop, Apache, Linux, HDFS, etc., to extract structured data.
- **Error Detection**: Searches structured log data for errors and anomalies using regex patterns.
- **AI-based Anomaly Detection**: Uses OpenAI's GPT-4 and LangChain to identify the probable cause of errors and provide detailed troubleshooting steps.
- **Memory**: Utilizes conversation memory to provide context for recurring issues and offer more relevant solutions.

## Technologies Used

- **Python**: Primary programming language.
- **LangChain**: For managing LLMs, document loaders, vector stores, and agents.
- **OpenAI**: For leveraging the GPT-4 model to process log entries and generate explanations.
- **FAISS**: For similarity search and handling large datasets efficiently.
- **Pydantic**: For data validation and model definition.
- **Regular Expressions**: To identify specific log patterns and anomalies.

## Datasets

The project supports the following log datasets:

- **Hadoop**
- **Apache**
- **BGL**
- **Linux**
- **Proxifier**
- **HDFS**
- **Other (generic format)**

Each dataset comes with its predefined log format and regex patterns for parsing.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/log-anomaly-detection.git
   cd log-anomaly-detection

2. Set up the environment: It's recommended to use a virtual environment. You can use Anaconda or venv to create one.

   ```bash
   pip install -r requirements.txt
   ```


## Usage

- **Select Dataset**: When you run the program, you will be prompted to select a dataset from the available options (e.g., Hadoop, Apache, etc.).

- **Log Parsing**: After selecting the dataset, the program will parse the log file based on its predefined format and store the structured data in a CSV file.

- **Error Query**: Enter a log entry or error message to analyze. The AI will process the entry, search for similar issues in the parsed data, and provide troubleshooting advice.

- **AI Troubleshooting**: The model (GPT-4) will provide possible causes for the error and suggest steps to resolve it.

### Example Run:
```bash
Select a dataset from the following options:
1. Hadoop
2. Apache
3. Linux
4. HDFS
5. Other


Enter the number corresponding to the dataset you want to use: 1

Enter the name of the Hadoop log file (e.g., 'hadoop_logfile.log'): <hadoop_logfile_name>.log

Enter a log entry for analysis: Error: Block allocation failed
```

## Directory Structure

```perl
log-anomaly-detection/
│
├── data/                   # Raw log files
├── result/                 # Parsed and structured log data
├── main.py                 # Main script to run the application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── utils.py                # Helper functions for log parsing and analysis

```

## Scalability
For large-scale log analysis, the solution can be optimized to handle millions of log entries by:

1. Using batch processing for log parsing.
2. Storing structured data in a database for faster querying.
3. Implementing parallel processing with multi-threading or distributed systems like Spark.

## Future Improvements

- **Model Fine-Tuning**: Fine-tuning the GPT model on specific log data could improve accuracy and performance for troubleshooting tasks.
- **Real-Time Monitoring**: Implementing continuous log analysis with real-time streaming platforms like Kafka.
- **Better Error Classification**: Adding more granular error classification to improve troubleshooting advice.
- **Anomaly Detection for Entire Files**: Training a model to detect anomalies across the whole log file, rather than focusing on individual log entries, could improve the detection of systemic issues or patterns across multiple log events.
- **Enhanced Log Parsing**: Developing a more robust log parsing function with better support for varied log structures, customizable delimiters, and flexible parsing rules to handle diverse log formats more effectively.
- **Chat Interface for Improved Visualization**: Creating a chat-based interface for better interaction with the system, enabling users to query logs and get real-time troubleshooting advice in a more intuitive and visual format.

