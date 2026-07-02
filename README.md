# Agentic Software Engineering System

A working prototype of an agentic system that transforms software requirements into reviewable engineering outcomes.

## Overview

This system demonstrates end-to-end workflow automation across the SDLC, including:
- Requirement understanding and normalization
- Task decomposition with dependency management
- Codebase reasoning for brownfield scenarios
- Multi-step workflow orchestration
- Engineering output generation (code, tests, docs)
- Validation and risk control

## Architecture

The system consists of:
- **Requirement Understanding Agent**: Interprets intent and identifies ambiguities
- **Task Decomposition Agent**: Breaks requirements into structured, actionable tasks
- **Codebase Reasoning Agent**: Analyzes existing architecture for brownfield scenarios
- **Workflow Orchestration Engine**: Coordinates multi-step execution with dependency management
- **Output Generation Module**: Produces code, tests, and documentation
- **Validation System**: Implements guardrails and risk assessment

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the system with a requirement
python main.py --requirement "Build a scalable URL shortener service"
```

## Mandatory Use Case

The system demonstrates the URL shortener requirement:
"Build a scalable URL shortener service with APIs, persistence, and analytics."

## Example Scenarios

- **Greenfield**: New feature or system development
- **Brownfield**: Enhancements, refactoring, and bug fixes
- **Ambiguous**: Handling unclear requirements

## Documentation

- [Architecture Overview](docs/architecture.md)
- [Setup Instructions](docs/setup.md)
- [Testing Approach](docs/testing.md)
- [Example Scenarios](docs/examples.md)
