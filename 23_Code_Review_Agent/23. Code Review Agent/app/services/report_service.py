import os
from fpdf import FPDF
from app.models import ReviewResponse

class ReportService:
    def generate_report(self, review: ReviewResponse, format: str = "txt") -> str:
        if format.lower() == "pdf":
            return self._generate_pdf(review)
        else:
            return self._generate_txt(review)

    def _generate_txt(self, review: ReviewResponse) -> str:
        lines = []
        lines.append("CODE REVIEW REPORT")
        lines.append("==================")
        lines.append(f"Summary: {review.summary}\n")
        
        lines.append("ISSUES")
        lines.append("------")
        if not review.issues:
            lines.append("No issues found.")
        for issue in review.issues:
            lines.append(f"[{issue.severity.upper()}] {issue.category}: {issue.description}")
            if issue.line_number:
                lines.append(f"  Line: {issue.line_number}")
            lines.append(f"  Suggestion: {issue.suggestion}\n")
            
        lines.append("COMPLEXITY")
        lines.append("----------")
        lines.append(f"Time Complexity: {review.complexity.time_complexity}")
        lines.append(f"Space Complexity: {review.complexity.space_complexity}")
        if review.complexity.cyclomatic_complexity is not None:
            lines.append(f"Cyclomatic Complexity: {review.complexity.cyclomatic_complexity}")
        if review.complexity.maintainability_index is not None:
            lines.append(f"Maintainability Index: {review.complexity.maintainability_index:.2f}")
        lines.append("")

        if review.efficiency_recommendations:
            lines.append("EFFICIENCY RECOMMENDATIONS")
            lines.append("--------------------------")
            for rec in review.efficiency_recommendations:
                lines.append(f"- {rec}")
            lines.append("")

        if review.style_suggestions:
            lines.append("STYLE SUGGESTIONS")
            lines.append("-----------------")
            for sugg in review.style_suggestions:
                lines.append(f"- {sugg}")
            lines.append("")
            
        if review.refactoring_suggestions:
            lines.append("REFACTORING SUGGESTIONS")
            lines.append("-----------------------")
            for ref in review.refactoring_suggestions:
                lines.append(f"Description: {ref.description}")
                lines.append(f"Explanation: {ref.explanation}")
                if ref.original_code:
                    lines.append("Original Code:")
                    lines.append(ref.original_code)
                lines.append("Refactored Code:")
                lines.append(ref.refactored_code)
                lines.append("")
                
        return "\n".join(lines)

    def _generate_pdf(self, review: ReviewResponse) -> str:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Code Review Report", ln=True, align='C')
        pdf.ln(10)
        
        # Summary
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Summary", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=review.summary)
        pdf.ln(5)
        
        # Issues
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Issues", ln=True)
        pdf.set_font("Arial", size=10)
        if not review.issues:
            pdf.cell(200, 10, txt="No issues found.", ln=True)
        for issue in review.issues:
            severity_color = (0, 0, 0)
            if issue.severity.lower() == 'major':
                severity_color = (255, 0, 0)
            elif issue.severity.lower() == 'medium':
                severity_color = (255, 165, 0)
            
            pdf.set_text_color(*severity_color)
            pdf.multi_cell(0, 10, txt=f"[{issue.severity.upper()}] {issue.category}: {issue.description}")
            pdf.set_text_color(0, 0, 0)
            
            if issue.line_number:
                pdf.cell(200, 10, txt=f"  Line: {issue.line_number}", ln=True)
            pdf.multi_cell(0, 10, txt=f"  Suggestion: {issue.suggestion}")
            pdf.ln(2)
            
        # Complexity
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Complexity", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Time Complexity: {review.complexity.time_complexity}", ln=True)
        pdf.cell(200, 10, txt=f"Space Complexity: {review.complexity.space_complexity}", ln=True)
        if review.complexity.cyclomatic_complexity is not None:
            pdf.cell(200, 10, txt=f"Cyclomatic Complexity: {review.complexity.cyclomatic_complexity}", ln=True)
        if review.complexity.maintainability_index is not None:
            pdf.cell(200, 10, txt=f"Maintainability Index: {review.complexity.maintainability_index:.2f}", ln=True)
            
        # Other sections... (simplified for brevity)
        if review.efficiency_recommendations:
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt="Efficiency Recommendations", ln=True)
            pdf.set_font("Arial", size=10)
            for rec in review.efficiency_recommendations:
                pdf.multi_cell(0, 10, txt=f"- {rec}")

        # Save to a temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf.output(tmp.name)
            return tmp.name
