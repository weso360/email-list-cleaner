import re
import csv
import os
import time
import dns.resolver  # Import the dnspython library for DNS queries

def is_valid_email(email):
    # Regular expression for basic email validation
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

def remove_duplicates(email_list):
    # Convert list to set to remove duplicates, then back to list
    return list(set(email_list))

def check_mx_records(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return mx_records
    except dns.resolver.NoAnswer:
        print(f"No MX records found for {domain}")
        return None
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist")
        return None
    except dns.resolver.Timeout:
        print("DNS query timed out")
        return None
    except dns.resolver.NoNameservers:
        print("No nameservers available for resolving the domain")
        return None
    except dns.exception.DNSException as e:
        print(f"DNS resolution error: {e}")
        return None

def check_spam_traps(email):
    # More advanced spam trap detection based on multiple factors
    # This is a simplified version and may not cover all scenarios

    # Common spam trap patterns
    spam_trap_patterns = ['abuse', 'spam', 'trap', 'admin', 'postmaster']

    # Email address patterns that may indicate a spam trap
    email_patterns = [
        # Common spam trap domains
        'mailinator.com', 'guerrillamail.com', '10minutemail.com', 'dispostable.com',
        # Suspicious patterns in email local parts
        'admin@', 'contact@', 'abuse@', 'postmaster@', 'info@', 'noreply@', 'support@',
        'newsletter@', 'marketing@', 'sales@', 'service@', 'customerservice@', 'noreply@',
        # Long alphanumeric strings
        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@', '11111111111111111111111111111111111111111111111@',
        # Random combinations of characters
        'xyzyxzxzxxyxxyzyxyxzyzxxyxyxyxyx@', 'qazxswedcvfrtgbnhytgbvfredcxswqaz@'
    ]

    # Check for common spam trap patterns in the email address
    for pattern in spam_trap_patterns:
        if pattern in email:
            return True

    # Check for suspicious patterns in the email local part
    local_part = email.split('@')[0]
    for pattern in email_patterns:
        if pattern in local_part:
            return True

    # Check if the email domain is a common disposable email service
    disposable_domains = ['mailinator.com', 'guerrillamail.com', '10minutemail.com', 'dispostable.com']
    domain = email.split('@')[-1]
    if domain in disposable_domains:
        return True

    # Check if the domain has a poor reputation (you'll need a reputation database or service for this)
    # For demonstration purposes, let's assume any domain without MX records has a poor reputation
    if not check_mx_records(domain):
        return True

    # If none of the above conditions are met, the email is likely not a spam trap
    return False

def check_email_activity(email):
    # Get the domain from the email address
    domain = email.split('@')[-1]

    # Check MX records for the domain
    mx_records = check_mx_records(domain)

    if mx_records:
        return True  # MX records found, email is considered active
    else:
        return False  # No MX records found, email is considered inactive

def clean_email_list(email_list):
    cleaned_list = []
    invalid_count = 0
    inactive_count = 0
    spam_trap_count = 0

    for email in email_list:
        if is_valid_email(email):
            if check_spam_traps(email):
                spam_trap_count += 1
            elif check_email_activity(email):
                cleaned_list.append(email)
            else:
                inactive_count += 1
        else:
            invalid_count += 1

    cleaned_list = remove_duplicates(cleaned_list)
    
    return cleaned_list, len(cleaned_list), invalid_count, inactive_count, spam_trap_count

def read_emails_from_csv(file_path):
    emails = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Check if the row is not empty
                emails.extend(row)
    return emails

# Adjust the file path to point to the correct location
file_name = "emails.csv"
file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Email Cleaner', file_name)

if os.path.exists(file_path):
    emails = read_emails_from_csv(file_path)
    cleaned_emails, cleaned_count, invalid_count, inactive_count, spam_trap_count = clean_email_list(emails)
    print("Cleaned Email List:")
    for email in cleaned_emails:
        print(email)
    print(f"\nTotal cleaned emails: {cleaned_count}")
    print(f"Invalid emails: {invalid_count}")
    print(f"Inactive emails: {inactive_count}")
    print(f"Spam trap emails: {spam_trap_count}")
else:
    print(f"File '{file_name}' not found in the specified directory.")
