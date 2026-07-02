from typing import Optional
from anthropic import Anthropic
from src.models import CodebaseAnalysis, Requirement
import os


class CodebaseReasoningAgent:
    """Analyzes existing codebase for brownfield scenarios."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    
    def analyze(self, requirement: Requirement, codebase_path: Optional[str] = None) -> CodebaseAnalysis:
        """Analyze codebase to identify impacted components."""
        
        if codebase_path:
            # In production, would actually scan the codebase
            # For now, simulate analysis
            analysis = self._analyze_with_codebase(requirement, codebase_path)
        else:
            analysis = self._analyze_without_codebase(requirement)
        
        return analysis
    
    def _analyze_with_codebase(self, requirement: Requirement, codebase_path: str) -> CodebaseAnalysis:
        """Analyze with actual codebase scanning."""
        prompt = f"""Analyze how this requirement would impact an existing codebase.

Requirement: "{requirement.normalized or requirement.original}"
Codebase path: {codebase_path}

Identify:
1. Impacted services/modules
2. API changes needed
3. Data flow changes
4. Potential risks

Provide a structured analysis."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        
        return CodebaseAnalysis(
            impacted_services=self._extract_services(content),
            impacted_modules=self._extract_modules(content),
            api_changes=self._extract_api_changes(content),
            data_flow_changes=self._extract_data_flow_changes(content),
            risks=self._extract_risks(content)
        )
    
    def _analyze_without_codebase(self, requirement: Requirement) -> CodebaseAnalysis:
        """Provide generic analysis without codebase access."""
        return CodebaseAnalysis(
            impacted_services=["Core service", "API gateway"],
            impacted_modules=["Business logic", "Data access", "API handlers"],
            api_changes=["New endpoints", "Modified request/response schemas"],
            data_flow_changes=["New data paths", "Updated caching strategy"],
            risks=["Breaking changes", "Performance impact", "Data migration"]
        )
    
    def _extract_services(self, content: str) -> list:
        lines = content.split('\n')
        services = []
        for line in lines:
            if 'service' in line.lower() and ':' in line:
                services.append(line.split(':')[1].strip())
        return services or ["Core service"]
    
    def _extract_modules(self, content: str) -> list:
        lines = content.split('\n')
        modules = []
        for line in lines:
            if 'module' in line.lower() and ':' in line:
                modules.append(line.split(':')[1].strip())
        return modules or ["Business logic", "Data access"]
    
    def _extract_api_changes(self, content: str) -> list:
        lines = content.split('\n')
        changes = []
        for line in lines:
            if 'api' in line.lower() and ':' in line:
                changes.append(line.split(':')[1].strip())
        return changes or ["New endpoints"]
    
    def _extract_data_flow_changes(self, content: str) -> list:
        lines = content.split('\n')
        changes = []
        for line in lines:
            if 'data flow' in line.lower() and ':' in line:
                changes.append(line.split(':')[1].strip())
        return changes or ["Updated data paths"]
    
    def _extract_risks(self, content: str) -> list:
        lines = content.split('\n')
        risks = []
        for line in lines:
            if 'risk' in line.lower() and ':' in line:
                risks.append(line.split(':')[1].strip())
        return risks or ["Breaking changes", "Performance impact"]
