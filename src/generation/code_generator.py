from typing import Optional
from anthropic import Anthropic
from src.models import Workflow, CodebaseAnalysis, EngineeringOutput
import os


class CodeGenerator:
    """Generates engineering outputs: code, tests, documentation."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    
    def generate(self, workflow: Workflow, codebase_analysis: Optional[CodebaseAnalysis] = None) -> EngineeringOutput:
        """Generate all engineering outputs for the workflow."""
        
        outputs = EngineeringOutput()
        
        # Generate code
        outputs.code = self._generate_code(workflow, codebase_analysis)
        
        # Generate tests
        outputs.tests = self._generate_tests(workflow)
        
        # Generate documentation
        outputs.documentation = self._generate_documentation(workflow)
        
        # Generate API contracts
        outputs.api_contracts = self._generate_api_contracts(workflow)
        
        # Generate schemas
        outputs.schemas = self._generate_schemas(workflow)
        
        return outputs
    
    def _generate_code(self, workflow: Workflow, codebase_analysis: Optional[CodebaseAnalysis]) -> dict:
        """Generate production-quality code."""
        
        prompt = f"""Generate production-quality code for this requirement.

Requirement: "{workflow.requirement.normalized or workflow.requirement.original}"
Tasks: {[t.description for t in workflow.tasks]}

Generate:
1. Main application code
2. API handlers
3. Data models
4. Service layer
5. Configuration

Provide clean, modular, well-documented code. Use Python/FastAPI by default unless specified otherwise."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}]
        )
        
        code_content = response.content[0].text
        
        return {
            "main.py": self._extract_code_block(code_content, "main.py"),
            "models.py": self._extract_code_block(code_content, "models.py"),
            "api.py": self._extract_code_block(code_content, "api.py"),
            "service.py": self._extract_code_block(code_content, "service.py"),
            "config.py": self._extract_code_block(code_content, "config.py")
        }
    
    def _generate_tests(self, workflow: Workflow) -> dict:
        """Generate unit and integration tests."""
        
        prompt = f"""Generate comprehensive tests for this requirement.

Requirement: "{workflow.requirement.normalized or workflow.requirement.original}"

Generate:
1. Unit tests for core functionality
2. Integration tests for APIs
3. Edge case tests
4. Performance tests

Use pytest framework."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        test_content = response.content[0].text
        
        return {
            "test_main.py": self._extract_code_block(test_content, "test_main"),
            "test_api.py": self._extract_code_block(test_content, "test_api"),
            "test_integration.py": self._extract_code_block(test_content, "test_integration")
        }
    
    def _generate_documentation(self, workflow: Workflow) -> dict:
        """Generate documentation."""
        
        prompt = f"""Generate documentation for this requirement.

Requirement: "{workflow.requirement.normalized or workflow.requirement.original}"

Generate:
1. API documentation
2. Architecture overview
3. Setup instructions
4. Usage examples"""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        doc_content = response.content[0].text
        
        return {
            "API.md": doc_content,
            "ARCHITECTURE.md": self._extract_section(doc_content, "Architecture"),
            "SETUP.md": self._extract_section(doc_content, "Setup")
        }
    
    def _generate_api_contracts(self, workflow: Workflow) -> dict:
        """Generate API contracts (OpenAPI/Swagger)."""
        
        return {
            "openapi.yaml": """openapi: 3.0.0
info:
  title: Generated API
  version: 1.0.0
paths:
  /api/endpoint:
    get:
      summary: Example endpoint
      responses:
        '200':
          description: Success
"""
        }
    
    def _generate_schemas(self, workflow: Workflow) -> dict:
        """Generate data schemas."""
        
        return {
            "schema.json": """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated Schema",
  "type": "object"
}"""
        }
    
    def _extract_code_block(self, content: str, filename: str) -> str:
        """Extract a specific code block from generated content."""
        lines = content.split('```')
        for i, block in enumerate(lines):
            if filename in block or (i > 0 and 'python' in lines[i-1]):
                return block.strip()
        return content[:500]  # Fallback
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a section from documentation."""
        lines = content.split('\n')
        section_lines = []
        capture = False
        for line in lines:
            if section_name.lower() in line.lower():
                capture = True
            elif capture and line.startswith('#'):
                break
            elif capture:
                section_lines.append(line)
        return '\n'.join(section_lines) or content[:300]
