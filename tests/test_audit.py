import tempfile
import unittest
from pathlib import Path
from email_validation_claim_audit.audit import audit, doc_claims, source_evidence
from email_validation_claim_audit.phrases import EMAILVALIDATION, NOEMAILVALIDATION, GENERIC

class AuditTests(unittest.TestCase):
    def test_phrases(self):
        self.assertEqual((len(EMAILVALIDATION),len(NOEMAILVALIDATION),len(GENERIC)),(50,24,24))
        for p in EMAILVALIDATION:
            with self.subTest(p=p): self.assertTrue(doc_claims(p)[0])
        for p in NOEMAILVALIDATION:
            with self.subTest(p=p): self.assertEqual(doc_claims(p),([], [p]))
        self.assertEqual(doc_claims('```\nvalidate email\n```'),([],[]))
        self.assertTrue(doc_claims('`validate-email`')[0])
    def test_routes(self):
        routes=['from email_validator import validate_email as v\nv()', 'import email_validator as ev\nev.validate_email()', 'from email_validator.deliverability import validate_email_deliverability as v\nv()', 'import email_validator\nemail_validator.deliverability.validate_email_deliverability()', 'from validate_email import validate_email as v\nv()', 'import validate_email as v\nv.validate_email()', 'from validators import email as e\ne()', 'import validators as v\nv.email()']
        for code in routes:
            with self.subTest(code=code): self.assertTrue(source_evidence(code))
        for name in GENERIC:
            with self.subTest(name=name):
                self.assertTrue(source_evidence('obj.'+name+'()'))
                self.assertTrue(source_evidence('from other import '+name+' as f\nf()'))
                self.assertTrue(source_evidence('obj = make()\nobj.'+name+'()'))
    def test_non_evidence(self):
        cases=['import email_validator, validate_email, validators','validate_email(); validate_email_deliverability(); email()','x.validate_email(); x.email()','import email\nemail.email()','from email_validator import EmailNotValidError\nEmailNotValidError()','from email_validator import EmailNotValidError\ntry: pass\nexcept EmailNotValidError: pass','from email_validator import ValidatedEmail\nValidatedEmail()','from email.utils import parseaddr, formataddr\nparseaddr(x); formataddr(x)','import re\nre.match(pattern,x)','import dns.resolver\ndns.resolver.resolve(x,"MX")','import validators\nvalidators.url(x); validators.domain(x); validators.hostname(x)','import smtplib\nsmtplib.SMTP().sendmail(a,b,c)','send_confirmation(x); send_verification(x)','extract_email(x)','import subprocess\nsubprocess.run("validate email address")','"validate email address"\n# validate email address','validate_email','from email_validator import validate_email\nvalidate_email(','from email_validator import validate_email\ndef validate_email(x): pass\nvalidate_email(x)','import validators\nvalidators = object()\nvalidators.email(x)','from other import validate_email_address\nwith x as validate_email_address: pass\nvalidate_email_address()','def check_email_address(): pass\nobj.check_email_address()']
        for code in cases:
            with self.subTest(code=code): self.assertFalse(source_evidence(code))
    def test_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); readme=root/'README.md'; readme.write_text('TODO: validate email address')
            self.assertEqual(audit(root)['findings'][0]['severity'],'HIGH')
            (root/'tests').mkdir(); (root/'tests/test_x.py').write_text('import validators\nvalidators.email(x)')
            self.assertEqual(audit(root)['findings'][0]['severity'],'MEDIUM')
            (root/'a.py').write_text('import validators'); (root/'b.py').write_text('validators.email(x)')
            self.assertEqual(audit(root)['findings'][0]['severity'],'MEDIUM')
            (root/'a.py').write_text('import validators\nvalidators.email(x)'); self.assertFalse(audit(root)['findings'])
            readme.write_text('does not validate email address'); self.assertEqual(audit(root)['findings'][0]['severity'],'HIGH')
            (root/'a.py').unlink(); self.assertFalse(audit(root)['findings'])
            readme.write_text('No relevant claim.'); self.assertFalse(audit(root)['findings'])
    def test_no_source_and_ignore(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'README.md').write_text('no email validation'); self.assertFalse(audit(root)['findings'])
            (root/'README.md').write_text('validate email'); self.assertEqual(audit(root)['findings'][0]['severity'],'HIGH')
            (root/'main.py').write_text('import validators\nvalidators.email(x)'); self.assertFalse(audit(root)['findings']); self.assertTrue(audit(root,['main.py'])['findings'])
    def test_self_audit(self):
        self.assertFalse(audit(Path(__file__).resolve().parents[1])['findings'])
if __name__ == '__main__': unittest.main()
