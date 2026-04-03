import codecs
import re

latex_file_path = "C:\\Users\\Kitae Kim\\.gemini\\antigravity\\scratch\\academic-homepage\\data.tex"
html_file_path = "C:\\Users\\Kitae Kim\\.gemini\\antigravity\\scratch\\academic-homepage\\index.html"

with open(latex_file_path, "r", encoding="utf-8") as f:
    content = f.read()

def clean_latex(text):
    text = text.replace("\\textbf{Kitae Kim}", "<strong>Kitae Kim</strong>")
    text = text.replace("\\textbf{(Corresponding author)}", "<strong>(Corresponding author)</strong>")
    text = text.replace("\\textbf{BK IF =1}", "<strong>(BK IF =1)</strong>")
    text = re.sub(r"\\textit\{(.*?)\}", r"<em>\1</em>", text)
    text = text.replace("``", "\"").replace("''", "\"").replace("”", "\"").replace("“", "\"").replace("”", "\"")
    return text.strip()

# parse awards
awards_match = re.search(r"\\sectiontable\{Awards\}\{(.*?)\}", content, re.DOTALL)
awards_html = ""
if awards_match:
    awards_raw = awards_match.group(1)
    entries = re.findall(r"\\entry\{(.*?)\}\{(.*?)\\hfill\s*(.*?)\}", awards_raw)
    awards_html += "        <!-- Awards -->\n        <section id=\"awards\">\n          <h2>Honors & Awards</h2>\n          <table class=\"classic-table\">\n"
    for title, venue, year in entries:
        title = clean_latex(title)
        venue = clean_latex(venue)
        year = clean_latex(year)
        awards_html += f"            <tr>\n              <td class=\"year-col\">{year}</td>\n              <td><strong>{title}</strong><br><em>{venue}</em></td>\n            </tr>\n"
    awards_html += "          </table>\n        </section>\n\n        <hr>\n\n"

categories = [
    "International Journal",
    "Domestic Journal",
    "International Conference",
    "Domestic Conference",
    "International Patent",
    "Domestic Patent"
]

pubs_html = "        <!-- Publications -->\n        <section id=\"publications\">\n          <h2>Publications</h2>\n"

for i, cat in enumerate(categories):
    start_str = f"\\textbf{{{cat}}}"
    if start_str in content:
        start_idx = content.find(start_str)
        end_idx = len(content)
        for j in range(i+1, len(categories)):
            next_str = f"\\textbf{{{categories[j]}}}"
            if next_str in content:
                end_idx = content.find(next_str, start_idx)
                break
            
        block = content[start_idx:end_idx]
        itemsRaw = re.findall(r"\\item\s+(.*?)(?=\n\s*\\item|\n\s*\\end\{enumerate\}|\Z)", block, re.DOTALL)
        
        if itemsRaw:
            pubs_html += f"          <h3>{cat}</h3>\n          <ol class=\"publication-list\">\n"
            for item in itemsRaw:
                item_clean = clean_latex(item)
                item_clean = ' '.join(item_clean.split())
                pubs_html += f"            <li>{item_clean}</li>\n"
            pubs_html += "          </ol>\n\n"

pubs_html += "        </section>\n"

with open(html_file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# We need to strip out the messy end and replace it correctly.
# The safe part ends at:
safe_marker = "            </table>\n        </section>"
idx = html_content.find(safe_marker)
if idx != -1:
    idx += len(safe_marker)
    footer = """
        <footer class="footer">
            <p>&copy; 2026 Kitae Kim. Last updated: April 2026.</p>
        </footer>
    </div>
</body>
</html>"""
    
    new_html = html_content[:idx] + "\n\n        <hr>\n\n" + awards_html + pubs_html + footer
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Done")
else:
    print("Failed to find marker")
