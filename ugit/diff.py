"""Tree comparison, diff, and merge helpers for ugit object contents."""

import subprocess

from collections import defaultdict
from tempfile import NamedTemporaryFile as Temp

from . import data

def compare_trees(*trees):
    """Yield each path with the object id from every input tree."""
    entries = defaultdict(lambda: [None] * len(trees))
    for i, tree in enumerate(trees):
        for path, oid in tree.items():
            entries[path][i] = oid
    for path, oids in entries.items():
        yield (path, *oids)

def iter_changed_files(t_from, t_to):
    """Yield paths whose object ids differ between two tree dictionaries."""
    for path, o_from, o_to in compare_trees(t_from, t_to):
        if o_from != o_to:
            action = ('new file' if not o_from else
                      'deleted' if not o_to else
                      'modified')
            yield path, action

def diff_trees(t_from, t_to):
    """Return a unified diff for every changed blob between two trees."""
    output = 'b'
    for path, o_from, o_to in compare_trees(t_from, t_to):
        if o_from != o_to:
            output += diff_blobs(o_from, o_to, path)
    return output

def diff_blobs(o_from, o_to, path='blob'):
    """Run the system diff command against two blob objects."""
    with Temp() as f_from, Temp() as f_to:
        for oid, f in ((o_from, f_from), (o_to, f_to)):
            if oid:
                f.write(data.get_object(oid))
                f.flush()
        with subprocess.Popen(
                ['diff', '--unified', '--show-c-function', '--label', f'a/{path}', f_from.name, '--label', f'b/{path}', f_to.name],
                stdout=subprocess.PIPE) as proc:
                output, _ = proc.communicate ()
        return output

def merge_trees(t_base, t_HEAD, t_other):
    """Merge matching paths from base, HEAD, and another tree."""
    tree = {}
    for path, o_base, o_HEAD, o_other in compare_trees(t_base, t_HEAD, t_other):
        tree[path] = data.hash_object(merge_blobs(o_base, o_HEAD, o_other))
    return tree


def merge_blobs(o_base, o_HEAD, o_other):
    """Run diff3 to produce merged content for three blob versions."""
    with Temp() as f_base, Temp() as f_HEAD, Temp() as f_other:
        for oid, f in ((o_base, f_base), (o_HEAD, f_HEAD), (o_other, f_other)):
            if oid:
                f.write(data.get_object(oid))
                f.flush()
        with subprocess.Popen(
            ['diff3', '-m', '-L', 'HEAD', f_HEAD.name, '-L', 'BASE', f_base.name, '-L', 'MERGE_HEAD', f_other.name,],
            stdout=subprocess.PIPE) as proc:
            output, _ = proc.communicate()
            assert proc.returncode in (0,1)
        return output
