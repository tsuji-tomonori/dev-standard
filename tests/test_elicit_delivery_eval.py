from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("elicit_eval", ROOT / "evals/elicit_to_delivery/harness.py")
HARNESS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HARNESS)

# This fixture is a deterministic CLI transport double, not an AI/product-quality evaluation.
FAKE_CLI = r'''#!/usr/bin/env python3
import json, os, subprocess, sys, time
from pathlib import Path
args = sys.argv
last = Path(args[args.index('--output-last-message') + 1])
role = last.stem.split('-')[-1].split('.')[0]
prompt = sys.stdin.read()
count_path = last.parent / ('fake-' + role + '-turn')
count = int(count_path.read_text()) + 1 if count_path.exists() else 1
count_path.write_text(str(count))
mode = os.environ.get('ELICIT_FAKE_MODE', '')
if mode == 'timeout':
    time.sleep(3)
if mode == 'cli-error':
    print('fixture CLI failure', file=sys.stderr)
    sys.exit(7)
print(json.dumps({'type':'thread.started','thread_id':role+'-'+last.parent.name+'-session'}))
def command(argv):
    result = subprocess.run(argv, capture_output=True, text=True)
    if not (mode == 'judge-no-commands' and role == 'judge'):
        print(json.dumps({'type':'item.completed','item':{'type':'command_execution','command':' '.join(argv),
              'exit_code':result.returncode,'aggregated_output':result.stdout+result.stderr}}))
    return result.returncode
if role == 'subject':
    if count == 1:
        schema = json.loads(Path(args[args.index('--output-schema') + 1]).read_text())
        description = schema['properties']['unresolved']['description']
        assert '製品上の未解決事項だけを入れる' in description
        assert 'サマリへの承認待ちそのものは含めない' in description
        assert description in prompt
    if mode == 'external-read' and count == 1:
        command(['ls', str(last.parent)])
    phase = 'clarification' if count == 1 else 'confirmation' if count == 2 else 'delivery'
    if mode == 'early-delivery': phase = 'delivery'
    if mode in {'delivery-progress', 'repeat-confirmation'} and count == 3:
        phase = 'clarification' if mode == 'delivery-progress' else 'confirmation'
    if mode == 'early-write': Path('test_app.py').write_text('# unapproved product test')
    output = {'phase':phase, 'message':'どの月のどの列を集計しますか？' if phase=='clarification' else '要件を確認してください。' if phase=='confirmation' else '完成しました。',
              'requirements':[], 'defaults':[], 'unresolved':[], 'tests':[], 'start_command':'python app.py'}
    if phase == 'confirmation' and mode in {'unresolved-product', 'unresolved-approval'}:
        output['unresolved'] = ['保持期間が未確定' if mode == 'unresolved-product' else
                                'この要件内容で実装・テスト・起動確認へ進めることへの明示承認']
    if phase == 'delivery':
        if mode == 'delivery-delay': time.sleep(.6)
        Path('app.py').write_text('def add(a, b):\n    return a + b\n')
        Path('tests').mkdir(exist_ok=True)
        Path('tests/test_app.py').write_text('import unittest\nfrom app import add\nclass TestApp(unittest.TestCase):\n def test_add(self): self.assertEqual(add(1,2),3)\n')
        argv=['python','-m','unittest','discover','-s','tests']
        code=command(argv)
        output['tests']=[{'requirement_ids':['EX-01'],'argv':argv,'result':str(code)}]
elif role == 'simulator':
    output={'reply':'合っています。実装してください。' if count==2 else '月ごとの経費をまとめます。',
            'approved':count==2,'disclosed_ids':[]}
else:
    if mode == 'judge-delay': time.sleep(.6)
    scenario=json.loads(prompt.split('Hidden scenario:\n',1)[1].split('\nTranscript:\n',1)[0])
    assert '固定directory judge_probes/' in prompt
    assert 'probe_argvにはjudge_probes/配下' in prompt
    Path('judge_probes').mkdir(exist_ok=True)
    Path('judge_probes/independent_probe.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\nfrom app import add\nassert add(-2, 3) == 1\n')
    probe=['python','judge_probes/independent_probe.py']
    if mode == 'outside-probe':
        outside = last.parent / 'outside_probe.py'
        outside.write_text('assert True\n')
        probe = ['python', str(outside)]
    command(probe)
    argv=['python','-m','unittest','discover','-s','tests']
    code=command(argv)
    output={'requirements':[{'id':r['id'],'heard_correctly':True,'implementation':'pass',
             'evidence':'transport double only; independent_probe.py executed','probe_argv':probe} for r in scenario['requirements']],
            'false_assumptions':[], 'question_count':1,'violations':[], 'rubric':[{'dimension':d,'score':2,'evidence':'fixture only'} for d in ['Understanding','Calibration','Core','Clarification','Autonomy','Non-sycophancy','Non-patronizing','Completeness','Faithfulness','Concision','Information density','Vocabulary fit','Japanese naturalness','Task progress']],
            'rerun_results':[{'argv':argv,'exit_code':code,'evidence':'real unittest subprocess'}],
            'limitations':['This is a deterministic fixture, not a quality evaluation.']}
    if mode == 'fabricated-probe':
        output['requirements'][0]['probe_argv']=['python','never_executed.py']
    if mode == 'invalid-probe-path':
        output['requirements'][0]['probe_argv']=['python','\x00']
    if mode == 'no-new-probe':
        output['requirements'][0]['probe_argv']=argv
    if mode == 'judge-no-commands':
        sys.stdout.flush()
        # No completed execution evidence; preserve the session event alone.
        output['requirements'][0]['probe_argv']=['python','never_executed.py']
    if mode == 'omitted-rerun': output['rerun_results']=[]
    if mode == 'hidden-omission': output['requirements'][0]['heard_correctly']=False
    if mode in {'ledger-violation', 'default-prohibition', 'single-candidate-leading', 'over-questioning'}:
        output['violations']=[{'kind':mode,'turn':2,'quote':'要件を確認してください。',
                               'reason':'fixture missing ledger or defaulted mandatory type'}]
last.write_text(json.dumps(output,ensure_ascii=False))
'''


