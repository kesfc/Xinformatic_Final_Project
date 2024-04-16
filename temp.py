import pandas as pd

# Step 1: Read data from CSV
data = pd.read_csv('results.txt')

# Step 2: Optionally, manipulate or clean the data if needed

# Step 3: Generate HTML code
html_output = data.to_html(index=False)  # Convert DataFrame to HTML without index column

# Step 4: Optionally, apply CSS for styling
css_style = """
<style>
    /* Add your CSS styles here */
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
    }
</style>
"""

# Combine HTML and CSS
html_output_with_style = f"<html><head>{css_style}</head><body>{html_output}</body></html>"

# Write HTML to a file
with open('results.html', 'w') as f:
    f.write(html_output_with_style)