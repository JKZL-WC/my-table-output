from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Load the CSV file
        table1 = pd.read_csv('Table_Input.csv')

        # Check if required columns exist
        if 'Index #' not in table1.columns or 'Value' not in table1.columns:
            return "Error: Required columns 'Index #' or 'Value' not found in the CSV file."

        # Perform calculations
        # Locate values based on "Index #"
        table1.set_index('Index #', inplace=True)

        alpha = table1.loc['A5', 'Value'] + table1.loc['A20', 'Value'] if 'A5' in table1.index and 'A20' in table1.index else 0
        beta = table1.loc['A15', 'Value'] / table1.loc['A7', 'Value'] if 'A15' in table1.index and 'A7' in table1.index and table1.loc['A7', 'Value'] != 0 else "Infinity"
        charlie = table1.loc['A13', 'Value'] * table1.loc['A12', 'Value'] if 'A13' in table1.index and 'A12' in table1.index else 0

        # Prepare data for rendering
        table1_data = table1.reset_index().to_dict(orient='records')  # Reset index for rendering
        table2_data = {
            'Alpha': alpha,
            'Beta': beta,
            'Charlie': charlie
        }

        return render_template('index.html', table1=table1_data, table2=table2_data)

    except FileNotFoundError:
        return "Error: 'Table_Input.csv' file not found. Please add the file to the directory."

    except Exception as e:
        return f"Unexpected error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
