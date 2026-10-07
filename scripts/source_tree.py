"""Content-addressed sources shared by routing and Runtime distribution."""
from pathlib import Path
import hashlib, json, subprocess, re
DOMAIN_ENTRIES = ('AGENTS.md', '.agents/skills', 'docs', 'registry', 'schemas', 'domains')
KERNEL_ENTRIES = ('AGENTS.md', 'config', 'docs', 'rules', 'schemas', 'workflows', 'skills', 'scripts')

def tree_digest(root, entries=DOMAIN_ENTRIES):
    root = Path(root)
    files = []
    digest = hashlib.sha256()
    for entry in entries:
        p = root / entry
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files.extend((x for x in p.rglob('*') if x.is_file()))
    for p in sorted(files, key=lambda x: x.relative_to(root).as_posix()):
        if any((x in p.parts for x in ('.git', '__pycache__', '.DS_Store'))) or p.suffix == '.pyc':
            continue
        if p.is_symlink():
            raise ValueError('Unsupported source symlink: ' + str(p))
        digest.update(p.relative_to(root).as_posix().encode() + b'\x00')
        digest.update(hashlib.sha256(p.read_bytes()).hexdigest().encode() + b'\n')
    return 'sha256:' + digest.hexdigest()

class Source:

    def __init__(self, root, revision):
        if not isinstance(revision, str) or not re.fullmatch('([0-9a-f]{40}|sha256:[0-9a-f]{64})', revision):
            raise ValueError('Source revision must be an immutable Git SHA or content digest')
        self.root = Path(root).resolve()
        self.revision = revision
        self.snapshot = revision.startswith('sha256:')
        self.content_revision = revision
        if not self.snapshot and (not (self.root / '.git').exists()):
            provenance = json.loads((self.root / 'source-provenance.json').read_text())
            if provenance.get('revision') != revision:
                raise ValueError('Installed source provenance revision mismatch')
            self.content_revision = provenance['content_digest']
            self.snapshot = True
        self.verify()

    def text(self, relative):
        p = Path(relative)
        if p.is_absolute() or '..' in p.parts:
            raise ValueError('Source path escapes Domain root')
        if self.snapshot:
            target = (self.root / p).resolve()
            target.relative_to(self.root)
            return target.read_text(encoding='utf-8')
        result = subprocess.run(['git', '-C', str(self.root), 'show', f'{self.revision}:{relative}'], capture_output=True, text=True)
        if result.returncode:
            raise ValueError('Pinned source missing: ' + relative)
        return result.stdout

    def json(self, relative):
        return json.loads(self.text(relative))

    def verify(self):
        if self.snapshot and tree_digest(self.root) != self.content_revision:
            raise ValueError('Domain source digest mismatch')
