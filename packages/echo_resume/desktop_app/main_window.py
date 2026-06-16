"""PySide6 desktop interface for Echo."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from packages.echo_core.domain.profile import FactType, PersonalFact, Visibility
from packages.echo_core.profile_schema import import_profile_json
from packages.echo_core.repositories.sqlite import SQLiteProfileRepository
from packages.echo_resume.domain import JobAnalysis
from packages.echo_resume.fit_scoring import FitScore, score_job_fit
from packages.echo_resume.latex_generator import render_resume
from packages.echo_resume.resume_generator import ResumeGenerator


class EchoMainWindow:
    """Factory wrapper so PySide6 remains an optional import at module import time."""

    def __new__(cls, repository: SQLiteProfileRepository, data_root: Path):  # type: ignore[no-untyped-def]
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import (
            QCheckBox,
            QComboBox,
            QFileDialog,
            QFrame,
            QGridLayout,
            QHBoxLayout,
            QLabel,
            QListWidget,
            QListWidgetItem,
            QMainWindow,
            QMessageBox,
            QAbstractItemView,
            QPushButton,
            QStackedWidget,
            QTextEdit,
            QVBoxLayout,
            QWidget,
        )

        class _Window(QMainWindow):
            def __init__(self) -> None:
                super().__init__()
                self.repository = repository
                self.data_root = data_root
                self.current_fit: FitScore | None = None
                self.selected_fact: PersonalFact | None = None
                self.setWindowTitle("Echo")
                self.setMinimumSize(1180, 760)
                self._build_ui()
                self.refresh_profile()

            def _build_ui(self) -> None:
                root = QWidget()
                layout = QHBoxLayout(root)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

                sidebar = QFrame()
                sidebar.setObjectName("sidebar")
                sidebar_layout = QVBoxLayout(sidebar)
                title = QLabel("Echo")
                title.setObjectName("brand")
                sidebar_layout.addWidget(title)

                self.nav = QListWidget()
                for label in (
                    "Dashboard",
                    "Echo Profile",
                    "Echo Resume",
                    "Fit Scoring",
                    "Applications",
                    "Settings",
                ):
                    self.nav.addItem(label)
                self.nav.currentRowChanged.connect(self._show_page)
                sidebar_layout.addWidget(self.nav)
                sidebar_layout.addStretch()
                sidebar_layout.addWidget(QLabel("Local Mode\nAll data stays on your device"))

                self.stack = QStackedWidget()
                self.dashboard_page = self._dashboard()
                self.profile_page = self._profile()
                self.resume_page = self._resume()
                self.fit_page = self._fit()
                self.applications_page = self._placeholder("Applications", "Saved application history will appear here.")
                self.settings_page = self._placeholder("Settings", f"Private data path:\n{self.data_root}")
                for page in (
                    self.dashboard_page,
                    self.profile_page,
                    self.resume_page,
                    self.fit_page,
                    self.applications_page,
                    self.settings_page,
                ):
                    self.stack.addWidget(page)

                layout.addWidget(sidebar, 1)
                layout.addWidget(self.stack, 5)
                self.setCentralWidget(root)
                self.nav.setCurrentRow(0)
                self.setStyleSheet(STYLESHEET)

            def _show_page(self, index: int) -> None:
                self.stack.setCurrentIndex(index)

            def _placeholder(self, title: str, body: str) -> QWidget:
                page = QWidget()
                layout = QVBoxLayout(page)
                layout.addWidget(self._heading(title, body))
                layout.addStretch()
                return page

            def _heading(self, title: str, subtitle: str) -> QWidget:
                widget = QWidget()
                layout = QVBoxLayout(widget)
                label = QLabel(title)
                label.setObjectName("pageTitle")
                sublabel = QLabel(subtitle)
                sublabel.setObjectName("subtitle")
                layout.addWidget(label)
                layout.addWidget(sublabel)
                return widget

            def _dashboard(self) -> QWidget:
                page = QWidget()
                layout = QVBoxLayout(page)
                layout.addWidget(self._heading("Dashboard", "Overview of your profile and resume readiness."))
                cards = QGridLayout()
                self.verified_count = QLabel("0")
                self.resume_count = QLabel("0")
                self.public_count = QLabel("0")
                cards.addWidget(self._stat_card("Verified Facts", self.verified_count), 0, 0)
                cards.addWidget(self._stat_card("Resume Facts", self.resume_count), 0, 1)
                cards.addWidget(self._stat_card("Public Facts", self.public_count), 0, 2)
                layout.addLayout(cards)
                self.dashboard_recent = QTextEdit()
                self.dashboard_recent.setReadOnly(True)
                layout.addWidget(self.dashboard_recent)
                return page

            def _stat_card(self, label: str, value: QLabel) -> QWidget:
                card = QFrame()
                card.setObjectName("card")
                layout = QVBoxLayout(card)
                layout.addWidget(QLabel(label))
                value.setObjectName("stat")
                layout.addWidget(value)
                return card

            def _profile(self) -> QWidget:
                page = QWidget()
                layout = QVBoxLayout(page)
                top = QHBoxLayout()
                top.addWidget(self._heading("Echo Profile", "Add verified facts for RAG, resume tailoring, and public export."))
                import_button = QPushButton("Import Resume")
                import_button.clicked.connect(self.import_resume)
                top.addWidget(import_button)
                layout.addLayout(top)

                form = QGridLayout()
                self.fact_type = QComboBox()
                for item in FactType:
                    self.fact_type.addItem(item.value, item)
                self.visibility = QComboBox()
                for item in Visibility:
                    self.visibility.addItem(item.value, item)
                self.fact_text = QTextEdit()
                self.fact_text.setPlaceholderText("Add one verified career fact, project bullet, skill, achievement, or preference.")
                self.verified = QCheckBox("Verified")
                self.verified.setChecked(True)
                self.save_fact_button = QPushButton("Add Fact")
                self.save_fact_button.clicked.connect(self.save_fact)
                new_button = QPushButton("New")
                new_button.clicked.connect(self.clear_fact_form)
                delete_button = QPushButton("Delete Selected")
                delete_button.clicked.connect(self.delete_selected_fact)
                form.addWidget(QLabel("Type"), 0, 0)
                form.addWidget(self.fact_type, 0, 1)
                form.addWidget(QLabel("Visibility"), 0, 2)
                form.addWidget(self.visibility, 0, 3)
                form.addWidget(self.verified, 0, 4)
                form.addWidget(self.fact_text, 1, 0, 1, 5)
                form.addWidget(new_button, 2, 2)
                form.addWidget(delete_button, 2, 3)
                form.addWidget(self.save_fact_button, 2, 4)
                layout.addLayout(form)

                self.profile_facts = QListWidget()
                self.profile_facts.setSelectionMode(QAbstractItemView.ExtendedSelection)
                self.profile_facts.itemSelectionChanged.connect(self.load_selected_fact)
                layout.addWidget(self.profile_facts)
                bulk = QHBoxLayout()
                verify_selected = QPushButton("Verify Selected for Resume")
                verify_selected.clicked.connect(self.verify_selected_for_resume)
                private_selected = QPushButton("Mark Selected Private")
                private_selected.clicked.connect(self.mark_selected_private)
                bulk.addWidget(verify_selected)
                bulk.addWidget(private_selected)
                layout.addLayout(bulk)
                return page

            def _resume(self) -> QWidget:
                page = QWidget()
                layout = QVBoxLayout(page)
                layout.addWidget(self._heading("Echo Resume", "Paste a job post, score fit, select evidence, and preview a tailored resume."))
                self.job_posting = QTextEdit()
                self.job_posting.setPlaceholderText("Paste job description here...")
                layout.addWidget(self.job_posting)
                analyze = QPushButton("Analyze Job")
                analyze.clicked.connect(self.analyze_job)
                layout.addWidget(analyze, alignment=Qt.AlignRight)
                self.evidence_list = QListWidget()
                layout.addWidget(QLabel("Evidence Review"))
                layout.addWidget(self.evidence_list)
                generate = QPushButton("Generate Resume Preview")
                generate.clicked.connect(self.generate_resume)
                layout.addWidget(generate, alignment=Qt.AlignRight)
                self.resume_preview = QTextEdit()
                self.resume_preview.setReadOnly(True)
                layout.addWidget(QLabel("Resume Preview"))
                layout.addWidget(self.resume_preview)
                return page

            def _fit(self) -> QWidget:
                page = QWidget()
                layout = QVBoxLayout(page)
                layout.addWidget(self._heading("Fit Scoring", "See how your verified profile matches the pasted job post."))
                self.fit_score_label = QLabel("No job analyzed yet.")
                self.fit_score_label.setObjectName("fitScore")
                self.fit_details = QTextEdit()
                self.fit_details.setReadOnly(True)
                layout.addWidget(self.fit_score_label)
                layout.addWidget(self.fit_details)
                return page

            def refresh_profile(self) -> None:
                facts = self.repository.list_verified()
                resume_facts = self.repository.list_resume_eligible()
                public_facts = self.repository.list_public()
                self.verified_count.setText(str(len(facts)))
                self.resume_count.setText(str(len(resume_facts)))
                self.public_count.setText(str(len(public_facts)))
                self.profile_facts.clear()
                for fact in self.repository.list_all():
                    status = "verified" if fact.verified else "draft"
                    item = QListWidgetItem(
                        f"[{status}] [{fact.fact_type.value}] {fact.text} ({fact.visibility.value})"
                    )
                    item.setData(Qt.UserRole, fact)
                    self.profile_facts.addItem(item)
                self.dashboard_recent.setPlainText(
                    "\n".join(f"- {fact.text}" for fact in facts[-8:])
                    or "Add verified facts in Echo Profile to get started."
                )

            def _set_combo_value(self, combo: QComboBox, value: object) -> None:
                for index in range(combo.count()):
                    if combo.itemData(index) == value:
                        combo.setCurrentIndex(index)
                        return

            def load_selected_fact(self) -> None:
                selected = self.profile_facts.selectedItems()
                if not selected or len(selected) > 1:
                    return
                fact = selected[0].data(Qt.UserRole)
                if not isinstance(fact, PersonalFact):
                    return
                self.selected_fact = fact
                self.fact_text.setPlainText(fact.text)
                self._set_combo_value(self.fact_type, fact.fact_type)
                self._set_combo_value(self.visibility, fact.visibility)
                self.verified.setChecked(fact.verified)
                self.save_fact_button.setText("Save Changes")

            def clear_fact_form(self) -> None:
                self.selected_fact = None
                self.profile_facts.blockSignals(True)
                self.profile_facts.clearSelection()
                self.profile_facts.blockSignals(False)
                self.fact_text.clear()
                self._set_combo_value(self.fact_type, FactType.WORK)
                self._set_combo_value(self.visibility, Visibility.PRIVATE)
                self.verified.setChecked(True)
                self.save_fact_button.setText("Add Fact")

            def save_fact(self) -> None:
                text = self.fact_text.toPlainText().strip()
                if not text:
                    QMessageBox.warning(self, "Missing fact", "Add a profile fact first.")
                    return
                existing = self.selected_fact
                fact_data = {
                    "text": text,
                    "fact_type": self.fact_type.currentData(),
                    "verified": self.verified.isChecked(),
                    "visibility": self.visibility.currentData(),
                    "source": existing.source if existing else "manual",
                    "created_at": existing.created_at if existing else datetime.now(UTC),
                    "updated_at": datetime.now(UTC),
                }
                if existing:
                    fact_data["id"] = existing.id
                fact = PersonalFact(**fact_data)
                self.repository.save(fact)
                self.clear_fact_form()
                self.refresh_profile()

            def delete_selected_fact(self) -> None:
                selected_facts = self._selected_facts()
                if not selected_facts:
                    QMessageBox.information(self, "No selection", "Select a fact to delete.")
                    return
                for fact in selected_facts:
                    self.repository.delete(fact.id)
                self.clear_fact_form()
                self.refresh_profile()

            def _selected_facts(self) -> list[PersonalFact]:
                facts: list[PersonalFact] = []
                for item in self.profile_facts.selectedItems():
                    fact = item.data(Qt.UserRole)
                    if isinstance(fact, PersonalFact):
                        facts.append(fact)
                return facts

            def verify_selected_for_resume(self) -> None:
                selected = self._selected_facts()
                if not selected:
                    QMessageBox.information(self, "No selection", "Select one or more draft facts.")
                    return
                for fact in selected:
                    self.repository.save(
                        PersonalFact(
                            id=fact.id,
                            text=fact.text,
                            fact_type=fact.fact_type,
                            verified=True,
                            visibility=Visibility.RESUME_ALLOWED,
                            source=fact.source,
                            created_at=fact.created_at,
                            updated_at=datetime.now(UTC),
                        )
                    )
                self.clear_fact_form()
                self.refresh_profile()

            def mark_selected_private(self) -> None:
                selected = self._selected_facts()
                if not selected:
                    QMessageBox.information(self, "No selection", "Select one or more facts.")
                    return
                for fact in selected:
                    self.repository.save(
                        PersonalFact(
                            id=fact.id,
                            text=fact.text,
                            fact_type=fact.fact_type,
                            verified=False,
                            visibility=Visibility.PRIVATE,
                            source=fact.source,
                            created_at=fact.created_at,
                            updated_at=datetime.now(UTC),
                        )
                    )
                self.clear_fact_form()
                self.refresh_profile()

            def import_resume(self) -> None:
                path, _ = QFileDialog.getOpenFileName(
                    self,
                    "Import resume, profile JSON, text, LaTeX, or PDF",
                    "",
                    "Profile and resume files (*.json *.pdf *.tex *.txt *.md);;All files (*)",
                )
                if not path:
                    return
                if Path(path).suffix.lower() == ".json":
                    self.import_profile_json(Path(path))
                    return
                try:
                    content = self._read_resume_file(Path(path))
                except Exception as exc:
                    QMessageBox.warning(self, "Import failed", str(exc))
                    return
                imported = 0
                for line in content.splitlines():
                    cleaned = line.strip().strip("-* ")
                    if len(cleaned) < 20 or cleaned.startswith("\\"):
                        continue
                    self.repository.save(
                        PersonalFact(
                            text=cleaned,
                            fact_type=FactType.RESUME_BULLET,
                            verified=False,
                            visibility=Visibility.PRIVATE,
                            source=f"import:{Path(path).name}",
                        )
                    )
                    imported += 1
                self.refresh_profile()
                QMessageBox.information(
                    self,
                    "Resume imported",
                    f"Imported {imported} draft facts. Review and verify them before use.",
                )

            def _read_resume_file(self, path: Path) -> str:
                if path.suffix.lower() == ".pdf":
                    from PyPDF2 import PdfReader

                    reader = PdfReader(str(path))
                    return "\n".join(
                        page.extract_text() or "" for page in reader.pages
                    )
                return path.read_text(encoding="utf-8", errors="ignore")

            def import_profile_json(self, path: Path) -> None:
                try:
                    facts = import_profile_json(path)
                except Exception as exc:
                    QMessageBox.warning(self, "JSON import failed", str(exc))
                    return
                for fact in facts:
                    self.repository.save(fact)
                self.refresh_profile()
                QMessageBox.information(
                    self,
                    "Profile JSON imported",
                    f"Imported {len(facts)} typed draft facts. Select one or more and verify them when ready.",
                )

            def analyze_job(self) -> None:
                text = self.job_posting.toPlainText().strip()
                if not text:
                    QMessageBox.warning(self, "Missing job post", "Paste a job post first.")
                    return
                facts = self.repository.list_resume_eligible()
                self.current_fit = score_job_fit(text, facts)
                self.fit_score_label.setText(f"{self.current_fit.score}/100 fit score")
                self.fit_details.setPlainText(
                    "Matched terms:\n"
                    + ", ".join(self.current_fit.matched_terms or ("None",))
                    + "\n\nMissing terms:\n"
                    + ", ".join(self.current_fit.missing_terms or ("None",))
                    + "\n\nStrong evidence:\n"
                    + "\n".join(f"- {fact.text}" for fact in self.current_fit.strong_evidence)
                )
                self.evidence_list.clear()
                for fact in self.current_fit.strong_evidence:
                    item = QListWidgetItem(fact.text)
                    item.setData(Qt.UserRole, fact)
                    item.setCheckState(Qt.Checked)
                    self.evidence_list.addItem(item)
                self.nav.setCurrentRow(3)

            def generate_resume(self) -> None:
                selected: list[PersonalFact] = []
                for index in range(self.evidence_list.count()):
                    item = self.evidence_list.item(index)
                    if item.checkState() == Qt.Checked:
                        selected.append(item.data(Qt.UserRole))
                if not selected:
                    QMessageBox.warning(self, "No evidence selected", "Select evidence first.")
                    return
                draft = ResumeGenerator().generate(
                    JobAnalysis(company="Target Company", role="Tailored Role"),
                    selected,
                )
                self.resume_preview.setPlainText(render_resume(draft))
                self.nav.setCurrentRow(2)

        return _Window()


STYLESHEET = """
QMainWindow, QWidget {
    background: #F7FBF8;
    color: #102A1F;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
#sidebar {
    background: #FFFFFF;
    border-right: 1px solid #DCEFE3;
}
#brand {
    color: #15803D;
    font-size: 22px;
    font-weight: 700;
    padding: 20px 16px;
}
QListWidget {
    border: none;
    background: transparent;
}
QListWidget::item {
    padding: 10px 12px;
    border-radius: 8px;
}
QListWidget::item:selected {
    background: #EAF7EE;
    color: #15803D;
}
#pageTitle {
    font-size: 24px;
    font-weight: 700;
}
#subtitle {
    color: #5C6F64;
}
#card {
    background: #FFFFFF;
    border: 1px solid #DCEFE3;
    border-radius: 14px;
    padding: 18px;
}
#stat, #fitScore {
    font-size: 32px;
    font-weight: 700;
    color: #15803D;
}
QPushButton {
    background: #15803D;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 9px 14px;
}
QPushButton:hover {
    background: #166534;
}
QTextEdit, QComboBox {
    background: #FFFFFF;
    border: 1px solid #DCEFE3;
    border-radius: 8px;
    padding: 8px;
}
"""
