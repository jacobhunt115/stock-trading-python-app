# Stock Trading Python Pipeline

A Python application that fetches stock data from the Polygon.io API and exports it to CSV format. This project demonstrates data pipeline concepts and can be used as a foundation for stock market data analysis and trading applications.

##  Features

- **API Integration**: Fetches real-time stock ticker data from Polygon.io
- **Pagination Handling**: Automatically handles large datasets with pagination
- **CSV Export**: Exports data to CSV format with consistent schema
- **Modular Design**: Organized as a reusable function for data pipeline integration

##  Data Schema

The application exports the following fields for each stock ticker:

| Field | Description |
|-------|-------------|
| `ticker` | Stock symbol (e.g., AAPL, MSFT) |
| `name` | Company name |
| `market` | Market type (stocks) |
| `locale` | Geographic region (us) |
| `primary_exchange` | Exchange code (e.g., XNAS, XNYS) |
| `type` | Security type (e.g., CS for Common Stock) |
| `active` | Trading status (true/false) |
| `currency_name` | Currency (usd) |
| `cik` | Central Index Key |
| `composite_figi` | Composite FIGI identifier |
| `share_class_figi` | Share class FIGI identifier |
| `last_updated_utc` | Last update timestamp |

##  Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/geethasagarb/stock-trading-python-app.git
   cd stock-trading-python-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv pythonenv
   source pythonenv/bin/activate  # On Windows: pythonenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Polygon.io API key:
   ```
   POLYGON_API_KEY=your_actual_api_key_here
   ```

5. **Get a Polygon.io API key**
   - Visit [Polygon.io](https://polygon.io/)
   - Sign up for a free account
   - Get your API key from the dashboard

##  Usage

### Basic Usage

Run the script directly:
```bash
python script.py
```

This will:
1. Fetch all active stock tickers from Polygon.io
2. Handle pagination automatically
3. Export data to `tickers.csv`
4. Display progress and completion status

### Programmatic Usage

Import and use the function in your own code:
```python
from script import run_stock_job

# Run the stock data job
run_stock_job()
```

### Scheduled Execution

The modular design makes it easy to integrate with schedulers:

**Using CRON:**
```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/stock-trading-python-app && python script.py
```

**Using Python scheduler:**
```python
import schedule
import time
from script import run_stock_job

schedule.every().day.at("09:00").do(run_stock_job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

##  Project Structure

```
stock-trading-python-app/
├── script.py              # Main application script
├── scheduler.py           # Scheduler utilities
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── tickers.csv           # Generated CSV output (after running)
└── README.md             # This file
```

##  Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `POLYGON_API_KEY` | Your Polygon.io API key | Yes |

### API Configuration

The script uses the following default settings:
- **Market**: stocks
- **Status**: active only
- **Limit**: 1000 records per request
- **Sort**: by ticker symbol

##  Data Pipeline Integration

This project demonstrates key data pipeline concepts:

- **Data Extraction**: Fetches data from external API
- **Data Processing**: Handles pagination and data transformation
- **Data Storage**: Exports to CSV format
- **Scheduling**: Designed for automated execution
- **Error Handling**: Robust API response handling

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Resources

- [Polygon.io API Documentation](https://polygon.io/docs)
- [Python CSV Documentation](https://docs.python.org/3/library/csv.html)
- [Data Pipeline Best Practices](https://docs.python.org/3/library/csv.html)

## ⚠️ Important Notes

- **API Rate Limits**: Be mindful of Polygon.io rate limits
- **Data Volume**: The full dataset can be large (5000+ records)
- **API Key Security**: Never commit your `.env` file to version control
- **Data Freshness**: Stock data changes frequently; consider regular updates

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your `.env` file contains a valid Polygon.io API key
2. **Network Issues**: Check your internet connection and API endpoint availability
3. **Permission Errors**: Ensure you have write permissions for the output directory

