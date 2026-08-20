from pathlib import Path


class SOPRetriever:

    def __init__(self, sop_directory="sops"):

        self.sop_directory = Path(
            sop_directory
        )

        self.documents = []

        self.load_documents()


    # ========================================================
    # LOAD SOP DOCUMENTS
    # ========================================================

    def load_documents(self):

        self.documents = []


        if not self.sop_directory.exists():

            return


        for file_path in sorted(
            self.sop_directory.glob("*.md")
        ):

            try:

                content = file_path.read_text(
                    encoding="utf-8"
                )

                document = self.parse_document(
                    file_path,
                    content
                )

                self.documents.append(
                    document
                )

            except Exception as e:

                print(
                    f"Unable to load {file_path}: {e}"
                )


    # ========================================================
    # PARSE SOP
    # ========================================================

    def parse_document(
        self,
        file_path,
        content
    ):

        lines = content.splitlines()


        document_id = file_path.stem

        title = file_path.stem

        category = "General"

        issue = "General Banking Issue"

        support_level = "L1"

        version = "1.0"


        # ----------------------------------------------------
        # Parse metadata
        # ----------------------------------------------------

        for line in lines:

            clean = line.strip()


            if clean.startswith(
                "Document ID:"
            ):

                document_id = (
                    clean.split(
                        ":", 1
                    )[1].strip()
                )


            elif clean.startswith(
                "Title:"
            ):

                title = (
                    clean.split(
                        ":", 1
                    )[1].strip()
                )


            elif clean.startswith(
                "Category:"
            ):

                category = (
                    clean.split(
                        ":", 1
                    )[1].strip()
                )


            elif clean.startswith(
                "Issue:"
            ):

                issue = (
                    clean.split(
                        ":", 1
                    )[1].strip()
                )


            elif clean.startswith(
                "Support Level:"
            ):

                support_level = (
                    clean.split(
                        ":", 1
                    )[1].strip()
                )


            elif clean.startswith(
                "Version:"
            ):

                version = (
                    clean.split(
                        ":", 1
                    )[1].strip()
                )


        return {

            "document_id": document_id,

            "title": title,

            "category": category,

            "issue": issue,

            "support_level": support_level,

            "version": version,

            "content": content,

            "file": str(file_path)

        }


    # ========================================================
    # CATEGORIES
    # ========================================================

    def get_categories(self):

        categories = set()


        for document in self.documents:

            categories.add(
                document["category"]
            )


        return sorted(
            categories
        )


    # ========================================================
    # ISSUES
    # ========================================================

    def get_issues(
        self,
        category
    ):

        issues = []


        for document in self.documents:

            if (
                document["category"]
                .lower()
                ==
                category.lower()
            ):

                issues.append(
                    document["issue"]
                )


        return sorted(
            set(issues)
        )


    # ========================================================
    # FIND BY ISSUE
    # ========================================================

    def get_by_issue(
        self,
        category,
        issue
    ):

        results = []


        for document in self.documents:

            if (
                document["category"]
                .lower()
                ==
                category.lower()
                and
                document["issue"]
                .lower()
                ==
                issue.lower()
            ):

                results.append(
                    document
                )


        return results


    # ========================================================
    # SIMPLE SEARCH
    # ========================================================

    def search(
        self,
        query,
        top_k=3
    ):

        query_words = set(
            query.lower()
            .split()
        )


        scored_documents = []


        for document in self.documents:

            text = (
                document["title"]
                + " "
                + document["category"]
                + " "
                + document["issue"]
                + " "
                + document["content"]
            ).lower()


            score = 0


            for word in query_words:

                if len(word) < 3:

                    continue


                if word in text:

                    score += 1


            if score > 0:

                scored_documents.append(
                    (
                        score,
                        document
                    )
                )


        scored_documents.sort(
            key=lambda x: x[0],
            reverse=True
        )


        return [
            document
            for score, document
            in scored_documents[:top_k]
        ]