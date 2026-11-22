# Documentation claim audit

This offline tool compares documented claims about judging whether an address is well-formed, valid, or deliverable with static Python call patterns. It reports discrepancies for human review.

## Usage

```sh
email-validation-claim-audit audit .
python3 -m email_validation_claim_audit audit . --json
```

Use `--verbose` for details, `--ignore PREFIX` repeatedly to omit paths, and `--fail-on medium` to include test-only evidence in the failure threshold. Exit status is 0 for pass, 2 for findings at the threshold, and 1 for usage or I/O errors.

## Differentiation

This family covers judging whether an address is well-formed, valid, or deliverable only. It does not cover sending mail, sending a text to a number, proving who holds an address with a one-time code or confirmation link, reading an address out of a document, decoding a code from an image, formatting an address for display, splitting an address into a display name and a mailbox, matching an address-shaped pattern with a regex, looking up a domain's mail records, finding addresses inside running text, or checking whether a phone number is well-formed or valid for a region.

The phrase lists also exclude claims about spreadsheet reading and generation, word-document reading and generation, presentation reading and generation, PDF extraction, generation, merging, splitting, encryption, rotation, form-filling, watermarking, redaction, compression and annotation, table extraction, OCR, document extraction, e-signature, payment processing, screen recording, video generation, QR code generation, barcode generation and scanning, audio mixing, generation and editing, source separation, speech recognition, text-to-speech, noise suppression, music generation and transcription, and other claim-audit families.

## Limitations

```text
validate email address
```

A browser form may perform this check independently of the tool. The phrase is flagged for human judgment.

```text
check email address
```

This may refer only to whether a record contains an address. The phrase is flagged for human judgment.

```text
email address validation
```

A roadmap can mention this capability before implementation. The phrase is flagged for human judgment.

```text
email address validator
```

This may refer to a person or hosted page. The phrase is flagged for human judgment.

```text
valid email address
```

A person may have typed the address correctly without any check. The phrase is flagged for human judgment.

```text
email address is valid
```

Providers may use different rules. The phrase is flagged for human judgment.

```text
reject invalid email address
```

Rejection may instead mean a duplicate or blocked domain. The phrase is flagged for human judgment.

```text
check if email address is valid
```

This may describe a manual runbook step. The phrase is flagged for human judgment.

```text
validate email
```

This may mean only checking that a value was supplied. The phrase is flagged for human judgment.

```text
email deliverability check
```

This may refer to a third-party bulk-list hygiene report. The phrase is flagged for human judgment.

Only call shapes are checked; a call constructed but never executed still counts. Alias chains the tracer cannot follow are missed. A bare library import is not evidence. A roadmap, changelog, or TODO remains a claim. Denials outside the listed phrases may be missed. Only the root README and Markdown files under a docs component are read. Each route must occur within one module. A locally defined route name shadows the route, including thin wrappers. Dead code counts. A subprocess invocation is not evidence.

A sending call alone is not evidence. A phone check alone is not evidence. An authentication call alone is not evidence. An extraction call alone is not evidence. A locally defined generic name is shadowed. A generic name behind an untraceable alias chain is missed. Only exact phrases match, not meaning. Only Python source is read. Runtime-only routes are invisible; code is never executed and no network is used.

A parseaddr call alone only splits an address. A regex match alone only checks a pattern. A DNS mail-record query alone says nothing about the local part. An exception handler alone does not prove a check occurred. Constructing a result object alone does not perform a check. A confirmation send alone proves neither syntax nor deliverability.
