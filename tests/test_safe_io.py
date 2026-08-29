from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import safe_io


class SafeIOTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repository"
        self.root.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_missing_snapshot_can_be_published_once_and_then_is_idempotent(self) -> None:
        output = self.root / "generated" / "value.json"
        before = safe_io.snapshot_file(output, root=self.root)
        self.assertEqual(before, safe_io.MISSING)

        safe_io.atomic_write_cas(output, b'{"value":1}\n', before, root=self.root)
        after = safe_io.snapshot_file(output, root=self.root)
        safe_io.atomic_write_cas(output, b'{"value":1}\n', after, root=self.root)

        self.assertEqual(output.read_bytes(), b'{"value":1}\n')

    def test_stale_snapshot_is_rejected_without_overwriting_new_content(self) -> None:
        output = self.root / "value.txt"
        output.write_bytes(b"initial")
        before = safe_io.snapshot_file(output, root=self.root)
        output.write_bytes(b"target-owned-update")

        with self.assertRaises(safe_io.ConcurrentModificationError):
            safe_io.atomic_write_cas(output, b"generated", before, root=self.root)

        self.assertEqual(output.read_bytes(), b"target-owned-update")

    def test_bound_root_identity_rejects_later_lexical_name_replacement(self) -> None:
        original = self.root / "value.txt"
        original.write_bytes(b"original")
        info = self.root.stat()
        safe_io.bind_root_identity(self.root, (info.st_dev, info.st_ino))
        self.assertEqual(safe_io.read_bytes_nofollow(original, root=self.root), b"original")

        displaced = self.root.with_name("repository-displaced")
        self.root.rename(displaced)
        self.root.mkdir()
        replacement = self.root / "value.txt"
        replacement.write_bytes(b"replacement")

        with self.assertRaises(safe_io.ConcurrentModificationError):
            safe_io.read_bytes_nofollow(replacement, root=self.root)

        self.assertEqual((displaced / "value.txt").read_bytes(), b"original")
        self.assertEqual(replacement.read_bytes(), b"replacement")

    def test_symlinked_parent_is_refused_and_external_file_is_untouched(self) -> None:
        external = Path(self.temp.name) / "external"
        external.mkdir()
        outside = external / "value.txt"
        outside.write_bytes(b"outside")
        (self.root / "generated").symlink_to(external, target_is_directory=True)

        with self.assertRaises(safe_io.UnsafePathError):
            safe_io.atomic_write_cas(
                self.root / "generated" / "value.txt",
                b"replacement",
                safe_io.MISSING,
                root=self.root,
            )

        self.assertEqual(outside.read_bytes(), b"outside")

    def test_batch_validates_every_snapshot_before_first_publication(self) -> None:
        first = self.root / "first.txt"
        second = self.root / "second.txt"
        first.write_bytes(b"first-old")
        second.write_bytes(b"second-old")
        expected = {
            first: safe_io.snapshot_file(first, root=self.root),
            second: safe_io.snapshot_file(second, root=self.root),
        }
        second.write_bytes(b"target-owned")

        with self.assertRaises(safe_io.ConcurrentModificationError):
            safe_io.atomic_batch_write_cas(
                {first: b"first-new", second: b"second-new"},
                expected,
                root=self.root,
            )

        self.assertEqual(first.read_bytes(), b"first-old")
        self.assertEqual(second.read_bytes(), b"target-owned")

    def test_read_precondition_change_after_publication_rolls_back_outputs(self) -> None:
        source = self.root / "source.txt"
        output = self.root / "generated.txt"
        source.write_bytes(b"observed")
        read_preconditions = {
            source: safe_io.snapshot_file(source, root=self.root)
        }
        real_publish = safe_io._publish_missing

        def publish_then_change(
            parent_fd: int, temporary: str, destination: str
        ) -> None:
            real_publish(parent_fd, temporary, destination)
            source.write_bytes(b"changed")

        with mock.patch.object(
            safe_io, "_publish_missing", side_effect=publish_then_change
        ):
            with self.assertRaises(safe_io.ConcurrentModificationError):
                safe_io.atomic_batch_write_cas(
                    {output: b"derived"},
                    {output: safe_io.MISSING},
                    root=self.root,
                    read_preconditions=read_preconditions,
                )

        self.assertFalse(output.exists())
        self.assertEqual(source.read_bytes(), b"changed")

    @unittest.skipUnless(__import__("sys").platform.startswith("linux"), "renameat2 test")
    def test_noncooperating_boundary_update_is_restored_not_lost(self) -> None:
        output = self.root / "value.txt"
        output.write_bytes(b"initial")
        before = safe_io.snapshot_file(output, root=self.root)
        real_exchange = safe_io._exchange_existing
        injected = False

        def mutate_then_exchange(parent_fd: int, temporary: str, destination: str) -> None:
            nonlocal injected
            if not injected:
                injected = True
                descriptor = __import__("os").open(destination, __import__("os").O_WRONLY, dir_fd=parent_fd)
                try:
                    __import__("os").ftruncate(descriptor, 0)
                    __import__("os").write(descriptor, b"concurrent")
                    __import__("os").fsync(descriptor)
                finally:
                    __import__("os").close(descriptor)
            real_exchange(parent_fd, temporary, destination)

        with mock.patch.object(safe_io, "_exchange_existing", side_effect=mutate_then_exchange):
            with self.assertRaises(safe_io.ConcurrentModificationError):
                safe_io.atomic_write_cas(output, b"generated", before, root=self.root)

        self.assertEqual(output.read_bytes(), b"concurrent")

    def test_symlinked_lock_file_is_refused(self) -> None:
        outside = Path(self.temp.name) / "outside.lock"
        outside.write_bytes(b"outside")
        (self.root / ".unsafe.lock").symlink_to(outside)

        with self.assertRaises(safe_io.UnsafePathError):
            with safe_io.locked_repository(self.root, ".unsafe.lock"):
                self.fail("unsafe lock was acquired")
        self.assertEqual(outside.read_bytes(), b"outside")

    def test_pinned_module_loader_refuses_a_symlinked_source(self) -> None:
        real = Path(self.temp.name) / "outside.py"
        real.write_text("VALUE = 'outside'\n", encoding="utf-8")
        module_path = self.root / "tools" / "module.py"
        module_path.parent.mkdir()
        module_path.symlink_to(real)

        with self.assertRaises(safe_io.UnsafePathError):
            safe_io.load_module_nofollow(
                module_path,
                root=self.root,
                module_name="test_unsafe_pinned_module",
            )

    @unittest.skipUnless(__import__("sys").platform.startswith("linux"), "renameat2 test")
    def test_directory_publish_is_atomic_no_replace(self) -> None:
        parent = self.root / ".runtime"
        candidate = parent / ".candidate"
        destination = parent / "0.32.0"
        candidate.mkdir(parents=True)
        (candidate / "runtime.txt").write_bytes(b"candidate")
        destination.mkdir()
        (destination / "runtime.txt").write_bytes(b"installed")

        with self.assertRaises(safe_io.ConcurrentModificationError):
            safe_io.atomic_publish_directory_noreplace(candidate, destination, root=self.root)

        self.assertEqual((destination / "runtime.txt").read_bytes(), b"installed")
        self.assertEqual((candidate / "runtime.txt").read_bytes(), b"candidate")

    @unittest.skipUnless(__import__("sys").platform.startswith("linux"), "renameat2 test")
    def test_directory_cas_cleanup_preserves_a_post_identity_swap(self) -> None:
        output = self.root / "generated"
        output.mkdir()
        (output / "manifest.json").write_bytes(b"managed")
        expected = safe_io.directory_identity_nofollow(output, root=self.root)
        real_identity = safe_io.directory_identity_fd_nofollow
        displaced: Path | None = None
        competing: Path | None = None

        def swap_after_identity(
            descriptor: int,
            *,
            display: Path,
        ) -> tuple[int, int, str]:
            nonlocal displaced, competing
            identity = real_identity(descriptor, display=display)
            displaced = display.with_name(f"{display.name}.captured")
            display.rename(displaced)
            display.mkdir()
            competing = display / "human.txt"
            competing.write_bytes(b"preserve")
            return identity

        with mock.patch.object(
            safe_io,
            "directory_identity_fd_nofollow",
            side_effect=swap_after_identity,
        ):
            with self.assertRaises(safe_io.ConcurrentModificationError):
                safe_io.remove_tree_nofollow_cas(
                    output,
                    expected_identity=expected,
                    root=self.root,
                )

        self.assertIsNotNone(competing)
        self.assertTrue(competing.is_file())
        self.assertEqual(competing.read_bytes(), b"preserve")
        self.assertIsNotNone(displaced)
        self.assertTrue(displaced.is_dir())

    def test_snapshot_rejects_an_in_place_writer_during_read(self) -> None:
        path = self.root / "value.bin"
        path.write_bytes(b"a" * 1024)
        descriptor = os.open(path, os.O_RDONLY)
        real_read = os.read
        mutated = False

        def read_then_mutate(fd: int, size: int) -> bytes:
            nonlocal mutated
            chunk = real_read(fd, size)
            if chunk and not mutated:
                mutated = True
                path.write_bytes(b"b" * 1024)
            return chunk

        try:
            with mock.patch.object(os, "read", side_effect=read_then_mutate):
                with self.assertRaises(safe_io.ConcurrentModificationError):
                    safe_io._read_open_file(descriptor)
        finally:
            os.close(descriptor)

    def test_base_exception_removes_staged_temporary_file(self) -> None:
        output = self.root / "value.txt"
        with mock.patch.object(os, "write", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                safe_io.atomic_write_cas(output, b"new", safe_io.MISSING, root=self.root)
        self.assertFalse(output.exists())
        self.assertEqual(
            [path.name for path in self.root.iterdir() if ".safeio-" in path.name],
            [],
        )

    @unittest.skipUnless(__import__("sys").platform.startswith("linux"), "descriptor root test")
    def test_batch_pins_root_identity_across_path_replacement(self) -> None:
        output = self.root / "nested/value.txt"
        moved = self.root.with_name("repository-pinned")
        real_write_staged = safe_io._write_staged
        replaced = False

        def replace_root_then_stage(parent_fd: int, name: str, content: bytes, mode: int) -> str:
            nonlocal replaced
            if not replaced:
                replaced = True
                self.root.rename(moved)
                self.root.mkdir()
            return real_write_staged(parent_fd, name, content, mode)

        with mock.patch.object(safe_io, "_write_staged", side_effect=replace_root_then_stage):
            safe_io.atomic_write_cas(output, b"pinned", safe_io.MISSING, root=self.root)

        self.assertEqual((moved / "nested/value.txt").read_bytes(), b"pinned")
        self.assertFalse((self.root / "nested/value.txt").exists())
        self.root = moved

    def test_darwin_exchange_uses_atomic_renameatx_boundary(self) -> None:
        with (
            mock.patch.object(safe_io, "_renameat2", return_value=False),
            mock.patch.object(safe_io, "_renameatx_np", return_value=True) as darwin,
        ):
            safe_io._exchange_existing(10, "stage", "target")
        darwin.assert_called_once_with(
            10, "stage", 10, "target", safe_io._RENAME_SWAP_DARWIN
        )


if __name__ == "__main__":
    unittest.main()
