
# Email Cleaner

The Email Cleaner is a Python script designed to validate and clean email lists. It performs various checks to ensure the emails are valid, active, and not associated with spam traps.

## Features

- Validates email addresses using regular expressions.
- Removes duplicate email addresses from the list.
- Checks MX records to determine email domain activity.
- Detects potential spam trap email addresses based on patterns and known disposable email services.

## Requirements

- Python 3.x
- `dnspython` library for DNS queries (`pip install dnspython`)

## Usage

1. **Input File**: Create a CSV file containing the list of email addresses to be cleaned. Each email address should be in a separate row.

2. **Run Script**: Execute the `email_cleaner.py` script, providing the path to the input CSV file as an argument.

    ```bash
    python email_cleaner.py path/to/emails.csv
    ```

3. **Output**: The script will display the cleaned email list along with statistics on invalid, inactive, and potential spam trap email addresses.

## Example

Suppose you have a CSV file named `emails.csv` containing the following email addresses:

```
john@example.com
mary@example.com
spamtrap@example.com
invalid-email
```

Running the script:

```bash
python email_cleaner.py emails.csv
```

Output:

```
Cleaned Email List:
john@example.com
mary@example.com

Total cleaned emails: 2
Invalid emails: 1
Inactive emails: 0
Spam trap emails: 1
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to adjust the content according to your preferences and requirements!
