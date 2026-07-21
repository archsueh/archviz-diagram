import re
from pathlib import Path

def fix_all():
    # Repo root = scripts/..
    base_dir = Path(__file__).resolve().parent.parent
    templates_dir = base_dir / "templates" / "html"
    
    # Read the canonical theme block
    theme_file = templates_dir / "_archviz-theme.html"
    if not theme_file.exists():
        print("Theme file not found!")
        return
        
    theme_content = theme_file.read_text(encoding="utf-8")
    theme_match = re.search(r'(<style id="archviz-theme-vars">.*?</script>)', theme_content, re.DOTALL)
    if not theme_match:
        print("Canonical theme block not found!")
        return
    canonical_theme_block = theme_match.group(1)

    for f in templates_dir.glob("*.html"):
        if f.name in ("_archviz-theme.html", "_archviz-export.html", "_archviz-motion.html", "_flow-attach.html"):
            continue
            
        content = f.read_text(encoding="utf-8")
        
        # 1. Clean up duplicate theme script block
        # Look for any block matching the old theme system script:
        # <!-- archviz-skills Theme System Script -->\n<script>...</script>
        # Or duplicate script blocks containing window.archvizTheme =
        dup_pattern = r'<!-- archviz-skills Theme System Script -->\s*<script>.*?</script>'
        content = re.sub(dup_pattern, "", content, flags=re.DOTALL)
        
        # If there is still a duplicate window.archvizTheme script block, remove it.
        # We split the file by script tags and check.
        # Actually, let's just make sure the theme block is clean.
        # 2. Insert </head>\n<body> if missing.
        # Find where the theme system style/script block ends.
        # It ends with the script tag for archvizTheme.
        # Let's search for the pattern <style id="archviz-theme-vars">.*?</script>
        match = re.search(r'(<style id="archviz-theme-vars">.*?</script>)', content, re.DOTALL)
        if match:
            theme_end_pos = match.end()
            # Check what follows
            following_content = content[theme_end_pos:].strip()
            if not following_content.startswith("</head>"):
                print(f"Adding </head><body> to {f.name}...")
                # Insert </head>\n<body> right after the theme system block
                content = content[:theme_end_pos] + "\n</head>\n<body>" + content[theme_end_pos:]
                
        # 3. Clean up duplicate </body></html> at the end if any
        # Some files might have multiple body/html closures if we did replacements.
        # Let's make sure there is only one </body></html> at the very end.
        
        f.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    fix_all()
