from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class RequirementType(str, Enum):
    GREENFIELD = "greenfield"
    BROWNFIELD = "brownfield"
    AMBIGUOUS = "ambiguous"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class Requirement(BaseModel):
    original: str
    normalized: Optional[str] = None
    type: Optional[RequirementType] = None
    ambiguities: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)


class Task(BaseModel):
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = Field(default_factory=list)
    estimated_effort: Optional[str] = None
    outputs: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Workflow(BaseModel):
    id: str
    requirement: Requirement
    tasks: List[Task]
    current_step: int = 0
    status: TaskStatus = TaskStatus.PENDING
    artifacts: Dict[str, Any] = Field(default_factory=dict)


class CodebaseAnalysis(BaseModel):
    impacted_services: List[str] = Field(default_factory=list)
    impacted_modules: List[str] = Field(default_factory=list)
    api_changes: List[str] = Field(default_factory=list)
    data_flow_changes: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)


class EngineeringOutput(BaseModel):
    code: Dict[str, str] = Field(default_factory=dict)
    tests: Dict[str, str] = Field(default_factory=dict)
    documentation: Dict[str, str] = Field(default_factory=dict)
    api_contracts: Dict[str, str] = Field(default_factory=dict)
    schemas: Dict[str, str] = Field(default_factory=dict)


class ValidationResult(BaseModel):
    passed: bool
    issues: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    confidence_score: float = 0.0


class RiskAssessment(BaseModel):
    risks: List[Dict[str, Any]] = Field(default_factory=list)
    trade_offs: List[Dict[str, Any]] = Field(default_factory=list)
    failure_scenarios: List[Dict[str, Any]] = Field(default_factory=list)
    mitigation_strategies: List[Dict[str, Any]] = Field(default_factory=list)


class ExecutionSummary(BaseModel):
    implementation_plan: str
    rationale: str
    artifacts: Dict[str, Any]
    risks: RiskAssessment
    validation_approach: str
    assumptions: List[str]
    limitations: List[str]
