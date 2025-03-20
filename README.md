# Local AI Agents Examples for the Hugging Face Course

This repo contains code examples of how to take the examples given in the [hugging face agents course](https://huggingface.co/agents-course), which often rely on the Hugging Face Cloud API, and adapt them to run locally. This repo assumes the local machine uses Apple Silicon with at least 48GB of unified RAM. The code is tested to work on a M4 Pro Mac Mini.

If you have dual 24GB Nvidia GPUs and are running on linux, you should be able to use the code in this repo with little to no modification as well. If you have less ram, you'll have to use either a lower quantization or a smaller model than the default in this repo.

> **Note**: If you have less than 48GB of unified ram or have a lot of other applications in use, running the code as it might freeze your system. If you have exactly 48GB of ram, minimize the number of running apps and run `sudo sysctl iogpu.wired_limit_mb=40960` to dedicate 40GB of ram for the model, leaving 8GB for macos and other apps. Agents fill up the context window quickly and so this repo will be working with 32B parameter models and 32K context windows.

## Initial setup

**Step 1.** Clone this repo and navigate into its root.

**Step 2.** Make sure Python 3.13 is installed.

If you don't have that version of python, you can install `pyenv` as a python version manager. See install instructions [here](https://github.com/pyenv/pyenv?tab=readme-ov-file#a-getting-pyenv). Then run the command below to install the version on your system.

```
pyenv install 3.13
```

**Step 3.** Create a new environment inside the root of the cloned repo using the built in `venv` command. This will create a folder in the project named venv to store the local environment (the last parameter in the command below specifies the name and uses venv to be clear what this folder is for).

```
python -m venv venv
```

**Step 4.** Activate the environment.

```
source venv/bin/activate
```

**Step 5.** Spot check the python version is right.

```
python --version
Python 3.13.1
```

**Step 6.** Ensure that docker is installed and running. One of the easiest ways to install that is via [Docker Desktop](https://docs.docker.com/desktop/). Make sure docker is running.

**Step 7.** Install Ollama (click download on the [main page](https://ollama.com/)). Make sure ollama is running.

**Step 8.** Download the Qwen2.5 Coder Instruct 32B model.

```
ollama pull hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-GGUF:Q6_K_L
```

> **Note** You can get find the command to download any specific quantization by clicking on the quantization and then selecting `Use this model -> Ollama` from [this](https://huggingface.co/bartowski/Qwen2.5-Coder-32B-Instruct-GGUF) page.

## Smolagents (Unit 2.1 in the course)

This example runs a one of the agents shown in the course, but does so with the modification of being able to run it locally in a sandboxed environment with docker.

Assuming you've completed the Initial Setup above. You'll need to use two terminals and follow the steps below.

**Step 1.** Install Arize AI Phoenix and Docker optional dependencies for smolagents.

```
pip install 'smolagents[telemetry, docker]'
```

**Step 2.** Start the telemtry server.

`python -m phoenix.server.main serve`

> Note: It will take like 30 seconds to startup.

**Step 3.** In the other terminal, navigate to the smolagents directory

```
cd src/smolagents
```

Then run the example agent.

```
python sandbox_run.py
```

**Step 4.** Browse to http://127.0.0.1:6006/projects to see what the model is doing.

> Note: It will take a moment to start seeing initial results for the agent's first step. On an M4 Pro with 20 GPU cores and the Q6_K_L version of a 32B model, it took about 20 seconds to see the first step and a bit over 5 minutes to complete the task in 5 steps. You can see my local agents results below.
>
> <img src="/src/smolagents/results.png" title="smolagents phoenix telemetry results" alt="smolagents phoenix telemetry results">

## LlamaIndex

Coming Soon!

## LangGraph

Coming Soon!
