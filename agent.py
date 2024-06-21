from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langsmith import traceable
from langchain_community.tools.shell.tool import ShellTool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from tools import *
from prompts import *
from dotenv import load_dotenv

load_dotenv()


# @tool
# def create_react_app_with_vite():
#     """
#     This function creates a new React application using Vite in the 'app' directory located in the root.
#
#     It navigates to the root directory, finds or creates the 'app' directory,
#     and uses the npm 'create vite@latest' command to scaffold a new React project
#     with Vite as the build tool and React as the template. If the process is
#     successful, it prints a success message. If any subprocess command fails,
#     it catches the CalledProcessError exception and prints an error message.
#     """
#     try:
#         # Create a new Vite project in the app directory with React template
#         subprocess.run(['npm', 'create', 'vite@latest', '.', '--template', 'react'], check=True)
#         # Print success message if project creation is successful
#         return f"Successfully created a new React app using Vite."
#     except subprocess.CalledProcessError as e:
#         # Print error message if any subprocess command fails
#         return f"An error occurred: {e}"
#     except Exception as e:
#         # Print error message if any other exception occurs
#         return f"An unexpected error occurred: {e}"
#         # End of Selection


def create_agent(tools, system_prompt):
    # Configure the language model
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # Set up the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Bind the tools to the language model
    llm_with_tools = llm.bind_tools(tools)

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    return AgentExecutor(agent=agent, tools=tools, verbose=True)




# List of tools to use
coder_tools = [
    ShellTool(ask_human_input=True),
    create_directory,
    find_file,
    create_file,
    update_file,
    tavily_web_search
    # Add more tools if needed
]

reviewer_tools = [
    get_files_in_directory,
    find_file,
    read_file,
    tavily_web_search
    # Add more tools if needed
]

# Create the agents
coder_agent_executor = create_agent(coder_tools, CODER_PROMPT)
reviewer_agent_executor = create_agent(reviewer_tools, REVIEWER_PROMPT)


# Main loop to prompt the user
if __name__ == "__main__":
    try:
        iteration_count = 0
        user_prompt = input("Prompt: ")
        reviewer_feedback = ""
        while iteration_count < 5:    
            try:
                coder_output = list(coder_agent_executor.stream({"input": user_prompt}))[-1]['output']
                print(f"Coder output: {coder_output}")
                reviewer_feedback = list(reviewer_agent_executor.stream({"input": f"### Previous Feedback: \n{reviewer_feedback}\n\n### Coder output: \n{coder_output}"}))[-1]['output']
                print(f"Reviewer feedback: {reviewer_feedback}")
                if 'FINISHED' in reviewer_feedback:
                    break
                else:
                    user_prompt = reviewer_feedback
            except AttributeError as e:
                print(f"An error occurred: {e}")
            iteration_count += 1
        
        print(f"Finished the program after {iteration_count} iterations.")
    except KeyboardInterrupt:
        print("\nExiting the program.")

