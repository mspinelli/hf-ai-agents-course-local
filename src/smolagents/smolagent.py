import os

from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from phoenix.otel import register

from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel

# Setup telemetry traces for the agent. The code in this module will run
# inside of docker and assumes the telemetry server (phoenix) is running on
# the host machine.
#
# See https://huggingface.co/docs/smolagents/tutorials/inspect_runs for
# more details.
register()
SmolagentsInstrumentor().instrument()

# The following code comes from Unit 2.1 in the Hugging Face AI Agents course
# Section: Building Agents That Use Code
# Subheading: Selecting a Playlist for the Party Using smolagents
#
# Instead of using Hugging Face's Serverless API like the course materials use
# (e.g. HfApiModel), the code here uses Ollama through LiteLLMModel. Ollama is
# a which is a local server that can run any GGUF model downloaded from
# Huggingface. In this case a quantized model for Qwen2.5-Coder-32B-Instruct
# has been downloaded on the host machine already. As with the telemetry server,
# this code assumes that we are running Ollama on the host machine as well.
# On macos, Ollama cannot run inside of docker and utilize the GPU. This is why
# it must be installed on the host machine. Linux host machines, I believe, can
# run Ollama inside of docker and utilize the GPU. But this workaround should
# work on either Linux or Mac.
model = LiteLLMModel(
    model_id=f"ollama_chat/{os.getenv("OLLAMA_MODEL_ID")}",
    api_base=f"http://host.docker.internal:{int(os.getenv("OLLAMA_PORT"))}",
    num_ctx=int(os.getenv("OLLAMA_NUM_CTX")),
)

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)
response = agent.run(
    "Search for the best music recommendations for a party at the Wayne's mansion."
)

# If we weren't using telemetry then this becomes more important, but the
# output of the response will show in a more structured way in on the host
# machine via the telemetry dashboard at http://127.0.0.1:6006/projects by
# default
print(response)
