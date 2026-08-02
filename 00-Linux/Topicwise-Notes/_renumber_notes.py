from pathlib import Path
import re

base = Path(r'c:\Users\saura\OneDrive\Desktop\DevOps-Learnings\00-Linux\Topicwise-Notes')

for path in base.glob('*.md'):
    if path.name == 'README.md':
        continue

    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    out = []
    counters = {2: 0, 3: 0}

    for line in lines:
        m = re.match(r'^(#{2,3}) (\d+)(?:\.(\d+))?(.*)$', line)
        if m:
            level = len(m.group(1))
            if level == 2:
                counters[2] += 1
                counters[3] = 0
                new_num = counters[2]
                out.append(f"{'#' * level} {new_num}.{m.group(4)}")
            elif level == 3:
                counters[3] += 1
                new_num = f"{counters[2]}.{counters[3]}"
                out.append(f"{'#' * level} {new_num}{m.group(4)}")
            else:
                out.append(line)
        else:
            out.append(line)

    path.write_text('\n'.join(out).rstrip() + '\n', encoding='utf-8')
