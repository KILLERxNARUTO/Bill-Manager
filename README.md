# Bill Manager

A web-based invoice management system built with Flask that allows you to create, manage, and generate professional PDF invoices.

## Features

- Create and manage invoices with customer details
- Add multiple items with descriptions, quantities, and prices
- Automatic calculation of subtotals, GST, and total amounts
- Generate PDF invoices
- Clean and responsive web interface

## Technologies Used

- Python 3.x
- Flask - Web framework
- xhtml2pdf - PDF generation
- reportlab - PDF processing
- HTML/CSS - Frontend

## Installation

1. Clone the repository:
```bash
git clone https://github.com/KILLERxNARUTO/Bill-Manager.git
cd Bill-Manager
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Fill in the invoice details including:
   - Customer information
   - Item descriptions, quantities, and prices
   - Additional notes (optional)

4. Click "Generate Invoice" to create and download a PDF invoice

## Project Structure

```
Bill-Manager/
├── app.py              # Main Flask application
├── templates/
│   ├── index.html      # Invoice creation form
│   └── invoice.html    # Invoice PDF template
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

KILLERxNARUTO

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
