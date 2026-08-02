from pathlib import Path
import re

roots = [Path('00-Linux/Topicwise-Notes'), Path('01-Git/TopicWise-Notes')]
emoji_pattern = re.compile(r'[\U0001F300-\U0001FAFF\u2600-\u27BF]')

for root in roots:
    for path in root.rglob('*.md'):
        text = path.read_text(encoding='utf-8')
        lines = text.splitlines()
        out = []
        in_fence = False

        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith('```'):
                in_fence = not in_fence
                out.append(line)
                continue
            if in_fence:
                out.append(line)
                continue

            m = re.match(r'^(#{1,6})\s+(.+)$', line)
            if not m:
                out.append(line)
                continue

            hashes, content = m.groups()
            content = content.strip()

            # Match headings like: ### 1. 🔹 1 What is Linux?
            m_sub = re.match(r'^([0-9]+)\.\s*([^\w\s]+)\s+([0-9]+)\s*(.*)$', content)
            if m_sub:
                chapter, icon, subnum, title = m_sub.groups()
                title = title.strip()
                new_content = f'{icon} {chapter}.{subnum}' + (f' {title}' if title else '')
                out.append(f'{hashes} {new_content}')
                continue

            # Match headings like: ## 4. 📌 ⌨️ Essential Linux Commands
            m_num = re.match(r'^([0-9]+)\.\s*(.*)$', content)
            if m_num:
                num, rest = m_num.groups()
                rest = rest.strip()
                if emoji_pattern.search(rest):
                    first_icon = next(ch for ch in rest if emoji_pattern.fullmatch(ch))
                    rest = re.sub(r'^[\U0001F300-\U0001FAFF\u2600-\u27BF\s]+', '', rest).strip()
                    rest = re.sub(r'^[\U0001F300-\U0001FAFF\u2600-\u27BF\s]+', '', rest).strip()
                    new_content = f'{first_icon} {num}. {rest}' if rest else f'{first_icon} {num}.'
                else:
                    new_content = f'📌 {num}. {rest}' if rest else f'📌 {num}.'
                out.append(f'{hashes} {new_content}')
                continue

            if emoji_pattern.search(content):
                out.append(line)
            else:
                out.append(f'{hashes} 📌 {content}')

        new_text = '\n'.join(out) + ('\n' if text.endswith('\n') else '')
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
