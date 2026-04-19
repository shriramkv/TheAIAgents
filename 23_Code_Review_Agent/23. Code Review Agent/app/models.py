from typing import List, Optional
from pydantic import BaseModel, Field

class ReviewRequest(BaseModel):
    code: str
    language: str = "python"
    filename: Optional[str] = None

class Issue(BaseModel):
    category: str = Field(..., description="Category of the issue (e.g., SOLID, Logic, Style)")
    description: str
    line_number: Optional[int] = None
    severity: str = Field(..., description="major, medium, or minor")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    suggestion: Optional[str] = None

class ComplexityAnalysis(BaseModel):
    time_complexity: str
    space_complexity: str
    cyclomatic_complexity: Optional[int] = None
    maintainability_index: Optional[float] = None

class RefactoringSuggestion(BaseModel):
    description: str
    original_code: Optional[str] = None
    refactored_code: str
    explanation: str

class ReviewResponse(BaseModel):
    issues: List[Issue]
    complexity: ComplexityAnalysis
    efficiency_recommendations: List[str]
    style_suggestions: List[str]
    refactoring_suggestions: List[RefactoringSuggestion]
    summary: str
