"""
This code is to run a sandbox environment for running SmolAgents agents.
It's based on the tutorial provided by Hugging Face, which can be found at:
https://huggingface.co/docs/smolagents/tutorials/secure_code_execution#docker-setup

Changes to the default code are explained in the comments below.
"""

import os
from typing import Optional

import docker
from dotenv import load_dotenv


class DockerSandbox:
    def __init__(self):
        self.client = docker.from_env()
        self.container = None

    def create_container(self):
        try:
            image, build_logs = self.client.images.build(
                path=".",
                tag="agent-sandbox",
                rm=True,
                forcerm=True,
                buildargs={},
                # decode=True
            )
        except docker.errors.BuildError as e:
            print("Build error logs:")
            for log in e.build_log:
                if "stream" in log:
                    print(log["stream"].strip())
            raise

        # Create container with security constraints and proper logging
        #
        # This configuration assumes that the Phoenix server is running on the
        # host machine to collect telemetry traces of the agent. This requires
        # that the working directory is accessible to the both the host and
        # the container. Notice that /mnt/vol1 is a volume mounted on the host
        # machine and typically will point to the default folder created when
        # Phoenix is installed. In this case it's a home user on a macOS
        # machine (/Users/<USER>/.phoenix/) and if you're running this code
        # you'll want to change this to your own or create an environment
        # variable to load in the path.
        self.container = self.client.containers.run(
            "agent-sandbox",
            command="tail -f /dev/null",  # Keep container running
            detach=True,
            tty=True,
            mem_limit="512m",
            cpu_quota=50000,
            pids_limit=100,
            security_opt=["no-new-privileges"],
            cap_drop=["ALL"],
            environment={
                # This isn't need for running 100% local: "HF_TOKEN": os.getenv("HF_TOKEN"),
                "PHOENIX_COLLECTOR_ENDPOINT": f"http://host.docker.internal:{int(os.getenv("PHOENIX_PORT"))}",
                "PHOENIX_WORKING_DIR": "/mnt/vol1",
            },
            mounts=[
                {
                    "type": "bind",
                    "source": os.getenv("PHOENIX_PATH"),
                    "target": "/mnt/vol1",
                },
            ],
        )

    def run_code(self, code: str) -> Optional[str]:
        if not self.container:
            self.create_container()

        # Execute code in container
        exec_result = self.container.exec_run(cmd=["python", "-c", code], user="nobody")

        # Collect all output
        return exec_result.output.decode() if exec_result.output else None

    def cleanup(self):
        if self.container:
            try:
                self.container.stop()
            except docker.errors.NotFound:
                # Container already removed, this is expected
                pass
            except Exception as e:
                print(f"Error during cleanup: {e}")
            finally:
                self.container = None  # Clear the reference


# Function to replace environment variables in the script content
# Which is needed since smolagent.py is converted to a string and passed
# to the DockerSandbox and the dotenv context doesn't seem to persist
# once it's evaluated there. So this is a workaround to the structure
# of the code examples being worked with from the course.
def replace_env_vars(script_content):
    env_vars = {
        "OLLAMA_MODEL_ID": os.getenv("OLLAMA_MODEL_ID"),
        "OLLAMA_PORT": os.getenv("OLLAMA_PORT"),
        "OLLAMA_NUM_CTX": os.getenv("OLLAMA_NUM_CTX"),
    }

    for var_name, var_value in env_vars.items():
        placeholder = f'os.getenv("{var_name}")'
        if var_value is not None:
            script_content = script_content.replace(placeholder, f'"{var_value}"')
        else:
            raise ValueError(f"Environment variable {var_name} is not set.")

    return script_content


# Wrapped the example code in a main function block to make this code
# easier to be run directly from the command line or from a script.
def main() -> int:
    sandbox = DockerSandbox()
    # load environment variables from .env file
    load_dotenv()

    try:
        # Define your agent code
        #
        # Instead of hard coding the agent code as a string here like in the
        # example code, this imports the code from smolagents.py
        with open("smolagent.py", "r") as file:
            agent_code = replace_env_vars(file.read())

        # Run the code in the sandbox
        output = sandbox.run_code(agent_code)
        print(output)

    finally:
        sandbox.cleanup()


if __name__ == "__main__":
    main()
