from pathlib import Path
import re


class SOPRetriever:
    def __init__(self, sop_directory="sops"):
        self.sop_directory = Path(sop_directory)
        self.documents = []

        self.load_documents()

    def load_documents(self):
        """Load all SOP markdown files."""

        self.documents = []

        for file_path in self.sop_directory.glob("*.md"):
            content = file_path.read_text(encoding="utf-8")

            document = self.parse_document(
                file_path.name,
                content
            )

            self.documents.append(document)

    def parse_document(self, filename, content):
        """Extract basic metadata from SOP."""

        document_id = self.extract_field(
            content,
            "SOP"
        )

        title = self.extract_field(
            content,
            "Title"
        )

        category = self.extract_field(
            content,
            "Category"
        )

        issue = self.extract_field(
            content,
            "Issue"
        )

        support_level = self.extract_field(
            content,
            "Support Level"
        )

        version = self.extract_field(
            content,
            "Version"
        )

        return {
            "filename": filename,
            "document_id": document_id,
            "title": title,
            "category": category,
            "issue": issue,
            "support_level": support_level,
            "version": version,
            "content": content
        }

    def extract_field(self, content, field):
        pattern = rf"^{field}:\s*(.+)$"

        match = re.search(
            pattern,
            content,
            re.MULTILINE | re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

        # SOP ID is in the markdown heading
        if field == "SOP":
            match = re.search(
                r"^#\s*(SOP-\d+)",
                content,
                re.MULTILINE
            )

            if match:
                return match.group(1)

        return ""

    def get_categories(self):
        return sorted(
            list(
                set(
                    doc["category"]
                    for doc in self.documents
                )
            )
        )

    def get_issues(self, category):
        return sorted(
            list(
                set(
                    doc["issue"]
                    for doc in self.documents
                    if doc["category"] == category
                )
            )
        )

    def get_by_issue(self, category, issue):
        """Exact retrieval using category + issue."""

        results = [
            doc
            for doc in self.documents
            if doc["category"] == category
            and doc["issue"] == issue
        ]

        return results

    def search(self, query, top_k=3):
        """Simple keyword-based retrieval."""

        query_words = set(
            query.lower().split()
        )

        scored_documents = []

        for doc in self.documents:

            searchable_text = " ".join([
                doc["title"],
                doc["category"],
                doc["issue"],
                doc["content"]
            ]).lower()

            score = 0

            for word in query_words:
                if len(word) > 2 and word in searchable_text:
                    score += 1

            if score > 0:
                scored_documents.append(
                    (score, doc)
                )

        scored_documents.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            doc
            for score, doc in scored_documents[:top_k]
        ]