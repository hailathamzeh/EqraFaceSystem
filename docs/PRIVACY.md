# Privacy and biometric-data guidance

Eqra Face System processes face images and derived encodings. Both should be treated as sensitive biometric data.

## Before collecting data

- Define a specific, legitimate purpose for the experiment.
- Obtain informed consent from every participant.
- Explain what is collected, how it is processed, who can access it, and when it will be deleted.
- Obtain any institutional, ethics, or legal approval required for your setting.

## Storage and access

- Keep real images outside this repository or under the ignored `data/private/` directory.
- Keep the SQLite database, camera credentials, face encodings, logs, and recognition outputs out of Git.
- Use encrypted storage with restricted access for any retained data.
- Use separate development credentials for cameras and devices.
- Never commit a `.env` file or a populated database.

## Publication checklist

Before each push, run:

```bash
git status --short
git diff --cached
```

Confirm that no face images, encodings, databases, credentials, device addresses, personal names, or local paths are staged. If a secret has ever been committed, removing the current file is not enough. Rotate the credential and remove it from Git history before publishing.

## Retention

Document a retention period and securely delete images, encodings, logs, and database records when the stated purpose ends or consent is withdrawn.
