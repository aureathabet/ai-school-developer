# AI For Developer Productivity: Coder Agent

## Overview
This project features a Coder Agent designed to enhance developer productivity by automating code writing, an iterative code review feedback loop, and terminal command execution. The agent leverages tools to streamline workflows, ensuring accuracy and efficiency.

## Getting Started
To get started, clone the repository and install the required dependencies:
```bash
git clone <repository-url>
cd <repository-directory>
pip install -r requirements.txt
```

## Usage
Run the main script to start interacting with the Coder Agent:
```bash
python agent.py
```

## Agents
The codebase includes the following agents:
- **Coder Agent**: Uses tools like `ShellTool`, `create_directory`, `find_file`, `create_file`, `update_file`, and `tavily_web_search`.
- **Reviewer Agent**: Uses tools like `get_files_in_directory`, `find_file`, `read_file`, and `tavily_web_search`.

## Tools
The agent uses a variety of tools to perform its tasks:
- **ShellTool**: Executes shell commands.
- **create_directory**: Creates a new directory.
- **find_file**: Searches for a file.
- **create_file**: Creates a new file.
- **update_file**: Updates an existing file.
- **tavily_web_search**: Performs web searches using the Tavily API.
- **get_files_in_directory**: Retrieves a list of files in a directory.
- **read_file**: Reads the contents of a file.

## Customization
You can add new tools to match your specific workflow needs. For example, to add a tool for creating a React app with Vite, you can define it in `tools.py` and include it in the `coder_tools` list.

## Advanced Features
### Implemented:
- **Iterative Code Review Feedback Loop**: Identify potential bugs and suggest improvements, then send it back to the code for implementation.

### Consider implementing advanced features such as:
- **Context-Aware Assistance**: Offer suggestions based on project structure.
- **Collaboration**: Facilitate team collaboration with automated code reviews.
- **CI/CD Integration**: Automate testing and deployment processes.
- **AI-Driven Learning**: Personalize assistance based on coding patterns.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.