from pathlib import Path
import re

root = Path(r'c:\Users\saura\OneDrive\Desktop\DevOps-Learnings\00-Linux\Topicwise-Notes')
emoji_pattern = re.compile(r'^[\U0001F300-\U0001FAFF\u2600-\u27BF]+')

for path in sorted(root.glob('*.md')):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    out = []
    in_fence = False

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('```') or stripped.startswith('~~~'):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        m = re.match(r'^(?P<hashes>#{2,6})\s*(?P<num>\d+)\.\s*(?P<rest>.+)$', line)
        if not m:
            out.append(line)
            continue

        hashes = m.group('hashes')
        num = m.group('num')
        rest = m.group('rest')
        icon_match = emoji_pattern.match(rest)
        if icon_match:
            icon = icon_match.group(0)
            body = rest[len(icon):].lstrip()
            if body.startswith(num + '.'):
                body = body[len(num) + 1:].lstrip()
            elif body.startswith(num):
                body = body[len(num):].lstrip()
            if body:
                if re.match(r'^\d+$', body):
                    new_content = f'{icon} {num}.{body}'
                else:
                    new_content = f'{icon} {num}. {body}'
            else:
                new_content = f'{icon} {num}'
            out.append(f'{hashes} {new_content}')
            continue

        out.append(line)

    new_text = '\n'.join(out) + ('\n' if text.endswith('\n') else '')
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print(path)
