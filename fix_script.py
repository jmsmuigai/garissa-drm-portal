import re
with open("build_master_map.py", "r") as f:
    text = f.read()

# I will find where the first instance of 'HTML = HTML.replace('__SUBCTY_STATS__', subcounty_summary_js)' is,
# and where the second one is, or I will just look for the end of the good block.
idx1 = text.find("HTML = HTML.replace('__SUBCTY_STATS__', subcounty_summary_js)")
if idx1 != -1:
    idx2 = text.find("HTML = HTML.replace('__SUBCTY_STATS__', subcounty_summary_js)", idx1 + 10)
    
    # We want to keep everything up to idx1 + len(...)
    # Then skip the garbage which includes the rest of the old HTML f-string all the way to the end of the old replace block.
    # The end of the old replace block is exactly the second `HTML = HTML.replace('__SUBCTY_STATS__', subcounty_summary_js)`
    if idx2 != -1:
        good_part = text[:idx1 + len("HTML = HTML.replace('__SUBCTY_STATS__', subcounty_summary_js)")]
        rest_of_file = text[idx2 + len("HTML = HTML.replace('__SUBCTY_STATS__', subcounty_summary_js)"): ]
        
        # However, the garbage had `        <div style="margin-top:6px...` appended to it. Let's just find the next valid line which is `print(f"  📄 HTML size:` or similar.
        idx_print = text.find('print(f"  📄 HTML size:', idx1)
        
        with open("build_master_map_fixed.py", "w") as out:
            out.write(good_part + "\n\n" + text[idx_print:])
            print("Fixed!")
