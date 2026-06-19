import re
from pathlib import Path

def sync():
    base_dir = Path("/Users/mac/Developer/archviz")
    templates_dir = base_dir / "templates" / "html"
    export_file = templates_dir / "_archviz-export.html"

    if not export_file.exists():
        print(f"Export file {export_file} does not exist!")
        return

    export_content = export_file.read_text(encoding="utf-8")
    
    # We want to keep everything from _archviz-export.html (styles + script)
    # but remove any comments that are not necessary.
    # Actually, we can just sync the style block and the script block.
    # Let's extract the style block and script block from _archviz-export.html
    style_match = re.search(r'(<style id="archviz-export-styles">.*?</style>)', export_content, re.DOTALL)
    script_match = re.search(r'(<script>.*?</script>)', export_content, re.DOTALL)
    
    if not style_match or not script_match:
        print("Could not find style or script blocks in _archviz-export.html")
        return
        
    new_style = style_match.group(1)
    new_script = script_match.group(1)
    
    # The complete block we want to insert
    new_export_block = f"{new_style}\n\n{new_script}\n"

    for f in templates_dir.glob("*.html"):
        if f.name in ("_archviz-export.html", "_archviz-theme.html", "_archviz-motion.html", "_flow-attach.html"):
            continue
            
        content = f.read_text(encoding="utf-8")
        
        # We need to find where to replace or insert.
        # Let's check if there is an existing export block to replace.
        # Check patterns for the beginning of the export block:
        patterns = [
            r'<!-- === Export System Script === -->.*?</body>',
            r'<!-- archviz-skills Export Utility Script -->.*?</body>',
            r'<!-- Export Utility Module — paste BEFORE </body> of any archviz HTML template -->.*?</body>',
            r'<style id="archviz-export-styles">.*?</body>',
            r'<script>\s*/\* archviz-skills Export System.*?</body>'
        ]
        
        replaced = False
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                # We replace everything from the match start to </body> (exclusive)
                match_start = match.start()
                match_end = content.find("</body>", match_start)
                if match_end != -1:
                    print(f"Syncing export module to {f.name}...")
                    # Construct new content
                    new_content = content[:match_start] + "<!-- archviz-skills Export Utility Module -->\n" + new_export_block + content[match_end:]
                    f.write_text(new_content, encoding="utf-8")
                    replaced = True
                    break
        
        if not replaced:
            # If no pattern was matched but the template has window.archvizExport in it, warn
            if "archvizExport" in content:
                print(f"WARNING: {f.name} contains archvizExport but no known export block pattern was matched!")

if __name__ == "__main__":
    sync()