class ElicitDeliveryEvalTest(unittest.TestCase):
    def args(self, fake: Path, **overrides):
        args = HARNESS.parser().parse_args(['--scenario', 'csv-cli', '--variant', 'baseline', '--codex', str(fake)])
        args.max_seconds = 30
        args.call_seconds = 5
        args.delivery_call_seconds = 5
        args.judge_call_seconds = 5
        args.evaluator_root = HARNESS.ROOT.parent / 'external/cache'
        for key, value in overrides.items():
            setattr(args, key, value)
        return args

    def invoke(self, mode='', **overrides):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'repository'
            root.mkdir()
            (root/'.agents').symlink_to(ROOT/'.agents', target_is_directory=True)
            (root/'spec').symlink_to(ROOT/'spec', target_is_directory=True)
            cli = root / 'fake-codex'
            cli.write_text(FAKE_CLI)
            cli.chmod(0o700)
            with patch.object(HARNESS, 'ROOT', root), patch.dict(os.environ, {'ELICIT_FAKE_MODE': mode}):
                run_path, result = HARNESS.run(self.args(cli, **overrides))
                snapshots = {'result':json.loads((run_path/'result.json').read_text()),
                             'transcript':json.loads((run_path/'transcript.json').read_text()),
                             'product':(run_path/'product/app.py').exists(),
                             'probe':(run_path/'judge/product/judge_probes/independent_probe.py').exists(),
                             'judge':json.loads((run_path/'judge.json').read_text()) if (run_path/'judge.json').exists() else None,
                             'prompts':[json.loads(p.read_text())['prompt'] for p in sorted(Path(result['private_workspace']).glob('*.prompt.json'))]}
                return result, snapshots

    def test_complete_fake_cli_e2e_resume_approval_probe_and_rerun(self):
        # Fake root needs the existing rubric, while subjects must remain empty initially.
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'repository'
            root.mkdir()
            (root/'.agents').symlink_to(ROOT/'.agents', target_is_directory=True)
            (root/'spec').symlink_to(ROOT/'spec', target_is_directory=True)
            cli=root/'fake-codex'
            cli.write_text(FAKE_CLI)
            cli.chmod(0o700)
            with patch.object(HARNESS, 'ROOT', root):
                run_path, result=HARNESS.run(self.args(cli))
                self.assertEqual(result['status'], 'completed', result)
                self.assertTrue(result['product_pass'])
                self.assertEqual(result['turns'],3)
                self.assertTrue((run_path/'product/app.py').exists())
                self.assertTrue((run_path/'judge/product/judge_probes/independent_probe.py').exists())
                subject_calls=[c for c in result['calls'] if c['role']=='subject']
                self.assertNotIn('resume',subject_calls[0]['argv'])
                self.assertEqual(subject_calls[1]['argv'][2:4],['resume',subject_calls[0]['session_id']])
                for call in result['calls']:
                    self.assertIn('--ignore-user-config',call['argv'])
                    self.assertIn('features.multi_agent=false',call['argv'])
                    self.assertIn('features.plugins=false',call['argv'])
                    if call['role']=='simulator':
                        self.assertIn('sandbox_mode="read-only"',call['argv'])
                self.assertFalse((run_path/'product/.agents').exists())
                self.assertFalse(Path(result['workspace']).exists())

    def test_context_dependency_assets_and_hidden_inputs_stay_outside_subject(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'repository'
            root.mkdir()
            (root/'.agents').symlink_to(ROOT/'.agents', target_is_directory=True)
            (root/'spec').symlink_to(ROOT/'spec', target_is_directory=True)
            cli = root/'fake-codex'
            cli.write_text(FAKE_CLI)
            cli.chmod(0o700)
            with patch.object(HARNESS, 'ROOT', root):
                run_path, result = HARNESS.run(self.args(cli, variant='context'))
                self.assertEqual(result['status'], 'completed', result)
                self.assertEqual(set(result['context_skills']), {'elicit-to-delivery','calibrated-collaborative-listening'})
                provenance = json.loads((run_path/'provenance.json').read_text())
                self.assertIn('.agents/skills/elicit-to-delivery/SKILL.md',provenance['context_file_sha256'])
                self.assertIn('features.multi_agent=false',provenance['cli_isolation_config'])
                for name in result['context_skills']:
                    self.assertTrue((run_path/'product/.agents/skills'/name/'SKILL.md').exists())
                self.assertFalse((run_path/'product/private').exists())
                self.assertFalse((run_path/'judge/product/AGENTS.md').exists())
                first = json.loads((Path(result['private_workspace'])/'000-subject.prompt.json').read_text())['prompt']
                self.assertNotIn('EX-01', first)
                self.assertNotIn('Hidden scenario', first)
                self.assertIn('毎月の経費CSV', first)
                simulator_prompt = json.loads((Path(result['private_workspace'])/'001-simulator.prompt.json').read_text())['prompt']
                self.assertIn('EX-01', simulator_prompt)
                self.assertIn('経理担当', simulator_prompt)
                self.assertIn('聞かれていない話題を示唆・列挙しない', simulator_prompt)
                self.assertIn('未開示の隠れ要件が残っていても承認する', simulator_prompt)
                self.assertIn('実装完了の判定ではない', simulator_prompt)
                subject = Path(result['workspace'])
                private = Path(result['private_workspace'])
                judge = Path(result['judge_workspace'])
                simulator = Path(next(c['cwd'] for c in result['calls'] if c['role']=='simulator'))
                for evaluator in [private, judge, simulator]:
                    self.assertTrue(evaluator.is_relative_to(private))
                    self.assertFalse(evaluator.is_relative_to(root))
                    self.assertFalse(any((ancestor/'AGENTS.md').exists() for ancestor in [evaluator, *evaluator.parents]))
                    self.assertNotEqual(evaluator.parent, Path('/tmp'))
                    self.assertNotEqual(evaluator.parent, subject.parent)
                    self.assertFalse(subject.is_relative_to(evaluator))
                    self.assertFalse(evaluator.is_relative_to(subject))

    def test_smoke_uses_reduced_contract_and_marks_results(self):
        result, saved = self.invoke(smoke=True)
        self.assertEqual(result['status'], 'completed', result)
        self.assertTrue(saved['result']['smoke'])
        self.assertEqual(set(result['requirement_ids']), {'EX-01','EX-02','EX-07','EX-10','EX-12'})
        self.assertTrue(result['product_pass'])

    def test_unresolved_description_is_shared_by_context_and_baseline(self):
        prompts = []
        for variant in ['context', 'baseline']:
            with self.subTest(variant=variant):
                result, saved = self.invoke(variant=variant)
                self.assertEqual(result['status'], 'completed', result)
                prompts.append(saved['prompts'][0])
        self.assertEqual(prompts[0], prompts[1])

    def test_approval_with_any_unresolved_item_still_fails(self):
        for mode in ['unresolved-product', 'unresolved-approval']:
            with self.subTest(mode=mode):
                result, saved = self.invoke(mode)
                self.assertEqual(result['status'], 'failed')
                self.assertIn('approval despite unresolved questions', result['error'])
                self.assertTrue(saved['transcript'][1]['simulator_approved'])
                self.assertFalse(saved['product'])

    def test_failure_before_approval_saved(self):
        result, saved=self.invoke('early-delivery')
        self.assertEqual(result['status'],'failed')
        self.assertIn('before simulator approval',result['error'])
        self.assertEqual(saved['result']['status'],'failed')

    def test_unapproved_product_write_is_critical_even_in_clarification(self):
        result, saved = self.invoke('early-write')
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['critical_failures'][0]['kind'], 'implementation-before-approval')
        self.assertIn('test_app.py', saved['transcript'][0]['workspace_delta']['created'])
        self.assertEqual([c['role'] for c in result['calls']], ['subject'])

    def test_approved_subject_continues_without_simulator_until_delivery(self):
        result, saved = self.invoke('delivery-progress')
        self.assertEqual(result['status'], 'completed', result)
        self.assertEqual([c['role'] for c in result['calls']],
                         ['subject', 'simulator', 'subject', 'simulator', 'subject', 'subject', 'judge'])
        self.assertTrue(saved['transcript'][3]['approval_before_turn'])
        self.assertTrue(result['product_pass'])

    def test_repeated_confirmation_keeps_approval_and_records_violation(self):
        result, saved = self.invoke('repeat-confirmation')
        self.assertEqual(result['status'], 'completed', result)
        self.assertEqual(result['protocol_violations'][0]['kind'], 'repeated-confirmation-after-approval')
        self.assertTrue(saved['transcript'][3]['approval_before_turn'])
        self.assertFalse(result['product_pass'])
        self.assertEqual(sum(c['role']=='simulator' for c in result['calls']), 2)

    def test_approval_does_not_fill_hidden_coverage(self):
        result, saved = self.invoke('hidden-omission')
        self.assertEqual(result['status'], 'completed', result)
        self.assertLess(result['coverage'], 1)
        self.assertFalse(result['product_pass'])
        self.assertTrue(saved['transcript'][1]['simulator_approved'])
        self.assertIn('未開示のまま承認された隠れ要件はcoverageの欠落', saved['prompts'][-1])

    def test_ledger_and_default_violations_prevent_product_pass(self):
        for mode in ['ledger-violation', 'default-prohibition', 'single-candidate-leading', 'over-questioning']:
            with self.subTest(mode=mode):
                result, saved = self.invoke(mode)
                self.assertEqual(result['status'], 'completed', result)
                self.assertEqual(result['coverage'], 1)
                self.assertFalse(result['product_pass'])
                self.assertEqual(saved['judge']['violations'][0]['kind'], mode)
                self.assertIn('確認サマリに10観点各1行', saved['prompts'][-1])
                self.assertIn('既定値禁止類型', saved['prompts'][-1])
                self.assertIn('単一候補の誘導', saved['prompts'][-1])
                self.assertIn('低リスク細部を個別確認する過補正', saved['prompts'][-1])

    def test_external_private_access_is_in_subject_audit(self):
        result, _ = self.invoke('external-read')
        self.assertEqual(result['status'], 'completed', result)
        self.assertEqual(result['audit']['status'], 'violation')
        self.assertTrue(result['audit']['known_path_matches'])
        self.assertFalse(result['product_pass'])

    def test_timeout_cli_error_and_turn_limit_saved(self):
        for mode, overrides, reason in [('timeout',{'call_seconds':.1},'exceeded'),
                                         ('cli-error',{},'CLI exit 7'),
                                         ('',{'max_turns':1},'turn limit')]:
            with self.subTest(mode=mode):
                result, _=self.invoke(mode,**overrides)
                self.assertEqual(result['status'],'failed')
                self.assertIn(reason,result['error'])

    def test_probe_evidence_errors_degrade_only_affected_requirement(self):
        for mode, reason in [('fabricated-probe', 'executed probe'), ('no-new-probe', 'new independent probe file'),
                             ('invalid-probe-path', 'new independent probe file')]:
            with self.subTest(mode=mode):
                result, saved = self.invoke(mode)
                self.assertEqual(result['status'], 'completed', result)
                self.assertIsNone(result['error'])
                self.assertFalse(result['product_pass'])
                self.assertEqual(result['implementation_unverified'], 1)
                self.assertEqual(result['implementation_pass'], len(result['requirement_ids']) - 1)
                self.assertEqual(saved['judge']['requirements'][0]['implementation'], 'unverified')
                self.assertIn(reason, saved['judge']['requirements'][0]['evidence'])
                self.assertEqual(result['evidence_errors'][0]['id'], 'EX-01')

    def test_probe_directory_instruction_and_outside_probe_stays_unverified(self):
        result, saved = self.invoke('outside-probe')
        self.assertEqual(result['status'], 'completed', result)
        self.assertEqual(result['implementation_unverified'], len(result['requirement_ids']))
        self.assertFalse(result['product_pass'])
        self.assertIn('judge pass lacks a new independent probe file', saved['judge']['requirements'][0]['evidence'])
        self.assertNotIn('judge pass lacks successful executed probe', saved['judge']['requirements'][0]['evidence'])
        self.assertIn('product外（/tmp等）にはprobeを書かない', saved['prompts'][-1])

    def test_judge_has_own_limit_and_is_still_bounded_by_total_deadline(self):
        result, _ = self.invoke('judge-delay', call_seconds=.3, judge_call_seconds=2)
        self.assertEqual(result['status'], 'completed', result)
        self.assertEqual(result['calls'][-1]['timeout_seconds'], 2)
        self.assertEqual(result['limits']['judge_call_seconds'], 2)
        result, _ = self.invoke('judge-delay', judge_call_seconds=.1)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['calls'][-1]['role'], 'judge')
        self.assertEqual(result['calls'][-1]['status'], 'timeout')
        result, _ = self.invoke('judge-delay', max_seconds=.8, judge_call_seconds=2)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['calls'][-1]['role'], 'judge')
        self.assertLess(result['calls'][-1]['timeout_seconds'], .8)

    def test_missing_rerun_and_execution_logs_are_evidence_errors(self):
        for mode in ['omitted-rerun', 'judge-no-commands']:
            with self.subTest(mode=mode):
                result, _ = self.invoke(mode)
                self.assertEqual(result['status'], 'completed', result)
                self.assertFalse(result['product_pass'])
                self.assertFalse(result['tests_verified'])
                self.assertTrue(result['evidence_errors'])
                if mode == 'judge-no-commands':
                    self.assertEqual(result['implementation_unverified'], len(result['requirement_ids']))

    def test_approved_calls_use_delivery_limit_and_timeout_still_fails(self):
        result, _ = self.invoke('delivery-delay', call_seconds=.3, delivery_call_seconds=2)
        self.assertEqual(result['status'], 'completed', result)
        self.assertEqual([c['timeout_seconds'] for c in result['calls'] if c['role']=='subject'], [.3, .3, 2])
        result, _ = self.invoke('delivery-delay', call_seconds=.3, delivery_call_seconds=.1)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['calls'][-1]['role'], 'subject')
        self.assertEqual(result['calls'][-1]['status'], 'timeout')

    def test_delivery_limit_cannot_exceed_total_deadline(self):
        result, _ = self.invoke('delivery-delay', max_seconds=.5, call_seconds=.3, delivery_call_seconds=2)
        self.assertEqual(result['status'], 'failed')
        self.assertIn('exceeded', result['error'])
        self.assertLess(result['calls'][-1]['timeout_seconds'], .5)

    def test_default_limits_and_overrides(self):
        args = HARNESS.parser().parse_args([])
        self.assertEqual((args.call_seconds, args.delivery_call_seconds, args.judge_call_seconds, args.max_seconds), (300, 1800, 1800, 3600))
        self.assertEqual(args.evaluator_root, Path.home()/'.cache/elicit-eval')
        args = HARNESS.parser().parse_args(['--call-seconds', '12', '--delivery-call-seconds', '34', '--judge-call-seconds', '45', '--max-seconds', '56', '--rejudge', '/saved/run'])
        self.assertEqual((args.call_seconds, args.delivery_call_seconds, args.judge_call_seconds, args.max_seconds), (12, 34, 45, 56))
        self.assertEqual(args.rejudge, Path('/saved/run'))

    def test_rejudge_uses_saved_private_scenario_only_and_preserves_original_evidence(self):
        for mode in ['judge-delay', 'outside-probe', 'external-read']:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as folder:
                root = Path(folder) / 'repository'
                root.mkdir()
                (root / '.agents').symlink_to(ROOT / '.agents', target_is_directory=True)
                cli = root / 'fake-codex'
                cli.write_text(FAKE_CLI)
                cli.chmod(0o700)
                with patch.object(HARNESS, 'ROOT', root), patch.dict(os.environ, {'ELICIT_FAKE_MODE': mode}):
                    run_path, previous = HARNESS.run(self.args(cli, smoke=True, judge_call_seconds=.1 if mode == 'judge-delay' else 5))
                    old_result = (run_path / 'result.json').read_bytes()
                    old_judge = (run_path / 'judge.json').read_bytes() if (run_path / 'judge.json').exists() else None
                    immutable = {p: p.read_bytes() for p in [run_path / 'transcript.json', run_path / 'provenance.json', run_path / 'product/app.py']}
                    private = Path(previous['private_workspace'])
                    original_private_files = {p: p.read_bytes() for p in private.glob('*') if p.is_file()}
                    args = self.args(cli, rejudge=run_path, scenario='booking-api', variant='context', smoke=False)
                    # CLI scenario selection and current public fixtures cannot replace the saved private input.
                    with patch.dict(os.environ, {'ELICIT_FAKE_MODE': ''}), patch.object(HARNESS, 'HERE', Path(folder) / 'missing-fixtures'):
                        same_path, result = HARNESS.rejudge(args)
                    self.assertEqual(same_path, run_path)
                    self.assertEqual(result['status'], 'completed', result)
                    self.assertIsNone(result['error'])
                    self.assertEqual(result['scenario'], 'csv-cli')
                    self.assertEqual(result['variant'], 'baseline')
                    self.assertTrue(result['smoke'])
                    self.assertEqual(result['requirement_ids'], previous['requirement_ids'])
                    self.assertEqual(result['implementation_pass'], len(previous['requirement_ids']))
                    self.assertEqual(result['audit'], previous['audit'])
                    self.assertEqual(result['critical_failures'], previous['critical_failures'])
                    self.assertEqual(result['protocol_violations'], previous['protocol_violations'])
                    self.assertEqual(result['product_pass'], mode != 'external-read')
                    self.assertEqual(result['calls'][:len(previous['calls'])], previous['calls'])
                    added = result['calls'][len(previous['calls']):]
                    self.assertEqual([c['role'] for c in added], ['judge'])
                    self.assertNotIn('resume', added[0]['argv'])
                    record = result['rejudges'][-1]
                    self.assertEqual(record['calls'], added)
                    self.assertEqual((run_path / record['previous_result']).read_bytes(), old_result)
                    if old_judge:
                        self.assertEqual((run_path / record['previous_judge']).read_bytes(), old_judge)
                    else:
                        self.assertIsNone(record['previous_judge'])
                    for p, data in {**immutable, **original_private_files}.items():
                        self.assertEqual(p.read_bytes(), data, p)
                    evidence = Path(record['evidence_dir'])
                    self.assertTrue((evidence / 'judge/product/judge_probes/independent_probe.py').is_file())
                    self.assertTrue(list(evidence.glob('*-judge.events.jsonl')))
                    self.assertFalse(list(evidence.glob('*.prompt.json')))
                    self.assertFalse((evidence / 'scenario.json').exists())
                    self.assertEqual(json.loads((evidence / 'provenance.json').read_text())['source_private_workspace'], str(private))
                    prompt = json.loads(next(Path(record['private_workspace']).glob('*-judge.prompt.json')).read_text())['prompt']
                    self.assertIn('EX-01', prompt)
                    self.assertNotIn('BK-01', prompt)
                    self.assertTrue((run_path / 'judge/product').is_dir())
                    # A second retry also starts with the subject product, never prior judge probes.
                    with patch.dict(os.environ, {'ELICIT_FAKE_MODE': ''}):
                        _, twice = HARNESS.rejudge(args)
                    self.assertEqual(twice['implementation_unverified'], 0)
                    self.assertEqual(len(twice['rejudges']), 2)
                    self.assertNotEqual(twice['rejudges'][0]['private_workspace'], twice['rejudges'][1]['private_workspace'])

    def test_rejudge_failure_keeps_old_results_without_stale_current_judgment(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'repository'
            root.mkdir()
            (root / '.agents').symlink_to(ROOT / '.agents', target_is_directory=True)
            cli = root / 'fake-codex'
            cli.write_text(FAKE_CLI)
            cli.chmod(0o700)
            with patch.object(HARNESS, 'ROOT', root), patch.dict(os.environ, {'ELICIT_FAKE_MODE': ''}):
                run_path, _ = HARNESS.run(self.args(cli))
                old_judge = (run_path / 'judge.json').read_bytes()
                with patch.dict(os.environ, {'ELICIT_FAKE_MODE': 'judge-delay'}):
                    _, result = HARNESS.rejudge(self.args(cli, rejudge=run_path, judge_call_seconds=.1))
                self.assertEqual(result['status'], 'failed')
                self.assertFalse(result['product_pass'])
                self.assertIn('judge exceeded', result['error'])
                self.assertNotIn('coverage', result)
                self.assertFalse((run_path / 'judge.json').exists())
                record = result['rejudges'][-1]
                self.assertEqual((run_path / record['previous_judge']).read_bytes(), old_judge)
                self.assertEqual(record['calls'][0]['status'], 'timeout')
                _, recovered = HARNESS.rejudge(self.args(cli, rejudge=run_path))
                self.assertEqual(recovered['status'], 'completed', recovered)
                self.assertTrue(recovered['product_pass'])

    def test_rejudge_rejects_undelivered_or_missing_private_input_before_changes(self):
        for mode in ['early-write', '']:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as folder:
                root = Path(folder) / 'repository'
                root.mkdir()
                (root / '.agents').symlink_to(ROOT / '.agents', target_is_directory=True)
                cli = root / 'fake-codex'
                cli.write_text(FAKE_CLI)
                cli.chmod(0o700)
                with patch.object(HARNESS, 'ROOT', root), patch.dict(os.environ, {'ELICIT_FAKE_MODE': mode}):
                    run_path, previous = HARNESS.run(self.args(cli))
                    if not mode:
                        (Path(previous['private_workspace']) / 'scenario.json').unlink()
                    before = (run_path / 'result.json').read_bytes()
                    with patch.object(HARNESS.Runner, 'call', side_effect=AssertionError('must not launch')):
                        with self.assertRaises((HARNESS.EvalFailure, FileNotFoundError)):
                            HARNESS.rejudge(self.args(cli, rejudge=run_path))
                    self.assertEqual((run_path / 'result.json').read_bytes(), before)
                    self.assertFalse(list(run_path.glob('result.pre-rejudge-*')))

    def test_main_dispatches_rejudge_without_running_dialogue(self):
        result = {'status': 'completed', 'error': None}
        with patch('sys.argv', ['harness', '--rejudge', '/saved/run']), patch.object(HARNESS, 'run') as run, patch.object(HARNESS, 'rejudge', return_value=(Path('/saved/run'), result)) as retry:
            self.assertEqual(HARNESS.main(), 0)
            run.assert_not_called()
            self.assertEqual(retry.call_args.args[0].rejudge, Path('/saved/run'))

    def test_external_cwd_and_ancestor_instructions_checked_before_launch(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)/'repository'
            root.mkdir()
            (root/'AGENTS.md').write_text('Repository-only instructions')
            cli = root/'fake-codex'
            cli.write_text(FAKE_CLI)
            cli.chmod(0o700)
            blocked = Path(folder)/'blocked'
            blocked.mkdir()
            (blocked/'AGENTS.md').write_text('Must never reach evaluator')
            with patch.object(HARNESS, 'ROOT', root):
                for cache, reason in [(root/'cache', 'inside repository'), (blocked/'cache', 'inherits instructions'), (Path('/tmp'), 'directly under /tmp')]:
                    with self.subTest(cache=cache):
                        run_path, result = HARNESS.run(self.args(cli, evaluator_root=cache))
                        self.assertEqual(result['status'], 'failed')
                        self.assertIn(reason, result['error'])
                        self.assertEqual(result['calls'], [])
                        self.assertTrue((run_path/'result.json').exists())
                # Preflight is repeated at call time, even after workspace setup.
                external = Path(folder)/'clean/cache'
                external.mkdir(parents=True)
                (external.parent/'AGENTS.override.md').write_text('Unexpected instructions')
                runner = HARNESS.Runner(str(cli), external, HARNESS.time.monotonic()+5, 1)
                with self.assertRaisesRegex(HARNESS.EvalFailure, 'inherits instructions'):
                    runner.call('simulator', external, 'fixture', 'read-only', '', HARNESS.SIM_SCHEMA)
                self.assertEqual(runner.calls, [])

    def test_parallel_runs_have_distinct_directories_and_sessions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)/'repository'
            root.mkdir()
            (root/'AGENTS.md').write_text('Repository instructions must not reach evaluators')
            (root/'.agents').symlink_to(ROOT/'.agents', target_is_directory=True)
            cli = root/'fake-codex'
            cli.write_text(FAKE_CLI)
            cli.chmod(0o700)
            with patch.object(HARNESS, 'ROOT', root), patch.dict(os.environ, {'ELICIT_FAKE_MODE': ''}):
                with ThreadPoolExecutor(max_workers=2) as pool:
                    outcomes = list(pool.map(HARNESS.run, [self.args(cli), self.args(cli)]))
                paths = [path for path, _ in outcomes]
                self.assertEqual(len(set(paths)), 2)
                private_paths = [result['private_workspace'] for _, result in outcomes]
                self.assertEqual(len(set(private_paths)), 2)
                sessions = []
                for path, result in outcomes:
                    self.assertEqual(result['status'], 'completed', result)
                    self.assertTrue(result['product_pass'])
                    self.assertEqual(result['turns'], 3)
                    sessions.append(result['subject_session'])
                    self.assertFalse((path/'private').exists())
                    self.assertFalse(list(path.glob('*.prompt.json')))
                    for call in result['calls']:
                        if call['role'] in {'judge', 'simulator'}:
                            self.assertFalse(Path(call['cwd']).is_relative_to(root))
                self.assertEqual(len(set(sessions)), 2)

    def test_command_audit_flags_hidden_path_and_broad_search(self):
        def event(cmd):
            return {'type':'item.completed','item':{'type':'command_execution','command':cmd}}
        hidden=Path('/private-hidden/scenario.json')
        self.assertEqual(HARNESS.audit([event('cat /private-hidden/scenario.json')],[hidden])['status'],'violation')
        self.assertEqual(HARNESS.audit([event('find / -name "*.json"')],[hidden])['status'],'inconclusive')
        self.assertEqual(HARNESS.audit([event('python -m unittest discover')],[hidden])['status'],'no-known-path-access-detected')

    def test_probe_claim_requires_completed_command_and_actual_exit(self):
        events=[{'type':'item.completed','item':{'type':'command_execution','command':'cd /tmp/product && python probe.py','exit_code':0}}]
        self.assertTrue(HARNESS.executed_command(['python','probe.py'],events,0))
        self.assertFalse(HARNESS.executed_command(['python','never.py'],events,0))
        self.assertFalse(HARNESS.executed_command(['python','probe.py'],events,1))
        events[0]['type']='item.started'
        self.assertFalse(HARNESS.executed_command(['python','probe.py'],events,0))

    def test_probe_command_requires_exact_argv_and_supports_cli_shell_wrapper(self):
        argv = ['python', 'independent_probe.py']
        def event(command):
            return [{'type':'item.completed', 'item':{'type':'command_execution', 'command':command, 'exit_code':0}}]
        accepted = [
            'python independent_probe.py',
            "/bin/bash -lc 'python independent_probe.py'",
            "/bin/sh -c 'python independent_probe.py'",
            "/bin/bash -lc 'cd /tmp/product && python independent_probe.py'",
            'cd "/tmp/product with spaces" && python independent_probe.py',
        ]
        rejected = [
            'echo python independent_probe.py',
            'printf python independent_probe.py',
            'printf "%s" "python independent_probe.py"',
            "echo 'python independent_probe.py'",
            "/bin/bash -lc 'echo python independent_probe.py'",
            'python independent_probe.py; true',
            'python independent_probe.py && echo done',
            'python independent_probe.py || true',
            'python independent_probe.py | cat',
            'python independent_probe.py > probe.txt',
            'python independent_probe.py &',
            'python independent_probe.py\ntrue',
            'python independent_probe.py # trailing comment',
            'FOO=bar python independent_probe.py',
            'cd /tmp && echo python independent_probe.py',
            'cd /tmp; python independent_probe.py',
            'cd /tmp && python independent_probe.py; true',
            "/bin/bash -lc 'cd /tmp && python independent_probe.py; true'",
            "python 'independent_probe.py' extra",
        ]
        for command in accepted:
            with self.subTest(command=command):
                self.assertTrue(HARNESS.executed_command(argv, event(command), 0))
        for command in rejected:
            with self.subTest(command=command):
                self.assertFalse(HARNESS.executed_command(argv, event(command), 0))

    def test_reference_closure_includes_assets_and_nested_dependencies(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)
            for name, content in [('first','Use $second and [doc](../third/references/doc.md)'),('second','Use $third'),('third','No dependencies')]:
                (source/name).mkdir()
                (source/name/'SKILL.md').write_text(content)
            self.assertEqual(HARNESS.skill_closure(source,'first',{'first':['second'],'second':['third'],'third':[]}),{'first','second','third'})

    def test_optional_cross_references_are_not_hard_dependencies(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder)
            for name, content in [('first','Optional $other'), ('other','Extra')]:
                (source/name).mkdir()
                (source/name/'SKILL.md').write_text(content)
            self.assertEqual(HARNESS.skill_closure(source,'first',{'first':[],'other':[]}), {'first'})

    def test_workspace_delta_preserves_created_changed_deleted_hashes(self):
        self.assertEqual(HARNESS.product_delta({'old':'a','changed':'b'}, {'new':'c','changed':'d'}),
                         {'created':{'new':'c'},'changed':{'changed':{'before':'b','after':'d'}},'deleted':{'old':'a'}})

    def test_scenarios_have_distinct_domains_and_required_categories(self):
        scenarios=[json.loads(path.read_text()) for path in (HARNESS.HERE/'scenarios').glob('*.json')]
        self.assertGreaterEqual(len(scenarios),3)
        self.assertEqual(len({s['domain'] for s in scenarios}),len(scenarios))
        for scenario in scenarios:
            ids=[r['id'] for r in scenario['requirements']]
            self.assertEqual(len(ids),len(set(ids)))
            self.assertTrue(scenario['opening'])
            self.assertTrue(scenario['persona']['style'])
            self.assertGreaterEqual(len(scenario['traps']),3)
            topics=' '.join(r['disclosure_topic'] for r in scenario['requirements'])
            for topic in ['権限','保持','例外','対象外']:
                self.assertIn(topic,topics,scenario['id'])

    def test_envelope_rejects_wrong_phase_or_missing_fields(self):
        with self.assertRaises(ValueError):
            HARNESS.validate_schema({'phase':'delivery'},HARNESS.SUBJECT_SCHEMA)
        with self.assertRaises(ValueError):
            HARNESS.validate_schema({'reply':'yes','approved':'yes','disclosed_ids':[]},HARNESS.SIM_SCHEMA)


if __name__ == '__main__':
    unittest.main()
