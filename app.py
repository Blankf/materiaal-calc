from flask import Flask, render_template_string, request, send_file
from collections import defaultdict
import os

app = Flask(__name__)

# Enable debug mode via environment variable
DEBUG_MODE = os.environ.get('DEBUG', 'false').lower() == 'true'

def debug_print(msg):
    if DEBUG_MODE:
        print(f"DEBUG: {msg}")

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Materiaal Uitslag Samenvatting</title>
    <style>
        :root {
            --bg-color: #1a1a1a;
            --container-bg: #2d2d2d;
            --text-color: #ffffff;
            --input-bg: #3d3d3d;
            --input-border: #555;
            --table-bg: #2d2d2d;
            --table-header-bg: #404040;
            --table-border: #555;
            --btn-bg: #0078d7;
            --btn-hover: #005fa3;
            --debug-bg: #3d3d3d;
            --debug-border: #666;
            --shadow: 0 2px 8px rgba(0,0,0,0.3);
        }

        [data-theme="light"] {
            --bg-color: #f7f7f7;
            --container-bg: #ffffff;
            --text-color: #333333;
            --input-bg: #ffffff;
            --input-border: #ccc;
            --table-bg: #ffffff;
            --table-header-bg: #eee;
            --table-border: #ccc;
            --btn-bg: #0078d7;
            --btn-hover: #005fa3;
            --debug-bg: #f0f0f0;
            --debug-border: #ccc;
            --shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        body {
            font-family: Arial, sans-serif;
            margin: 2em;
            background: var(--bg-color);
            color: var(--text-color);
            transition: all 0.3s ease;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2em;
        }

        .logo {
            height: 60px;
            width: auto;
        }

        .theme-toggle {
            background: var(--btn-bg);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s ease;
        }

        .theme-toggle:hover {
            background: var(--btn-hover);
        }

        textarea {
            width: 100%;
            height: 200px;
            background: var(--input-bg);
            color: var(--text-color);
            border: 1px solid var(--input-border);
            border-radius: 4px;
            padding: 8px;
            font-family: monospace;
            transition: all 0.3s ease;
        }

        textarea:focus {
            outline: none;
            border-color: var(--btn-bg);
        }

        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 2em;
            background: var(--table-bg);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: var(--shadow);
        }

        th, td {
            border: 1px solid var(--table-border);
            padding: 12px;
            text-align: left;
        }

        th {
            background: var(--table-header-bg);
            font-weight: bold;
        }

        tr:nth-child(even) {
            background: rgba(255,255,255,0.05);
        }

        [data-theme="light"] tr:nth-child(even) {
            background: rgba(0,0,0,0.02);
        }

        .container {
            max-width: 1000px;
            margin: auto;
            background: var(--container-bg);
            padding: 2em;
            border-radius: 12px;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
        }

        .btn {
            background: var(--btn-bg);
            color: #fff;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .btn:hover {
            background: var(--btn-hover);
            transform: translateY(-1px);
        }

        .debug {
            background: var(--debug-bg);
            padding: 1em;
            margin: 1em 0;
            border-left: 4px solid var(--debug-border);
            font-family: monospace;
            white-space: pre-wrap;
            border-radius: 4px;
            font-size: 12px;
        }

        .debug-mode-indicator {
            color: #ff9800;
            font-weight: bold;
            margin-bottom: 1em;
            padding: 8px;
            background: rgba(255, 152, 0, 0.1);
            border-radius: 4px;
            border-left: 4px solid #ff9800;
        }

        label {
            font-weight: bold;
            margin-bottom: 8px;
            display: block;
        }

        h2 {
            margin-top: 0;
            color: var(--text-color);
        }

        h3 {
            color: var(--text-color);
            border-bottom: 2px solid var(--btn-bg);
            padding-bottom: 8px;
        }
    </style>
    <script>
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);

            const btn = document.querySelector('.theme-toggle');
            btn.textContent = newTheme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
        }

        // Load saved theme on page load
        document.addEventListener('DOMContentLoaded', function() {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            document.documentElement.setAttribute('data-theme', savedTheme);

            const btn = document.querySelector('.theme-toggle');
            btn.textContent = savedTheme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
        });
    </script>
