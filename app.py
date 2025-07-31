from flask import Flask, render_template, request, send_file
from collections import defaultdict
import os

app = Flask(__name__)

# Enable debug mode via environment variable
DEBUG_MODE = os.environ.get('DEBUG', 'false').lower() == 'true'

def debug_print(msg):
    if DEBUG_MODE:
        print(f"DEBUG: {msg}")

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
    return render_template('index.html', result=result, csv=csv, debug_info=debug_info, debug_mode=DEBUG_MODE)

@app.route('/logo')
def serve_logo():
    return send_file('leurs_logo.jpg', mimetype='image/jpeg')

def materiaal_uitslag_samenvatting(csv_text):
    debug_info = []
    lines = csv_text.strip().split('\n')
    debug_print(f"Total lines: {len(lines)}")

    if len(lines) < 1:
        return [], "No data found"

    # Check if first line contains headers or data
    first_line = lines[0].split('\t')
    first_line = [col.strip() for col in first_line]
    debug_print(f"First line: {first_line}")

    # Detect if headers are present by checking for known header names
    has_headers = any(col in ['Materiaal', 'Lengte', 'Breedte', 'Aantal', 'Kant_X2', 'Kant_X1', 'Kant_Y1', 'Kant_Y2'] for col in first_line)
    debug_print(f"Headers detected: {has_headers}")

    data_start_line = 1 if has_headers else 0

    if has_headers:
        # Parse header to find column positions
        header = first_line
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
    else:
        # Use fixed column positions based on expected structure:
        # Materiaal, user0, Lengte, Breedte, Aantal, Onderdeel, Element, Kant_X2, Kant_X1, Kant_Y1, Kant_Y2
        materiaal_idx = 0
        lengte_idx = 2
        breedte_idx = 3
        aantal_idx = 4
        kant_x2_idx = 7
        kant_x1_idx = 8
        kant_y1_idx = 9
        kant_y2_idx = 10
        debug_print(f"Using fixed column indices: Materiaal={materiaal_idx}, Lengte={lengte_idx}, Breedte={breedte_idx}")
        debug_print("Expected structure: Materiaal, user0, Lengte, Breedte, Aantal, Onderdeel, Element, Kant_X2, Kant_X1, Kant_Y1, Kant_Y2")

    # Process each data row
    uitslagen = []
    processed_count = 0
    skipped_count = 0

    for line_num, line in enumerate(lines[data_start_line:], data_start_line + 1):
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
