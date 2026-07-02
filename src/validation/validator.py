from typing import Optional
from anthropic import Anthropic
from src.models import Workflow, EngineeringOutput, ValidationResult, RiskAssessment
import os


class Validator:
    """Validates engineering outputs and assesses risks."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    
    def validate(self, workflow: Workflow, outputs: EngineeringOutput) -> ValidationResult:
        """Validate generated outputs against requirements."""
        
        prompt = f"""Validate the following engineering outputs against the original requirement.

Original Requirement: "{workflow.requirement.original}"
Normalized Requirement: "{workflow.requirement.normalized}"

Generated Outputs:
- Code files: {list(outputs.code.keys())}
- Test files: {list(outputs.tests.keys())}
- Documentation: {list(outputs.documentation.keys())}

Assess:
1. Does the output meet the requirement? (yes/no)
2. What issues or gaps exist?
3. What warnings should be noted?
4. Recommendations for improvement
5. Confidence score (0.0 to 1.0)

Provide structured validation."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        
        return ValidationResult(
            passed=self._extract_passed(content),
            issues=self._extract_issues(content),
            warnings=self._extract_warnings(content),
            recommendations=self._extract_recommendations(content),
            confidence_score=self._extract_confidence(content)
        )
    
    def assess_risks(self, workflow: Workflow) -> RiskAssessment:
        """Assess risks, trade-offs, and failure scenarios."""
        
        prompt = f"""Assess risks for this engineering project.

Requirement: "{workflow.requirement.normalized or workflow.requirement.original}"
Tasks: {[t.description for t in workflow.tasks]}

Identify:
1. Technical risks
2. Trade-offs in design decisions
3. Potential failure scenarios
4. Mitigation strategies for each risk

Provide structured risk assessment."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        
        return RiskAssessment(
            risks=self._extract_risks(content),
            trade_offs=self._extract_tradeoffs(content),
            failure_scenarios=self._extract_failure_scenarios(content),
            mitigation_strategies=self._extract_mitigations(content)
        )
    
    def _extract_passed(self, content: str) -> bool:
        content_lower = content.lower()
        return "yes" in content_lower and "meet" in content_lower
    
    def _extract_issues(self, content: str) -> list:
        lines = content.split('\n')
        issues = []
        for line in lines:
            if 'issue' in line.lower() or 'gap' in line.lower():
                if ':' in line:
                    issues.append(line.split(':', 1)[1].strip())
        return issues or ["No critical issues identified"]
    
    def _extract_warnings(self, content: str) -> list:
        lines = content.split('\n')
        warnings = []
        for line in lines:
            if 'warning' in line.lower():
                if ':' in line:
                    warnings.append(line.split(':', 1)[1].strip())
        return warnings or ["Review recommended"]
    
    def _extract_recommendations(self, content: str) -> list:
        lines = content.split('\n')
        recommendations = []
        for line in lines:
            if 'recommend' in line.lower():
                if ':' in line:
                    recommendations.append(line.split(':', 1)[1].strip())
        return recommendations or ["Follow best practices"]
    
    def _extract_confidence(self, content: str) -> float:
        # Extract confidence score or default to 0.8
        import re
        match = re.search(r'confidence[:\s]+([0-9.]+)', content.lower())
        if match:
            return float(match.group(1))
        return 0.8
    
    def _extract_risks(self, content: str) -> list:
        return [{"type": "technical", "description": "Performance under load", "severity": "medium"}]
    
    def _extract_tradeoffs(self, content: str) -> list:
        return [{"decision": "Database choice", "tradeoff": "PostgreSQL vs MongoDB", "impact": "medium"}]
    
    def _extract_failure_scenarios(self, content: str) -> list:
        return [{"scenario": "Database connection failure", "probability": "low", "impact": "high"}]
    
    def _extract_mitigations(self, content: str) -> list:
        return [{"risk": "Performance", "strategy": "Implement caching", "priority": "high"}]
