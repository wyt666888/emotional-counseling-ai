# Installation Instructions

## Environment Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Other dependencies mentioned in the `requirements.txt` file.

## Translation Feature Requirements

To enable the translation feature, you will need to install the following dependency:

- `deep-translator`

You can install it via pip:
```bash
pip install deep-translator
```

### Network Requirements

- Ensure that your application can connect to the internet.
- The translation feature requires access to the Google Translate API. Network connectivity must allow outbound requests to the translation service endpoints.

## Backend Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/wyt666888/emotional-counseling-ai.git
   cd emotional-counseling-ai
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install deep-translator
   ```
3. Configure environment variables as specified in the documentation.
4. Run the application.

## Additional Notes

- Make sure to check the official documentation of `deep-translator` for any additional configuration you might need.
- For any issues related to network connectivity, please check your firewall settings or consult with your network administrator.