</head>
<body>
<div class="container">
    <div class="header">
        <img src="/logo" alt="Leurs Logo" class="logo">
        <button class="theme-toggle" onclick="toggleTheme()">☀️ Light Mode</button>
    </div>

    <h2>Materiaal Uitslag Samenvatting</h2>

    {% if debug_mode %}
    <div class="debug-mode-indicator">🔧 DEBUG MODE ENABLED</div>
    {% endif %}

    <form method="post">
        <label for="csv">Paste your tab-separated CSV content here:</label>
        <textarea name="csv" id="csv" placeholder="Paste your CSV data here...">{{ csv|default('') }}</textarea>
        <br><br>
        <button class="btn" type="submit">🔢 Calculate</button>
    </form>

    {% if debug_info %}
    <h3>🐛 Debug Information</h3>
    <div class="debug">{{ debug_info }}</div>
    {% endif %}

    {% if result %}
    <h3>📊 Result</h3>
    <table>
        <tr>
            <th>Materiaal</th>
            <th>TotaalUitslagLengte_m</th>
            <th>TotaalUitslagBreedte_m</th>
            <th>TotaalUitslagOpgeteld_m</th>
        </tr>
        {% for row in result %}
        <tr>
            <td>{{ row['Materiaal'] }}</td>
            <td>{{ row['TotaalUitslagLengte_m'] }}</td>
            <td>{{ row['TotaalUitslagBreedte_m'] }}</td>
            <td>{{ row['TotaalUitslagOpgeteld_m'] }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
</div>
</body>
</html>
'''

def materiaal_uitslag_samenvatting(csv_text):
    debug_info = []
    lines = csv_text.strip().split('\n')
    debug_print(f"Total lines: {len(lines)}")

    if len(lines) < 2:
        return [], "No data found"

    # Parse header to find column positions
    header = lines[0].split('\t')
    header = [col.strip() for col in header]
    debug_print(f"Header: {header}")

    # Find column indices
    try:
        materiaal_idx = header.index('Materiaal')
        lengte_idx = header.index('Lengte')
        breedte_idx = header.index('Breedte')
        aantal_idx = header.index('Aantal')
        kant_x2_idx = header.index('Kant_X2')
        kant_x1_idx = header.index('Kant_X1')
        kant_y1_idx = header.index('Kant_Y1')
        kant_y2_idx = header.index('Kant_Y2')
        debug_print(f"Column indices: Materiaal={materiaal_idx}, Lengte={lengte_idx}, Breedte={breedte_idx}")
    except ValueError as e:
        return [], f'Missing column: {e}'

    # Process each data row
    uitslagen = []
    processed_count = 0
    skipped_count = 0

    for line_num, line in enumerate(lines[1:], 2):
        if not line.strip():
            continue
        cols = line.split('\t')
        debug_print(f"Line {line_num}: {len(cols)} columns")

        # Check if we have at least the minimum required columns
        min_required_cols = max(materiaal_idx, lengte_idx, breedte_idx, aantal_idx) + 1
        if len(cols) < min_required_cols:
            debug_print(f"Line {line_num}: Not enough columns ({len(cols)} < {min_required_cols}), skipping")
            skipped_count += 1
            continue

        try:
            materiaal = cols[materiaal_idx].strip()
            debug_print(f"Line {line_num}: materiaal='{materiaal}' (len={len(materiaal)})")

            # Special debug for "geen materiaal_18"
            if "geen materiaal" in materiaal.lower():
                debug_print(f"Line {line_num}: Found 'geen materiaal' case: '{materiaal}'")
                debug_print(f"Line {line_num}: Raw line: '{line}'")
                debug_print(f"Line {line_num}: Split cols: {cols}")
                debug_print(f"Line {line_num}: Column count: {len(cols)}, Required indices: X2={kant_x2_idx}, X1={kant_x1_idx}, Y1={kant_y1_idx}, Y2={kant_y2_idx}")

            if len(materiaal) == 0:
                debug_print(f"Line {line_num}: Empty materiaal, skipping")
                skipped_count += 1
                continue

            lengte = float(cols[lengte_idx].strip().replace(',', '.'))
            breedte = float(cols[breedte_idx].strip().replace(',', '.'))
            aantal = int(cols[aantal_idx].strip()) if cols[aantal_idx].strip().isdigit() else 1

            # Safely get edge values with bounds checking
            kant_x2 = cols[kant_x2_idx].strip() if kant_x2_idx < len(cols) and cols[kant_x2_idx] else ''
            kant_x1 = cols[kant_x1_idx].strip() if kant_x1_idx < len(cols) and cols[kant_x1_idx] else ''
            kant_y1 = cols[kant_y1_idx].strip() if kant_y1_idx < len(cols) and cols[kant_y1_idx] else ''
            kant_y2 = cols[kant_y2_idx].strip() if kant_y2_idx < len(cols) and cols[kant_y2_idx] else ''

            # Special debug for "geen materiaal_18"
            if "geen materiaal" in materiaal.lower():
                debug_print(f"Line {line_num}: Edge values - X2='{kant_x2}', X1='{kant_x1}', Y1='{kant_y1}', Y2='{kant_y2}'")
                debug_print(f"Line {line_num}: Dimensions - L={lengte}, B={breedte}, aantal={aantal}")

            # Calculate uitslag - exact PowerShell logic
            uitslag_lengte = 0
            uitslag_breedte = 0

            aantal_x_l = 0
            if kant_x2 == 'X':
                aantal_x_l += 1
            if kant_x1 == 'X':
                aantal_x_l += 1
            if aantal_x_l > 0:
                uitslag_lengte = (lengte * aantal_x_l + (aantal_x_l * 50)) * aantal

            aantal_x_b = 0
            if kant_y1 == 'X':
                aantal_x_b += 1
            if kant_y2 == 'X':
                aantal_x_b += 1
            if aantal_x_b > 0:
                uitslag_breedte = (breedte * aantal_x_b + (aantal_x_b * 50)) * aantal

            # Special debug for "geen materiaal_18"
            if "geen materiaal" in materiaal.lower():
                debug_print(f"Line {line_num}: aantal_x_l={aantal_x_l}, aantal_x_b={aantal_x_b}")
                debug_print(f"Line {line_num}: Final calculation - L={uitslag_lengte}, B={uitslag_breedte}")

            debug_print(f"Line {line_num}: {materiaal} -> L={uitslag_lengte}, B={uitslag_breedte}")

            # Special debug for "geen materiaal_18"
            if "geen materiaal" in materiaal.lower():
                debug_print(f"Line {line_num}: 'geen materiaal' final: L={uitslag_lengte}, B={uitslag_breedte}, processed={uitslag_lengte > 0 or uitslag_breedte > 0}")

            uitslagen.append({
                'Materiaal': materiaal,
                'UitslagLengte': uitslag_lengte,
                'UitslagBreedte': uitslag_breedte
            })

            # Special debug for "geen materiaal_18"
            if "geen materiaal" in materiaal.lower():
                debug_print(f"Line {line_num}: Added to uitslagen: {materiaal} with L={uitslag_lengte}, B={uitslag_breedte}")

            processed_count += 1

        except (ValueError, IndexError) as e:
            debug_print(f"Line {line_num}: Error processing - {e}")
            skipped_count += 1
            continue

    debug_print(f"Processed: {processed_count}, Skipped: {skipped_count}")

    # Debug: Show all unique materials found
    unique_materials = set(item['Materiaal'] for item in uitslagen)
    debug_print(f"Unique materials in uitslagen: {sorted(unique_materials)}")
    for mat in sorted(unique_materials):
        if ' ' in mat:
            debug_print(f"Material with space: '{mat}'")

    # Group by Materiaal and sum
    grouped = defaultdict(lambda: {'UitslagLengte': 0, 'UitslagBreedte': 0})
    for item in uitslagen:
        grouped[item['Materiaal']]['UitslagLengte'] += item['UitslagLengte']
        grouped[item['Materiaal']]['UitslagBreedte'] += item['UitslagBreedte']

        # Special debug for "geen materiaal_18"
        if "geen materiaal" in item['Materiaal'].lower():
            debug_print(f"Grouping: Added {item['Materiaal']} with L={item['UitslagLengte']}, B={item['UitslagBreedte']}")
            debug_print(f"Grouping: Total now for '{item['Materiaal']}': L={grouped[item['Materiaal']]['UitslagLengte']}, B={grouped[item['Materiaal']]['UitslagBreedte']}")

    debug_print(f"Grouped materials: {list(grouped.keys())}")

    # Special debug for "geen materiaal_18"
    for mat_name in grouped.keys():
        if "geen materiaal" in mat_name.lower():
            debug_print(f"Found 'geen materiaal' in grouped materials: '{mat_name}'")

    # Format result
    result = []
    for materiaal, totals in grouped.items():
        totaal_lengte = totals['UitslagLengte'] / 1000
        totaal_breedte = totals['UitslagBreedte'] / 1000
        totaal_opgeteld = totaal_lengte + totaal_breedte

        # Special debug for "geen materiaal_18"
        if "geen materiaal" in materiaal.lower():
            debug_print(f"Final result for '{materiaal}': L={totaal_lengte}, B={totaal_breedte}, Total={totaal_opgeteld}")

        result.append({
            'Materiaal': materiaal,
            'TotaalUitslagLengte_m': round(totaal_lengte, 2),
            'TotaalUitslagBreedte_m': round(totaal_breedte, 2),
            'TotaalUitslagOpgeteld_m': round(totaal_opgeteld, 2)
        })

    # Sort by Materiaal
    result = sorted(result, key=lambda x: x['Materiaal'])

    debug_summary = f"Processed {processed_count} rows, skipped {skipped_count} rows\nFound materials: {[r['Materiaal'] for r in result]}"
    return result, debug_summary if DEBUG_MODE else ""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    debug_info = ""
    csv = ''
    if request.method == 'POST':
        csv = request.form['csv']
        try:
            result, debug_info = materiaal_uitslag_samenvatting(csv)
        except Exception as e:
            result = [{'Materiaal': 'Error', 'TotaalUitslagLengte_m': str(e), 'TotaalUitslagBreedte_m': '', 'TotaalUitslagOpgeteld_m': ''}]
            debug_info = f"Exception: {e}"
    return render_template_string(HTML, result=result, csv=csv, debug_info=debug_info, debug_mode=DEBUG_MODE)

@app.route('/logo')
def serve_logo():
    return send_file('leurs_logo.jpg', mimetype='image/jpeg')

def test_geen_materiaal_case():
    """Test the specific 'geen materiaal_18' case"""
    # Data from CSV: geen materiaal_18	1	563.0	520.0	2	Legplank	K2 OVEN		X
    materiaal = "geen materiaal_18"
    lengte = 563.0
    breedte = 520.0
    aantal = 2
    kant_x2 = ""  # empty
    kant_x1 = "X"
    kant_y1 = ""  # empty
    kant_y2 = ""  # empty

    print(f"Testing: {materiaal}")
    print(f"Dimensions: L={lengte}, B={breedte}, aantal={aantal}")
    print(f"Edges: X2='{kant_x2}', X1='{kant_x1}', Y1='{kant_y1}', Y2='{kant_y2}'")

    # Calculate uitslag - exact PowerShell logic
    uitslag_lengte = 0
    uitslag_breedte = 0

    aantal_x_l = 0
    if kant_x2 == 'X':
        aantal_x_l += 1
        print(f"X2 is X, aantal_x_l now: {aantal_x_l}")
    if kant_x1 == 'X':
        aantal_x_l += 1
        print(f"X1 is X, aantal_x_l now: {aantal_x_l}")
    if aantal_x_l > 0:
        uitslag_lengte = (lengte * aantal_x_l + (aantal_x_l * 50)) * aantal
        print(f"Length calculation: ({lengte} * {aantal_x_l} + ({aantal_x_l} * 50)) * {aantal} = {uitslag_lengte}")

    aantal_x_b = 0
    if kant_y1 == 'X':
        aantal_x_b += 1
        print(f"Y1 is X, aantal_x_b now: {aantal_x_b}")
    if kant_y2 == 'X':
        aantal_x_b += 1
        print(f"Y2 is X, aantal_x_b now: {aantal_x_b}")
    if aantal_x_b > 0:
        uitslag_breedte = (breedte * aantal_x_b + (aantal_x_b * 50)) * aantal
        print(f"Width calculation: ({breedte} * {aantal_x_b} + ({aantal_x_b} * 50)) * {aantal} = {uitslag_breedte}")
    else:
        print("No Y edges marked, width uitslag = 0")

    print(f"Final result: L={uitslag_lengte}, B={uitslag_breedte}")
    print(f"In meters: L={uitslag_lengte/1000:.3f}, B={uitslag_breedte/1000:.3f}, Total={(uitslag_lengte+uitslag_breedte)/1000:.3f}")
    return uitslag_lengte, uitslag_breedte

# Run test when module is executed directly
if __name__ == '__main__':
    if os.environ.get('TEST_MODE') == 'true':
        test_geen_materiaal_case()
    else:
        app.run(host='0.0.0.0', port=8080)
