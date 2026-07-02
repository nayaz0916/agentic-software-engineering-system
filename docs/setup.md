# Setup Instructions

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Anthropic API key
- (Optional) OpenAI API key
- (Optional) Redis for URL shortener example

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nayaz0916/agentic-software-engineering-system.git
cd agentic-software-engineering-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
```

### 5. Verify Installation

Run the health check:
```bash
python main.py --help
```

## Running the System

### Basic Usage

Run with a custom requirement:
```bash
python main.py --requirement "Build a REST API for user management"
```

### Run Predefined Scenarios

**URL Shortener (Mandatory Use Case):**
```bash
python main.py --scenario url-shortener
```

**Greenfield Scenario:**
```bash
python main.py --scenario greenfield
```

**Brownfield Scenario:**
```bash
python main.py --scenario brownfield
```

**Ambiguous Requirement:**
```bash
python main.py --scenario ambiguous
```

### Run Example Scripts

```bash
# URL shortener example
python examples/url_shortener_example.py

# Greenfield example
python examples/greenfield_example.py

# Brownfield example
python examples/brownfield_example.py

# Ambiguous requirement example
python examples/ambiguous_example.py
```

## Running the URL Shortener Service

The URL shortener is a complete implementation that can be run independently:

### 1. Install Additional Dependencies

```bash
pip install redis
```

### 2. Start Redis (Optional but Recommended)

```bash
redis-server
```

### 3. Run the Service

```bash
python use_cases/url_shortener/implementation.py
```

The service will start on `http://localhost:8000`

### 4. Test the Service

```bash
# Create a short URL
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/url"}'

# Redirect (in browser or curl)
curl http://localhost:8000/{short_code}

# Get analytics
curl http://localhost:8000/analytics/{short_code}

# Health check
curl http://localhost:8000/health
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run URL Shortener Tests

```bash
pytest use_cases/url_shortener/tests/test_url_shortener.py
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

## Output Structure

After running the system, outputs are saved to the `outputs/` directory:

```
outputs/
├── artifacts.json          # All workflow artifacts
├── code/                    # Generated source code
│   ├── main.py
│   ├── models.py
│   ├── api.py
│   └── service.py
├── tests/                   # Generated tests
│   ├── test_main.py
│   ├── test_api.py
│   └── test_integration.py
└── docs/                    # Generated documentation
    ├── API.md
    ├── ARCHITECTURE.md
    └── SETUP.md
```

## Troubleshooting

### API Key Issues

If you get authentication errors:
1. Verify your API key is correct in `.env`
2. Ensure the API key has sufficient credits
3. Check that the API service is operational

### Import Errors

If you get import errors:
1. Ensure you're in the virtual environment
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python version: `python --version` (should be 3.9+)

### Redis Connection Issues

If the URL shortener can't connect to Redis:
1. Ensure Redis is running: `redis-cli ping`
2. Check Redis is on localhost:6379
3. The service will work without Redis (just without caching)

### LLM Rate Limits

If you hit rate limits:
1. Wait a few minutes before retrying
2. Consider using a different API key
3. Reduce the complexity of requirements

## Development Setup

For development with hot-reload:

```bash
pip install pytest-watch
ptw
```

For code formatting:
```bash
pip install black isort
black src/
isort src/
```

For linting:
```bash
pip install flake8
flake8 src/
```

## Production Considerations

For production deployment:

1. **Environment Variables**: Use a secure secret manager
2. **API Keys**: Rotate regularly and use least-privilege access
3. **Database**: Use PostgreSQL instead of SQLite for scalability
4. **Caching**: Use Redis Cluster for distributed caching
5. **Monitoring**: Add logging and metrics (Prometheus, Grafana)
6. **Rate Limiting**: Implement API rate limiting
7. **Authentication**: Add authentication/authorization
8. **HTTPS**: Use TLS certificates
9. **Containerization**: Dockerize the application
10. **Orchestration**: Use Kubernetes for deployment
