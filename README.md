# CVHancer AI Agent

An AI agent for analysing and improving resumes (CVs) and matching them to job descriptions. It is built in Python on Claude through the official [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python).

> **Status:** early development. The repository currently contains the agent framework (a streaming chat and a tool-using agent), the datasets, and a first data-exploration notebook. CV-specific tools are not implemented yet.

## Features

- **Interactive chat** (`ai-chat`): streams Claude's replies and keeps the full conversation history.
- **Tool-using agent** (`ai-agent`): Claude decides when to call the Python tools defined in `tools.py`.
- **Configurable** model, reasoning effort and output length, set through environment variables.
- **Datasets** of resumes and job descriptions for exploring and building CV/job matching.

## Project structure

```
.
├── src/ai_project/
│   ├── config.py        # Settings loaded from env / .env (model, effort, max tokens)
│   ├── client.py        # Shared Anthropic client
│   ├── chat.py          # Interactive streaming chat (ai-chat)
│   ├── agent.py         # Tool-using agent (ai-agent)
│   └── tools.py         # Agent tools (plain functions wrapped with @beta_tool)
├── tests/               # Unit tests (no API calls)
├── Resume/              # Resume dataset (Resume.csv)
├── JobdescriptionDataset/  # Job description dataset
├── dataCleaning.ipynb   # Data exploration / cleaning notebook
├── .env.example         # Template for environment variables
└── pyproject.toml
```

## Getting started

### Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- An Anthropic API key ([get one here](https://console.anthropic.com/settings/keys))

### Installation

```bash
git clone https://github.com/maryemkhlifi/CVHancer-AI-Agent-.git
cd CVHancer-AI-Agent-
uv sync
```

### Configuration

Copy the example environment file and add your API key:

```bash
cp .env.example .env
```

| Variable            | Default           | Description                                       |
| ------------------- | ----------------- | ------------------------------------------------- |
| `ANTHROPIC_API_KEY` | —                 | Your Anthropic API key (required)                 |
| `CLAUDE_MODEL`      | `claude-opus-5-5` | Model to use                                      |
| `CLAUDE_EFFORT`     | `high`            | `low`, `medium`, `high`, `xhigh` or `max`         |
| `CLAUDE_MAX_TOKENS` | `64000`           | Maximum output tokens per chat response           |

`.env` is gitignored. Never commit your API key.

## Usage

```bash
# Interactive chat (type 'exit' to quit)
uv run ai-chat

# Give the agent a single task
uv run ai-agent "What is 17% of 2340, and what time is it?"
```

## Datasets

### `Resume/Resume.csv`

Contains 2,484 resumes with these columns:

| Column        | Description |
| ------------- | ----------- |
| `ID`          | Unique resume identifier. |
| `Resume_str`  | The resume as plain text (summary, skills, experience, education, accomplishments). **Start here.** You can give this text to the model to extract skills, years of experience, education and previous roles. |
| `Resume_html` | The same resume as HTML. It is useful for experimenting with structured text extraction, and you can ignore it at first. |
| `Category`    | Occupational category, such as `HR`, `INFORMATION-TECHNOLOGY`, `ACCOUNTANT` or `ENGINEERING`. Use it as a label to predict a resume's field. It says nothing about the resume's quality and is not a job description. |

### `JobdescriptionDataset/jobDescription_dataset.csv`

Job postings with two columns: `Job Title` and `Description`.

### `jobmatchingDatset/` (not included)

The CV/vacancy matching dataset (`train (1).csv`, about 1 GB) is too large for GitHub and is excluded through `.gitignore`. To use it, download it separately and place it in `jobmatchingDatset/`.

## Development

```bash
uv run pytest            # run tests (tests never call the API)
uv run ruff check .      # lint
uv run ruff format .     # format
```

### Adding an agent tool

1. Write the logic as a plain function in `src/ai_project/tools.py` and add unit tests for it in `tests/`.
2. Wrap it with `@beta_tool`. The docstring becomes the tool description the model sees.
3. Add it to `ALL_TOOLS`.

## Roadmap

- [ ] Clean and preprocess the resume and job description datasets
- [ ] Tool to extract structured data (skills, experience, education) from a resume
- [ ] Tool to score a resume against a job description
- [ ] Generate targeted suggestions to improve a CV for a specific job
