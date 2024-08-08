def load_meta_tags(file_path, env_vars):
    meta_tags = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.strip():
                continue
            parts = line.strip().split(';')
            if len(parts) == 3:
                tag_type, name, content = parts
                # Replace {{ var }} with corresponding environment variable value
                for key, value in env_vars.items():
                    content = content.replace(f"{{{{ {key.lower()} }}}}", value)
                meta_tags.append(f'<meta {tag_type}="{name}" content="{content}">')
    return '\n'.join(meta_tags)
