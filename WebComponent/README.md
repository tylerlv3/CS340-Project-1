# README.md

# Flask App

This is a Flask application boilerplate that provides a basic structure for building web applications using the Flask framework.

## Project Structure

```
flask-app
├── src
│   ├── static
│   │   └── styles.css
│   ├── templates
│   │   ├── base.html
│   │   └── index.html
│   ├── app.py
│   └── config.py
├── tests
│   └── test_app.py
├── requirements.txt
├── .env
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd flask-app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python src/app.py
   ```

## Usage

- Access the application in your web browser at `http://127.0.0.1:5000/`.

## Testing

To run the tests, use the following command:
```bash
pytest tests/test_app.py
```

## License

This project is licensed under the MIT License.