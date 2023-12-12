from flask import Flask, render_template, request, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

class CalculationForm(FlaskForm):
    number1 = StringField('Number 1')
    number2 = StringField('Number 2')
    calculate = SubmitField('Calculate')
    print_pdf = SubmitField('Print PDF')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CalculationForm()
    result = None

    if request.method == 'POST' and form.validate_on_submit():
        # Calculation on the server side
        number1 = float(form.number1.data)
        number2 = float(form.number2.data)
        result = number1 + number2

        # Create a DataFrame and write to Excel sheet
        df = pd.DataFrame({'Number 1': [number1], 'Number 2': [number2], 'Result': [result]})

        if form.print_pdf.data:
            # Generate PDF using reportlab
            pdf_data = BytesIO()
            generate_pdf(pdf_data, df)

            # Send PDF as a response
            pdf_data.seek(0)
            return send_file(pdf_data, download_name='calculation_result.pdf', as_attachment=True)

    return render_template('index.html', form=form, result=result)


def generate_pdf(pdf_data, df):
    # Use reportlab to generate PDF content
    pdf_canvas = SimpleDocTemplate(pdf_data, pagesize=letter)
    
    # Set up PDF content
    data = [df.columns.to_list()] + df.astype(str).values.tolist()

    # Create a table style
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#77a7df'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), '#ffffff'),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), '#f0f8ff')])

    # Create the table
    table = Table(data, style=style)


    # Build PDF document
    pdf_canvas.build([table])



if __name__ == '__main__':
    app.run(debug=True)
