import os
import json
import logging
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any


@dataclass
class Issue:
    id: str
    title: str
    description: str
    severity: str  # "high", "medium", "low"
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    recommendation: Optional[str] = None
    category: str = "general"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class IssueManager:
    def __init__(self):
        self.issues: List[Issue] = []
        self.logger = logging.getLogger(__name__)

    def add_issue(self, issue: Issue) -> None:
        """Add a new issue to the issue list"""
        self.issues.append(issue)
        self.logger.info(f"Added issue: {issue.title} ({issue.severity})")

    def add_issues_from_list(self, issues_list: List[Dict[str, Any]]) -> None:
        """Add multiple issues from a list of dictionaries"""
        for issue_data in issues_list:
            try:
                issue = Issue(**issue_data)
                self.add_issue(issue)
            except Exception as e:
                self.logger.error(f"Failed to add issue: {e}")

    def get_all_issues(self) -> List[Dict[str, Any]]:
        """Get all issues as a list of dictionaries"""
        return [issue.to_dict() for issue in self.issues]

    def get_issues_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """Get issues filtered by severity level"""
        return [issue.to_dict() for issue in self.issues if issue.severity == severity]

    def get_issues_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get issues filtered by category"""
        return [issue.to_dict() for issue in self.issues if issue.category == category]

    def clear_issues(self) -> None:
        """Clear all issues"""
        self.issues = []
        self.logger.info("Cleared all issues")

    def save_to_file(self, filepath: str) -> bool:
        """Save issues to a JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.get_all_issues(), f, indent=2)
            self.logger.info(f"Saved {len(self.issues)} issues to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save issues to file: {e}")
            return False

    def load_from_file(self, filepath: str) -> bool:
        """Load issues from a JSON file"""
        try:
            if not os.path.exists(filepath):
                self.logger.warning(f"File {filepath} does not exist")
                return False

            with open(filepath, 'r') as f:
                issues_data = json.load(f)

            self.clear_issues()
            self.add_issues_from_list(issues_data)

            self.logger.info(
                f"Loaded {len(self.issues)} issues from {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load issues from file: {e}")
            return False

    def generate_report(self) -> Dict[str, Any]:
        """Generate a summary report of issues"""
        high_severity = len([i for i in self.issues if i.severity == "high"])
        medium_severity = len(
            [i for i in self.issues if i.severity == "medium"])
        low_severity = len([i for i in self.issues if i.severity == "low"])

        categories = {}
        for issue in self.issues:
            if issue.category not in categories:
                categories[issue.category] = 0
            categories[issue.category] += 1

        return {
            "total_issues": len(self.issues),
            "severity_counts": {
                "high": high_severity,
                "medium": medium_severity,
                "low": low_severity
            },
            "category_counts": categories
        }
