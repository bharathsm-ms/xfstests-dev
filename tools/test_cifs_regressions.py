import errno
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


WORKSPACE = Path(__file__).resolve().parents[1]
FAIL_FUNCTION = '_fail() { printf "%s\\n" "$1"; exit 1; };\n'


class CifsTestRegressions(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='cifs regressions ')
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)

    def source(self, test_id):
        return (WORKSPACE / 'tests/cifs' / test_id).read_text()

    def shell(self, code, *arguments):
        return subprocess.run(
            ['bash', '-c', FAIL_FUNCTION + code, 'regression',
             str(self.directory), *arguments], cwd=WORKSPACE,
            capture_output=True, text=True, timeout=10)

    def test_shell_syntax(self):
        for test_id in ('103', '116', '157', '171', '216', '251', '310'):
            with self.subTest(test=test_id):
                result = subprocess.run(
                    ['bash', '-n', str(WORKSPACE / 'tests/cifs' / test_id)],
                    capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_socket_visibility_rejects_incompatible_profile(self):
        body = 'if printf ' + self.source('103').split('if printf ', 1)[1]
        body = body.split('\n_host_from_unc()', 1)[0]
        harness = '''TEST_FS_MOUNT_OPTS=$2; MOUNT_OPTIONS=$3
_notrun() { printf '%s\\n' "$1"; exit 77; }
'''
        for options in ('nosharesock', '-o nosharesock',
                        '-o vers=3.1.1,nosharesock,seal',
                        '-o credentials=/private/creds,nosharesock'):
            for position in ('test', 'mount'):
                with self.subTest(options=options, position=position):
                    arguments = (options, '') if position == 'test' else ('', options)
                    result = self.shell(harness + body, *arguments)
                    self.assertEqual(result.returncode, 77, result)
                    self.assertIn('required sharesock baseline', result.stdout)
        for options in ('', '-o credentials=/private/creds,seal',
                        '-o credentials=/private/nosharesock,seal',
                        '-o username=nosharesock', '-o nosharesock_extra'):
            with self.subTest(options=options):
                self.assertEqual(self.shell(harness + body, options, options).returncode, 0)

    def test_punch_hole_diagnostic_preserves_error(self):
        line = next(line for line in self.source('116').splitlines()
                    if '_fail "fallocate punch-hole failed:' in line)
        (self.directory / 'err').write_text('fallocate: Input/output error\n')
        result = self.shell('W=$1;\n' + line)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout,
                         'fallocate punch-hole failed: fallocate: Input/output error\n')
        self.assertEqual(result.stderr, '')

    def test_punch_hole_only_skips_unsupported_operations(self):
        body = self.source('116').split('# Punch hole (zero data) in the middle, keep size\n', 1)[1]
        body = body.split('\n# Size must remain unchanged', 1)[0]
        harness = '''W=$1; message=$2; operation_status=$3; off=262144; len=262144
_notrun() { printf '%s\\n' "$1"; exit 77; }
fallocate() {
    [[ "$LC_ALL" == C ]] || return 99
    printf '%s\\n' "$message" >&2
    return "$operation_status"
}
'''
        for message, expected in (
                ('fallocate: fallocate failed: keep size mode is unsupported', 77),
                ('fallocate: Operation not supported', 77),
                ('fallocate: EOPNOTSUPP', 77),
                ('fallocate: ENOTSUP', 77),
                ('fallocate: Invalid argument (EINVAL)', 1),
                ('fallocate: Input/output error', 1),
                ('fallocate: Permission denied', 1),
                ('fallocate: unrecognized option', 1)):
            with self.subTest(message=message):
                result = self.shell(harness + body, message, '1')
                self.assertEqual(result.returncode, expected, result)
                if expected == 1:
                    self.assertIn(message, result.stdout)
        self.assertEqual(self.shell(harness + body, '', '0').returncode, 0)

    def test_flush_counter_is_share_scoped(self):
        stats = self.directory / 'stats'
        stats.write_text(
            '1) \\\\other\\share\nFlushes: 999 sent 0 failed\n'
            '2) \\\\target\\share\nFlushes: 4 sent 0 failed\n'
            '3) \\\\target\\share\nFlushes: 5 sent 0 failed\n')
        code = '. ./common/cifs_debug; _cifs_stat "$2" "Flushes:" "$1/stats"'
        result = self.shell(code, '//target/share')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '9\n')
        result = self.shell(code, '//missing/share')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')

    def test_strictsync_requires_flush_increment(self):
        body = 'stat_before=' + self.source('157').split('stat_before=', 1)[1]
        harness = '''TEST_DEV=//target/share
CIFS_TEST_WORK=$1
seqres=$1/result
after=$2
_notrun() { printf 'SKIP: %s\\n' "$*"; exit 77; }
_cifs_stat() {
    [[ "$1" == //target/share && "$2" == Flushes: ]] || exit 9
    if [[ -e "$CIFS_TEST_WORK/strictsync_test" ]]; then
        [[ "$after" != missing-after ]] || return 1
        printf '%s\\n' "$after"
    else
        [[ "$after" != missing-before ]] || return 1
        printf '4\\n'
    fi
}
'''
        for after, expected in (('5', 0), ('4', 1), ('3', 1),
                                ('missing-before', 77), ('missing-after', 1)):
            with self.subTest(after=after):
                (self.directory / 'strictsync_test').unlink(missing_ok=True)
                result = self.shell(harness + body, after)
                self.assertEqual(result.returncode, expected, result)
                self.assertEqual('strictsync flush OK' in result.stdout, expected == 0)
        (self.directory / 'strictsync_test').unlink(missing_ok=True)
        result = self.shell(harness + 'python3() { return 1; }\n' + body, '5')
        self.assertEqual(result.returncode, 1)
        self.assertIn('strictsync write/fsync failed', result.stdout)

    def test_strictsync_does_not_swallow_fsync_error(self):
        code = self.source('157').split("<<'PY'\n", 1)[1].split('\nPY\n', 1)[0]
        with (patch.object(sys, 'argv', ['check', str(self.directory / 'data')]),
              patch('os.fsync', side_effect=OSError(errno.EIO, 'injected fsync error'))):
            with self.assertRaises(OSError) as raised:
                exec(compile(code, 'cifs157-workload', 'exec'), {})
        self.assertEqual(raised.exception.errno, errno.EIO)

    def test_lease_stress_preserves_recovery_errors(self):
        body = self.source('171').split(
            '# Attempt remediation for race losses (file deleted/renamed by other worker)\n', 1)[1]
        body = body.split('            if [ $rc -ne 0 ]; then', 1)[0]
        harness = 'fname=$1/file; op=$2; rc=1;\n'
        for operation in ('0', '1', '2', '3'):
            with self.subTest(operation=operation):
                result = self.shell(harness + body + '\nexit "$rc"', operation)
                self.assertEqual(result.returncode, 0, result)
                result = self.shell(harness + 'echo() { return 7; };\n' +
                                    body + '\nexit "$rc"', operation)
                self.assertEqual(result.returncode, 7, result)
        result = self.shell(harness + 'mv() { return 9; };\n' +
                            body + '\nexit "$rc"', '2')
        self.assertEqual(result.returncode, 9, result)

    def test_lease_stress_rename_paths_are_worker_local(self):
        body = 'case $op in\n' + self.source('171').split('        case $op in\n', 1)[1]
        body = body.split('        end_ns=', 1)[0]
        worker = '(\n' + body + '\nprintf "%s\\n" "$alt"\n) &\n'
        result = self.shell('fname=$1/file; op=2; mv() { return 0; };\n' +
                            worker + worker + 'wait\n')
        self.assertEqual(result.returncode, 0, result)
        paths = result.stdout.splitlines()
        self.assertEqual(len(paths), 2, result)
        self.assertEqual(len(set(paths)), 2, result)

    def test_lease_stress_checks_worker_exit_status(self):
        body = self.source('171').split('# Wait cleanup\n', 1)[1]
        body = body.split('# Basic activity sanity:', 1)[0]
        harness = 'WROOT=$1; seqres=$1/result; OPMAX=4000; (exit "$2") & pids=$!;\n'
        self.assertEqual(self.shell(harness + body, '0').returncode, 0)
        result = self.shell(harness + body, '23')
        self.assertEqual(result.returncode, 1, result)
        self.assertIn('rc failure', result.stdout)

    def test_lease_stress_zero_counts_are_single_numbers(self):
        body = 'ops_count=' + self.source('171').split('ops_count=', 1)[1]
        body = body.split('\necho "Lease stress closetimeo=30 OK"', 1)[0]
        harness = 'seqres=$1/result; SLOW_TOL=3; RC_TOL=2; OPMAX=4000;\n'
        log = self.directory / 'result.full'
        log.write_text('DONE tag=P1 slow_final=0 rc_fail_final=0\n')
        result = self.shell(harness + body + '\nprintf "%s:%s:%s" "$ops_count" "$slow_total" "$rc_fail_total"')
        self.assertEqual(result.returncode, 0, result)
        self.assertEqual(result.stdout, '1:0:0')
        log.write_text('')
        result = self.shell(harness + body)
        self.assertEqual(result.returncode, 1, result)
        self.assertIn('no worker completion markers', result.stdout)

    def test_readdir_survivors_are_exact_bytes(self):
        body = self.source('216').split('surviving=0\n', 1)[1]
        body = body.split('\necho "cifs216: delete-during-readdir', 1)[0]
        code = 'DIR2=$1; seqres=$1/result; surviving=0;\n' + body
        for index in range(2, 101, 2):
            (self.directory / f'del_{index}').write_bytes(f'content_{index}\n'.encode())
        self.assertEqual(self.shell(code).returncode, 0)
        target = self.directory / 'del_2'
        for value in (b'content_2\x00\n', b'content_2\n\n', b'content_2',
                      b'content_2\r\n', b'\x00' * 10, b'wrong\n', b''):
            with self.subTest(value=value):
                target.write_bytes(value)
                result = self.shell(code)
                self.assertEqual(result.returncode, 1, result)
                self.assertIn('del_2 has wrong content', result.stdout)
                self.assertNotIn('ignored null byte', result.stderr)
        target.unlink()
        result = self.shell(code)
        self.assertEqual(result.returncode, 1)
        self.assertIn('expected 50 surviving files, got 49', result.stdout)

    def test_readdir_fixture_creation_errors_fail(self):
        body = self.source('216').split('for i in $(seq 1 100); do\n', 1)[1]
        body = body.split('\ndone', 1)[0]
        result = self.shell('DIR2=$1/absent; i=2;\n' + body)
        self.assertEqual(result.returncode, 1)
        self.assertIn('create del_2 failed', result.stdout)

    def test_idsfromsid_creation_and_stat_errors_fail(self):
        body = '    F4=' + self.source('251').split('    F4=', 1)[1]
        body = body.split('\n    _do "umount', 1)[0]
        harness = 'M1=$1; SUB=work; seqres=$1/result;\n'
        result = self.shell(harness + body)
        self.assertEqual(result.returncode, 1)
        self.assertIn('create idsfromsid_file failed', result.stdout)
        (self.directory / 'work').mkdir()
        self.assertEqual(self.shell(harness + body).returncode, 0)
        for field, message in (('%u', 'owner'), ('%g', 'group')):
            with self.subTest(field=field):
                mock = ('stat() { if [[ "$2" == "' + field + '" ]]; then return 1; '
                        'else command stat "$@"; fi; };\n')
                result = self.shell(harness + mock + body)
                self.assertEqual(result.returncode, 1)
                self.assertIn(f'stat idsfromsid {message} failed', result.stdout)

    def test_multimount_samples_are_exact_bytes(self):
        code = self.source('310').split("<<'PY'\n", 1)[1].split('\nPY\n', 1)[0]
        prefix = 'cifs310.regression'
        for index in (1, 2):
            (self.directory / f'{prefix}.mount{index}_file1').write_bytes(
                f'mount{index}_file1_data\n'.encode())

        def run():
            return subprocess.run(
                [sys.executable, '-B', '-c', code, str(self.directory), prefix, '2'],
                capture_output=True, text=True, timeout=10)

        result = run()
        self.assertEqual(result.returncode, 0, result)
        self.assertEqual(result.stdout, '')
        expected = b'mount1_file1_data\n'
        target = self.directory / f'{prefix}.mount1_file1'
        for value in (b'', b'\x00' * len(expected),
                      expected.replace(b'file', b'\x00file'),
                      expected.replace(b'\n', b'\r\n'), expected[:-1],
                      expected + b'\n', b'wrong\n'):
            with self.subTest(value=value):
                target.write_bytes(value)
                result = run()
                self.assertEqual(result.returncode, 1, result)
                self.assertIn('content mismatch mount 1', result.stdout)
        target.unlink()
        result = run()
        self.assertEqual(result.returncode, 1)
        self.assertIn('sample read failed for mount 1', result.stdout)


if __name__ == '__main__':
    unittest.main()
