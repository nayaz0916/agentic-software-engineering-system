#!/bin/bash
# Live demonstration script for stakeholders

echo "=========================================="
echo "Agentic Software Engineering System Demo"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

echo "Step 1: Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required"
    exit 1
fi
echo "✓ Python found"
echo ""

echo "Step 2: Checking API key..."
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Creating from example..."
    cp .env.example .env
    echo "Please add your ANTHROPIC_API_KEY to .env file"
    echo "Then run this script again"
    exit 1
fi
echo "✓ .env file found"
echo ""

echo "Step 3: Starting URL Shortener Service..."
echo "(This will run in the background)"
python use_cases/url_shortener/implementation.py > /tmp/url_shortener.log 2>&1 &
SERVICE_PID=$!
sleep 3

# Check if service started
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "Error: Service failed to start. Check /tmp/url_shortener.log"
    kill $SERVICE_PID 2>/dev/null
    exit 1
fi
echo "✓ Service started on http://localhost:8000"
echo ""

echo "Step 4: Testing URL Shortener API..."
echo ""
echo "Creating a short URL..."
SHORT_RESPONSE=$(curl -s -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/demo-url-for-stakeholders"}')
echo "$SHORT_RESPONSE" | python3 -m json.tool
echo ""

# Extract short code
SHORT_CODE=$(echo "$SHORT_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['short_code'])")
echo "Short code created: $SHORT_CODE"
echo ""

echo "Testing redirection..."
curl -s -I http://localhost:8000/$SHORT_CODE | head -n 1
echo ""

echo "Getting analytics..."
curl -s http://localhost:8000/analytics/$SHORT_CODE | python3 -m json.tool
echo ""

echo "Step 5: Running the Agentic System..."
echo "This will demonstrate the full workflow:"
echo "  - Requirement analysis"
echo "  - Task decomposition"
echo "  - Code generation"
echo "  - Validation"
echo ""
python main.py --scenario url-shortener
echo ""

echo "Step 6: Running URL Shortener Tests..."
echo ""
pytest use_cases/url_shortener/tests/test_url_shortener.py -v --tb=short
echo ""

echo "Step 7: Showing generated outputs..."
echo ""
if [ -d "outputs" ]; then
    echo "Generated files:"
    find outputs -type f | head -20
    echo ""
    echo "Code files:"
    ls -la outputs/code/ 2>/dev/null || echo "No code files generated"
    echo ""
    echo "Test files:"
    ls -la outputs/tests/ 2>/dev/null || echo "No test files generated"
    echo ""
    echo "Documentation:"
    ls -la outputs/docs/ 2>/dev/null || echo "No documentation generated"
else
    echo "No outputs directory found"
fi
echo ""

echo "Step 8: Cleaning up..."
kill $SERVICE_PID 2>/dev/null
echo "✓ Service stopped"
echo ""

echo "=========================================="
echo "Demo Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Review the outputs in the outputs/ directory"
echo "2. Check the documentation in docs/"
echo "3. Try other scenarios: python main.py --scenario greenfield"
echo "4. View the repository: https://github.com/nayaz0916/agentic-software-engineering-system"
echo ""
