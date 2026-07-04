with open('build_master_map.py', 'r') as f:
    lines = f.readlines()

out_lines = []
in_garbage = False

for line in lines:
    if "HTML = HTML.replace('__SUBCTY_STATS__', subcounty_summary_js)" in line and "<div style=" in line:
        out_lines.append("HTML = HTML.replace('__SUBCTY_STATS__', subcounty_summary_js)\n")
        in_garbage = True
        continue
    
    if in_garbage:
        if line.strip() == 'print(f"  📄 HTML size: {len(HTML)/1024:.0f} KB")':
            in_garbage = False
            out_lines.append(line)
        continue
        
    out_lines.append(line)

with open('build_master_map.py', 'w') as f:
    f.writelines(out_lines)
print("File fixed.")
