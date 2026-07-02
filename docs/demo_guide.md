# Stakeholder Demonstration Guide

This guide helps you demonstrate the Agentic Software Engineering System to stakeholders.

## Quick Demo (5 minutes)

### 1. Show the Repository

Open the repository in a browser:
```
https://github.com/nayaz0916/agentic-software-engineering-system
```

**Key points to highlight**:
- Clean project structure
- Comprehensive documentation
- Working prototype with real implementation

### 2. Run the URL Shortener (Mandatory Use Case)

This is the most impressive demo because it shows a complete, working system.

```bash
# Navigate to the project
cd agentic-software-engineering-system

# Start the URL shortener service
python use_cases/url_shortener/implementation.py
```

The service will start on `http://localhost:8000`

**In a separate terminal, test the API**:

```bash
# Create a short URL
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/url"}'

# Response: {"short_code": "abc123", "original_url": "...", ...}

# Test redirection (in browser or curl)
curl http://localhost:8000/abc123

# Get analytics
curl http://localhost:8000/analytics/abc123

# Health check
curl http://localhost:8000/health
```

**Key points to highlight**:
- Production-ready API with FastAPI
- Redis caching for performance
- SQLite persistence
- Analytics tracking
- Comprehensive test coverage

### 3. Run the Agentic System

```bash
# Run the URL shortener scenario through the agentic system
python main.py --scenario url-shortener
```

This demonstrates the full workflow:
- Requirement analysis
- Task decomposition
- Code generation
- Validation

## Extended Demo (15 minutes)

### 1. Show All Scenarios

```bash
# Greenfield scenario
python main.py --scenario greenfield

# Brownfield scenario
python main.py --scenario brownfield

# Ambiguous requirement
python main.py --scenario ambiguous
```

### 2. Show the Generated Outputs

After running a scenario, show the outputs:

```bash
# View generated code
ls outputs/code/
cat outputs/code/main.py

# View generated tests
ls outputs/tests/
cat outputs/tests/test_main.py

# View generated documentation
ls outputs/docs/
cat outputs/docs/API.md
```

### 3. Run Tests

```bash
# Run URL shortener tests
pytest use_cases/url_shortener/tests/test_url_shortener.py -v
```

## Presentation Structure

### Slide 1: Overview
- **Title**: Agentic Software Engineering System
- **What it does**: Transforms requirements into engineering outcomes
- **Key features**: Requirement understanding, task decomposition, orchestration, code generation, validation

### Slide 2: Architecture
- Show the architecture diagram from `docs/architecture.md`
- Explain the agent-based approach
- Highlight the orchestration engine

### Slide 3: Mandatory Use Case
- **Requirement**: "Build a scalable URL shortener service with APIs, persistence, and analytics"
- **Demonstration**: Live API demo
- **Key achievements**: Working service with tests and documentation

### Slide 4: Other Scenarios
- Greenfield: New system development
- Brownfield: Existing system enhancement
- Ambiguous: Handling unclear requirements

### Slide 5: Validation & Risk Control
- Confidence scoring
- Risk assessment
- Guardrails for safe execution

### Slide 6: Technical Highlights
- Multi-step orchestration with dependencies
- Parallel task execution
- Human-in-the-loop approval
- Error handling and recovery

### Slide 7: Deliverables
- Working prototype ✓
- Architecture overview ✓
- Example scenarios ✓
- Setup instructions ✓
- Testing approach ✓

## Live Demo Script

Use this script for a smooth live demo:

```bash
#!/bin/bash
# demo.sh - Live demonstration script

echo "=== Agentic Software Engineering System Demo ==="
echo ""
echo "1. Starting URL Shortener Service..."
python use_cases/url_shortener/implementation.py &
SERVICE_PID=$!
sleep 3

echo ""
echo "2. Testing the API..."
echo "Creating short URL..."
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/demo"}'

echo ""
echo "3. Running the Agentic System..."
python main.py --scenario url-shortener

echo ""
echo "4. Running Tests..."
pytest use_cases/url_shortener/tests/test_url_shortener.py -v

echo ""
echo "5. Cleaning up..."
kill $SERVICE_PID

echo ""
echo "=== Demo Complete ==="
```

Save as `demo.sh` and run with `bash demo.sh`

## Key Talking Points

### For Technical Stakeholders
- **Architecture**: Multi-agent system with orchestration
- **Scalability**: Can handle complex requirements
- **Quality**: Validation with confidence scoring
- **Extensibility**: Easy to add new agents and scenarios

### For Business Stakeholders
- **Value**: Automates end-to-end software development
- **Speed**: Reduces time from requirement to working code
- **Quality**: Built-in validation and testing
- **Control**: Human oversight with approval checkpoints

### For Interviewers
- **Completeness**: All deliverables implemented
- **Quality**: Production-grade code and tests
- **Documentation**: Comprehensive docs and setup guide
- **Demonstrated Skills**: System design, orchestration, validation

## Troubleshooting Demo Issues

### Service Won't Start
- Check if port 8000 is available
- Ensure dependencies are installed: `pip install -r requirements.txt`

### API Calls Fail
- Verify service is running: `curl http://localhost:8000/health`
- Check Redis is running (optional but recommended)

### Agentic System Fails
- Ensure API key is set in `.env`
- Check internet connection (needs LLM API access)
- Run with `--help` to see options

## Follow-Up Materials

After the demo, provide stakeholders with:
1. Repository URL: https://github.com/nayaz0916/agentic-software-engineering-system
2. Setup instructions: `docs/setup.md`
3. Architecture overview: `docs/architecture.md`
4. Testing approach: `docs/testing.md`
5. URL shortener documentation: `use_cases/url_shortener/README.md`
