

# AI Chatbot Project


This project is a Flask-based AI chatbot application that allows users to interact with a chatbot through a web interface.


## Project Structure

```
ai-chatbot
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── static
│   └── templates
├── tests
│   ├── __init__.py
│   └── test_routes.py
├── requirements.txt
├── config.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-chatbot
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python -m app
   ```

2. Open your web browser and go to `http://127.0.0.1:5000` to interact with the chatbot.

## Testing

To run the tests, ensure your virtual environment is activated and run:
```
pytest
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
