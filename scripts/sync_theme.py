import re
from pathlib import Path

def sync():
    # Repo root = scripts/..
    base_dir = Path(__file__).resolve().parent.parent
    templates_dir = base_dir / "templates" / "html"
    theme_file = templates_dir / "_archviz-theme.html"

    if not theme_file.exists():
        print(f"Theme file {theme_file} does not exist!")
        return

    theme_content = theme_file.read_text(encoding="utf-8")
    match = re.search(r'(<style id="archviz-theme-vars">.*?</script>)', theme_content, re.DOTALL)
    if not match:
        print("Could not find theme block in _archviz-theme.html")
        return

    theme_block = match.group(1)

    for f in templates_dir.glob("*.html"):
        if f.name == "_archviz-theme.html":
            continue
        content = f.read_text(encoding="utf-8")
        if 'style id="archviz-theme-vars"' in content:
            print(f"Syncing theme block to {f.name}...")
            new_content = re.sub(r'<style id="archviz-theme-vars">.*?</script>', theme_block, content, flags=re.DOTALL)
            f.write_text(new_content, encoding="utf-8")

if __name__ == "__main__":
    sync()
