

def readCsvAsString(filePath, sep=","):
    """Leggi un file csv e crea un dataframe associato.
    utile quando il file csv non ha un numero di colonne 
    fisse e questo crea problemi con read_csv di pandas

    Args:
        filePath (_type_): _description_
    """        
    import pandas as pd
    # 1. Leggi il file CSV come file di testo
    with open(filePath, 'r') as file:
        lines = file.readlines()

    # 2. Dividi ogni riga sui `;`
    lines = [line.strip().split(sep) for line in lines]

    # 3. Trova il numero massimo di colonne
    max_columns = max(len(line) for line in lines)

    # 4. Crea un DataFrame vuoto con il numero massimo di colonne
    df = pd.DataFrame(columns=range(max_columns))

    # 5. Riempi il DataFrame con le righe del file CSV
    for index, line in enumerate(lines):
        df.loc[index] = pd.Series(line)

    # 6. Se vuoi togliere i NaN e mettere valori stringa vuoti
    df = df.fillna("")

    print(df)
    return df




import smtplib
from email.mime.text import MIMEText
def send_email(subject, message, to_email):
    """invia email con gmail

    Important: To create an app password, you need 2-Step Verification on your Google Account.

    If you use 2-Step-Verification and get a "password incorrect" error when you sign in, you can try to use an app password.

    Go to your Google Account.
    Select Security.
    Under "Signing in to Google," select 2-Step Verification.
    At the bottom of the page, select App passwords.
    Enter a name that helps you remember where you’ll use the app password.
    Select Generate.
    To enter the app password, follow the instructions on your screen. The app password is the 16-character code that generates on your device.
    Select Done.
    If you’ve set up 2-Step Verification but can’t find the option to add an app password, it might be because:

    Your Google Account has 2-Step Verification set up only for security keys.
    You’re logged into a work, school, or another organization account.
    Your Google Account has Advanced Protection.

    Args:
        subject (_type_): _description_
        message (_type_): _description_
        to_email (_type_): _description_
    """    
    from_email = "project.vpp@gmail.com"
    password = "qedq awim kmsp nccx"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

# send_email("Test Subject", "This is the body of the email.", "castaldini.gianmaria@gmail.com")


