"""SQL配置と説明コメントの回帰を実際のsourceで検査する。"""

from __future__ import annotations

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

from test_qualityflow import ROOT, qualityflow


class SourceConventionsTest(unittest.TestCase):
    """導入時の配置違反と言語の生成元修正を確認する。"""

    def setUp(self) -> None:
        """API別SQLを持つ最小のrepositoryを用意する。"""
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".git").mkdir()
        (self.root / "tools").mkdir()
        shutil.copyfile(ROOT / "tools/safe_io.py", self.root / "tools/safe_io.py")
        self.app = self.root / "src/app"
        self.operation = self.app / "apis/items/create"
        (self.operation / "sql").mkdir(parents=True)
        (self.operation / "generated").mkdir()
        self.write("router.py", "# itemを作成するAPI。\n")
        self.write("functions.py", 'def create():\n    """itemを保存する。"""\n    return None\n')
        self.write("sql/001_create.sql", "-- itemを保存する。\nINSERT INTO items (id) VALUES (:id);\n")
        self.write("generated/queries.py", "# SQLとDDLから自動生成。直接編集しない。\n")

    def write(self, relative: str, content: str) -> Path:
        """fixtureをUTF-8で配置する。"""
        path = self.operation / relative
        path.write_text(content, encoding="utf-8")
        return path

    def test_japanese_source_and_operation_layout_pass(self) -> None:
        """配置と説明が正しい場合は成功する。"""
        self.assertEqual(qualityflow.source_conventions([self.app], self.app), [])

    def test_generated_english_header_fails_without_rewriting_output(self) -> None:
        """生成物の英語ヘッダーも検査から除外しない。"""
        path = self.write("generated/queries.py", "# Generated from sibling sql/*.sql and migration DDL. Do not edit.\n")
        before = path.read_bytes()
        with contextlib.redirect_stdout(io.StringIO()):
            result = qualityflow.main(["source-conventions", "--root", str(self.app)])
        self.assertEqual(result, 1)
        self.assertEqual(path.read_bytes(), before)
        self.write("generated/queries.py", "# SQLとDDLから自動生成。直接編集しない。\n")
        self.assertEqual(qualityflow.source_conventions([self.app], None), [])

    def test_english_docstring_and_sql_comment_fail(self) -> None:
        """コメントの存在だけでは言語規約を満たさない。"""
        self.write("functions.py", 'def create():\n    """Create an item."""\n    return None\n')
        self.write("sql/001_create.sql", "-- Create an item.\nINSERT INTO items (id) VALUES (:id);\n")
        findings = qualityflow.source_conventions([self.app], None)
        self.assertEqual(len(findings), 2, findings)

    def test_sql_string_is_not_a_comment(self) -> None:
        """SQL文字列中のコメント記号を誤検出しない。"""
        self.write("sql/001_create.sql", "-- itemを取得する。\nSELECT '-- English text' AS value;\n")
        self.assertEqual(qualityflow.source_conventions([self.app], None), [])

    def test_directives_and_runtime_strings_are_preserved(self) -> None:
        """機械用指示と実行時文字列は翻訳対象にしない。"""
        self.write("functions.py", '#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n# SPDX-License-Identifier: MIT\n# fmt: off\nvalue = "English runtime value"  # noqa: E501\n# fmt: on\n# pyright: ignore[reportUnknownMemberType]\n')
        self.assertEqual(qualityflow.source_conventions([self.app], None), [])

    def test_directive_does_not_hide_english_explanation(self) -> None:
        """機械用指示に付いた自然言語の理由は検査する。"""
        self.write("functions.py", 'value = None  # pyright: ignore[reportArgumentType] - trusted packaged SQL\n')
        self.assertEqual(len(qualityflow.source_conventions([self.app], None)), 1)

    def test_inline_sql_in_shared_repository_is_rejected(self) -> None:
        """API directory外の共通repositoryへの再集約も検出する。"""
        (self.app / "repository.py").write_text('def load(conn):\n    """itemを読む。"""\n    return conn.execute("SELECT id FROM items WHERE id = :id")\n', encoding="utf-8")
        findings = qualityflow.source_conventions([self.app], self.app)
        self.assertTrue(any("直書きSQLを" in item for item in findings), findings)

    def test_misplaced_sql_and_missing_generated_wrapper_fail(self) -> None:
        """共通SQL配置と型付きquery未生成を検出する。"""
        (self.operation / "sql/001_create.sql").rename(self.app / "create.sql")
        findings = qualityflow.operation_sql_findings(self.app)
        self.assertTrue(any("API別" in item for item in findings), findings)
        self.assertTrue(any("生成物" in item for item in findings), findings)

    def test_applied_migrations_outside_application_are_unchanged(self) -> None:
        """適用済みmigrationを業務SQL検査で書き換えない。"""
        path = self.root / "migrations"
        path.mkdir()
        ddl = path / "001_initial.sql"
        ddl.write_text("-- Existing migration\nCREATE TABLE items (id TEXT);\n", encoding="utf-8")
        before = ddl.read_bytes()
        self.assertEqual(qualityflow.source_conventions([self.app], self.app), [])
        self.assertEqual(ddl.read_bytes(), before)

    def test_empty_scope_fails(self) -> None:
        """空の対象を成功の証拠にしない。"""
        empty = self.root / "empty"
        empty.mkdir()
        self.assertTrue(qualityflow.source_conventions([empty], None))

    def test_declared_migration_runner_does_not_exempt_business_repository(self) -> None:
        """移行管理用SQLだけを除外し、共通業務SQLは検出する。"""
        runner = self.app / "migrate.py"
        runner.write_text('SQL = "SELECT checksum FROM schema_migrations"\n', encoding="utf-8")
        (self.app / "repository.py").write_text('SQL = "SELECT id FROM items"\n', encoding="utf-8")
        findings = qualityflow.operation_sql_findings(self.app, [runner])
        self.assertEqual(len(findings), 1, findings)
        self.assertIn("repository.py", findings[0])
        with self.assertRaises(qualityflow.QualityError):
            qualityflow.operation_sql_findings(self.app, [self.operation])


if __name__ == "__main__":
    unittest.main()
