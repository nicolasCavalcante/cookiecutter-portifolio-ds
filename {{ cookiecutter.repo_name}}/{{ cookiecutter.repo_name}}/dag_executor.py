"""DAG pipeline tool for python"""

import json
from pathlib import Path
from typing import Callable, List, Set

CACHE_PATH = Path(__file__).parent / '.dag_cache'
CACHE_PATH.parent.mkdir(exist_ok=True, parents=True)


class Cache():
    def __init__(self) -> None:
        if not CACHE_PATH.is_file():
            with CACHE_PATH.open('w') as f:
                f.write('{ }')
        with CACHE_PATH.open() as f:
            data = json.load(f)
        self.data = {}
        for pathstr in data:
            self.data[Path(pathstr).resolve()] = data[pathstr]

    def changed(self, path: Path):
        path = path.resolve()
        if path in self.data:
            return path.stat().st_mtime > self.data[path]
        self.data[path.resolve()] = 1
        return True

    def update(self):
        for path in self.data:
            path: Path
            self.data[path.resolve()] = path.stat().st_mtime
        data = {}
        for path in self.data:
            data[path.as_posix()] = self.data[path]
        with CACHE_PATH.open('w') as f:
            json.dump(data, f, indent=4)


class PipeNode():
    def __init__(
        self,
        dependencies: List[Path] = list(),
        actions: List[Callable] = list(),
        targets: List[Path] = list()
    ) -> None:
        self.dependencies: List[Path] = dependencies
        self.actions: List[Callable] = actions
        self.targets: List[Path] = targets

    def run(self, cache: Cache) -> bool:
        can_run = all([path.exists() for path in self.dependencies])
        if not can_run:
            return False
        changed = not self.dependencies
        changed |= any([cache.changed(path) for path in self.dependencies])
        changed |= any([not path.exists() for path in self.targets])
        sucessfull = True
        if not changed:
            return sucessfull
        sucessfull = all([
            action(self.dependencies, self.targets) for action in self.actions
        ])
        return sucessfull


class Pipeline():
    def __init__(self, nodes: Set[PipeNode] = set()) -> None:
        self.nodes: Set[PipeNode] = nodes
        return None

    def run(self) -> List[PipeNode]:
        cache = Cache()
        to_run = list(self.nodes)
        while True:
            got_new_runs = False
            for i in reversed(range(len(to_run))):
                node: PipeNode = to_run[i]
                successful = node.run(cache)
                if successful:
                    del to_run[i]
                    got_new_runs = True
            if not got_new_runs:
                break
        cache.update()
        return to_run


if __name__ == '__main__':

    def slowaction(dependencies: List[Path], targets: List[Path]) -> bool:
        for tgt in targets:
            tgt.mkdir(parents=True, exist_ok=True)
        print('running')
        return True

    def action(dependencies: List[Path], targets: List[Path]) -> bool:
        for tgt in targets:
            tgt.mkdir(parents=True, exist_ok=True)
        return True

    nodes = set()
    nodes.add(PipeNode([], [action], [Path('test/a.txt')]))
    nodes.add(PipeNode([Path('test/a.txt')], [action], [Path('test/b.txt')]))
    nodes.add(PipeNode([Path('test/a.txt')], [action], [Path('test/c.txt')]))
    nodes.add(
        PipeNode([Path('test/b.txt'), Path('test/c.txt')], [action],
                 [Path('test/d.txt')]))
    nodes.add(
        PipeNode([Path('test/a.txt'), Path('test/d.txt')], [action],
                 [Path('test/c.txt'), Path('test/f.txt')]))
    nodes.add(PipeNode([Path('test/f.txt')], [action], [Path('test/g.txt')]))
    nodes.add(
        PipeNode([Path('test/g.txt')], [slowaction], [Path('test/h.txt')]))
    pipe = Pipeline(nodes)
    for node in pipe.run():
        node: PipeNode
        for path in node.dependencies:
            print(str(path))
