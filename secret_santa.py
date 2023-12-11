import csv
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_participants(file_path):
    participants = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader, None)
        for row in reader:
            name, email = row
            if email in participants:
                participants[email].append(name)
            else:
                participants[email] = [name]
    return participants

def secret_santa_pairing(participants):
    all_names = [name for names in participants.values() for name in names]
    random.shuffle(all_names)

    pairings = {}
    remaining_recipients = all_names.copy()

    for household_names in participants.values():
        for giver in household_names:
            # Ensure that the recipient is not in the same household
            possible_recipients = [name for name in remaining_recipients if name not in household_names]
            
            if not possible_recipients:
                raise ValueError("Unable to create Secret Santa pairings. Please check your input data.")
            
            recipient = random.choice(possible_recipients)
            pairings[giver] = recipient
            remaining_recipients.remove(recipient)

    return pairings

def get_random_holiday_joke():
    holiday_jokes = [
        "Why did Santa go to music school? Because he wanted to improve his wrapping skills!",
        "What do you get if you cross a snowman and a dog? Frostbite!",
        "Why was the snowman looking through the carrots? He was picking his nose!",
        "What do you call an elf who sings? A wrapper!",
        "Why was the math book sad during the holidays? Because it had too many problems!"
    ]
    return random.choice(holiday_jokes)

def send_email(to_email, subject, body):
    # Replace these with your own email and SMTP server information
    smtp_server = 'your_smtp_server'
    smtp_port = 587
    smtp_username = 'your_email@gmail.com'
    smtp_password = 'your_email_password'

    from_email = smtp_username

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    # Get a random holiday joke
    holiday_joke = get_random_holiday_joke()

    body_with_joke = f"{body}\n\nHere's a holiday joke for you:\n\n{holiday_joke}\n\nBest regards,\nYour Secret Santa Organizer"

    message.attach(MIMEText(body_with_joke, 'plain'))

    return to_email, message.as_string()

def main():
    file_path = 'names_email.csv'  # Update with your file path
    participants = load_participants(file_path)
    
    try:
        pairings = secret_santa_pairing(participants)
        email_contents = []

        for giver, receiver in pairings.items():
            print(f"{giver} is the Secret Santa for {receiver}")
            # Customize the email subject and body
            subject = 'Secret Santa Pairing'
            body = f"Dear {giver},\n\nYou are the Secret Santa for {receiver}! Spread the holiday cheer."

            # Get email content without sending the email
            to_email, email_content = send_email(giver, subject, body)
            email_contents.append((to_email, email_content))
    except ValueError as e:
        print(e)

    # At this point, email_contents contains tuples of (recipient_email, email_content)
    # You can choose what to do with this information (e.g., print, save to a file, etc.)
    for to_email, email_content in email_contents:
        print(f"Recipient: {to_email}\n\n{email_content}\n{'='*30}\n")

if __name__ == "__main__":
    main()
