# CUA (Computer User Assistant)

A Python framework that enables AI models to interact with web browsers via the OpenAI computer-use-preview API.

## Overview

CUA is a lightweight framework that connects OpenAI's computer-use-preview model to a Playwright-powered browser automation system. It allows AI agents to:

- Navigate to websites
- Capture screenshots of web pages
- Interact with web content (clicking, typing, scrolling)
- Execute complex browser workflows

## Components

- **Agent**: Main class that connects to OpenAI's API and manages the browser
- **BasePlaywrightComputer**: Abstract base class for browser automation
- **LocalPlaywrightComputer**: Implementation for local browser control

## Dependencies

- Python 3.x
- Playwright
- OpenAI Python SDK

## Usage

```python
from agent import Agent

# Initialize the agent
agent = Agent(
    system_prompt="You are a helpful browser assistant.",
    headless=True,  # Set to False to see the browser in action
    verbose=True
)

# Give the agent a task
agent("Go to apple.com and check the latest MacBook Air")
```

To use this framework, you'll need to set your OpenAI API key as an environment variable:
```
export OPENAI_API_KEY="your-api-key"
```