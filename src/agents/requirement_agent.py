from typing import Optional
from anthropic import Anthropic
from src.models import Requirement, RequirementType
import os


class RequirementUnderstandingAgent:
    """Analyzes requirements to understand intent and identify ambiguities."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    
    def analyze(self, requirement_text: str) -> Requirement:
        """Analyze a requirement and normalize it."""
        
        prompt = f"""Analyze the following software requirement and provide:
1. Normalized requirement (clear, specific, actionable)
2. Requirement type (greenfield, brownfield, or ambiguous)
3. List of ambiguities or unclear aspects
4. List of necessary assumptions
5. Key context information

Requirement: "{requirement_text}"

Provide your response in a structured format."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        
        # Parse the response (in production, use structured output)
        requirement = Requirement(
            original=requirement_text,
            normalized=self._extract_normalized(content),
            type=self._extract_type(content),
            ambiguities=self._extract_ambiguities(content),
            assumptions=self._extract_assumptions(content),
            context={"raw_analysis": content}
        )
        
        return requirement
    
    def _extract_normalized(self, content: str) -> str:
        """Extract normalized requirement from analysis."""
        lines = content.split('\n')
        for line in lines:
            if 'normalized' in line.lower() or 'clear requirement' in line.lower():
                return line.split(':', 1)[1].strip() if ':' in line else line.strip()
        return content[:200]  # Fallback
    
    def _extract_type(self, content: str) -> RequirementType:
        """Extract requirement type from analysis."""
        content_lower = content.lower()
        if 'brownfield' in content_lower or 'existing' in content_lower or 'modify' in content_lower:
            return RequirementType.BROWNFIELD
        elif 'ambiguous' in content_lower or 'unclear' in content_lower:
            return RequirementType.AMBIGUOUS
        return RequirementType.GREENFIELD
    
    def _extract_ambiguities(self, content: str) -> list:
        """Extract ambiguities from analysis."""
        lines = content.split('\n')
        ambiguities = []
        capture = False
        for line in lines:
            if 'ambiguit' in line.lower():
                capture = True
                continue
            if capture and line.strip():
                if line.startswith('-') or line.startswith('*'):
                    ambiguities.append(line.strip()[1:].strip())
                elif ':' in line:
                    ambiguities.append(line.split(':', 1)[1].strip())
        return ambiguities
    
    def _extract_assumptions(self, content: str) -> list:
        """Extract assumptions from analysis."""
        lines = content.split('\n')
        assumptions = []
        capture = False
        for line in lines:
            if 'assumption' in line.lower():
                capture = True
                continue
            if capture and line.strip():
                if line.startswith('-') or line.startswith('*'):
                    assumptions.append(line.strip()[1:].strip())
                elif ':' in line:
                    assumptions.append(line.split(':', 1)[1].strip())
        return assumptions
