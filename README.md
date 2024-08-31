# Read all my emails

I have too many unread old emails. So I made this script to do it for me instead.
You need a json file from your Google account with tokens from the Gmail API with Gmail modify scope,
and name the json file `credentials.json`.

## How to install and run:

Create a Conda environment:
```bash
conda create --name read-my-emails python=3.12
```

Activate the environment:
```bash
conda activate read-my-emails
```

Install pip in the environment:
```bash
conda install pip
```

Install required packages:
```bash
pip install -r requirements.txt
```

Run the script:
```bash
python read-emails.py
```
