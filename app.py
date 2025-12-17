from flask import Flask, render_template, request, send_file
from datetime import datetime
import io
from xhtml2pdf import pisa

app = Flask(__name__)

# Business Details
BUSINESS_INFO = {
    'name': 'Rifa Appliances',
    'address_line1': '93, Taj complex, Kumarsamy Patty',
    'address_line2': 'Salem, TamilNadu-636007',
    'country': 'India',
    'gstin': '33CCYPS5494Q1Z5',
    'contact': '91-9150328675',
    'email': 'rifawahid1@gmail.com'
}

def number_to_words(n):
    """Convert number to Title Case words (Indian Numbering System)"""
    n = int(n)
    if n == 0:
        return "Zero Only"

    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    def convert_hundreds(num):
        parts = []
        if num >= 100:
            parts.append(units[num // 100] + " Hundred")
            num %= 100
        
        if num >= 20:
            parts.append(tens[num // 10])
            if num % 10 > 0:
                parts.append(units[num % 10])
        elif num >= 10:
            parts.append(teens[num - 10])
        elif num > 0:
            parts.append(units[num])
        
        return " ".join(parts)

    words = []
    
    # Crores
    if n >= 10000000:
        crores = n // 10000000
        words.append(convert_hundreds(crores) + " Crore")
        n %= 10000000
    
    # Lakhs
    if n >= 100000:
        lakhs = n // 100000
        words.append(convert_hundreds(lakhs) + " Lakh")
        n %= 100000
    
    # Thousands
    if n >= 1000:
        thousands = n // 1000
        words.append(convert_hundreds(thousands) + " Thousand")
        n %= 1000
        
    # Remaining hundreds
    if n > 0:
        words.append(convert_hundreds(n))

    # Join all parts
    result = " ".join(words)
    
    # Return formatted string matching your Invoice PDF requirement
    # If you strictly want just the words without "Indian Rupee", remove that prefix below.
    return f"{result} Only"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    # 1. Collect Form Data
    invoice_number = request.form.get('invoice_number')
    invoice_date = request.form.get('invoice_date')
    
    bill_to = {
        'name': request.form.get('bill_name'),
        'address': request.form.get('bill_address'),
        'city': request.form.get('bill_city'),
        'state': request.form.get('bill_state'),
        'pincode': request.form.get('bill_pincode')
    }
    
    ship_to = {
        'name': request.form.get('ship_name'),
        'address': request.form.get('ship_address'),
        'city': request.form.get('ship_city'),
        'state': request.form.get('ship_state'),
        'pincode': request.form.get('ship_pincode')
    }
    
    # 2. Process Items
    global_tax_rate = float(request.form.get('tax_rate', 18))
    cgst_rate = global_tax_rate / 2
    sgst_rate = global_tax_rate / 2
    
    items = []
    descriptions = request.form.getlist('description[]')
    hsn_codes = request.form.getlist('hsn[]')
    quantities = request.form.getlist('qty[]')
    rates = request.form.getlist('rate[]')
    
    sub_total = 0
    total_cgst = 0
    total_sgst = 0
    
    for i in range(len(descriptions)):
        if descriptions[i]:
            qty = float(quantities[i])
            rate = float(rates[i])
            base_amount = qty * rate
            
            cgst_amt = base_amount * (cgst_rate / 100)
            sgst_amt = base_amount * (sgst_rate / 100)
            
            items.append({
                'sno': i + 1,
                'description': descriptions[i],
                'hsn': hsn_codes[i],
                'qty': qty,
                'rate': rate,
                'cgst_rate': cgst_rate,
                'cgst_amt': cgst_amt,
                'sgst_rate': sgst_rate,
                'sgst_amt': sgst_amt,
                'taxable_amount': base_amount
            })
            
            sub_total += base_amount
            total_cgst += cgst_amt
            total_sgst += sgst_amt

    # 3. Calculations
    grand_total_raw = sub_total + total_cgst + total_sgst
    grand_total_rounded = round(grand_total_raw)
    adjustment = grand_total_rounded - grand_total_raw
    
    payment_made = float(request.form.get('payment_made', 0))
    balance_due = grand_total_rounded - payment_made
    
    # 4. Render Template
    rendered_html = render_template('invoice.html',
        business=BUSINESS_INFO,
        invoice_number=invoice_number,
        invoice_date=datetime.strptime(invoice_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
        bill_to=bill_to,
        ship_to=ship_to,
        items=items,
        sub_total=sub_total,
        cgst_total=total_cgst,
        sgst_total=total_sgst,
        cgst_rate=cgst_rate,
        sgst_rate=sgst_rate,
        adjustment=adjustment,
        grand_total=grand_total_rounded,
        payment_made=payment_made,
        balance_due=balance_due,
        amount_in_words=number_to_words(grand_total_rounded)
    )
    
    # 5. Create PDF using xhtml2pdf
    pdf_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(
        io.BytesIO(rendered_html.encode("utf-8")),
        dest=pdf_file
    )
    
    if pisa_status.err:
        return "Error generating PDF", 500
        
    pdf_file.seek(0)
    
    return send_file(pdf_file, 
                     as_attachment=True,
                     download_name=f'Invoice_{invoice_number}.pdf',
                     mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)