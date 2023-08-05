from pathlib import Path
from typing import List, Dict, Any

import yaml


def generate_class(name: str, dictionary: dict) -> str:
    return '\n'.join((
        f'class {name}:',
        ' ' * 4 + f'def __init__(self):',
        '\n'.join((
            ' ' * 8 + f'self.{key}: {type(value).__name__} = {repr(value)}' for key, value in dictionary.items()
        ))
    ))


def lazy_write(file_path: Path, content: str):
    if file_path.exists():
        with open(str(file_path)) as f:
            exists_content = f.read()
        if exists_content == content:
            return

    with open(str(file_path), 'w') as f:
        f.write(content)


def generate(file_path: Path, suffix: str = '') -> bool:
    with open(str(file_path)) as f:
        content: Dict[str, Dict[str, Any]] = yaml.load(f)

    root: Path = file_path.parent / 'build'
    root.mkdir(exist_ok=True)

    init_list: List[str] = []
    for key, value in content.items():
        class_name = key.replace('_', ' ').title().replace(' ', '') + suffix.capitalize()
        class_content = generate_class(name=class_name, dictionary=value)

        file_name = key if not suffix else f'{key}_{suffix}'
        generate_path = root / f'{file_name}.py'
        lazy_write(file_path=generate_path, content=class_content + '\n')

        init_list.append(f'from .{generate_path.stem} import {class_name}')

    init_content = '\n'.join(init_list) + '\n'
    lazy_write(file_path=root / '__init__.py', content=init_content)

    return True
