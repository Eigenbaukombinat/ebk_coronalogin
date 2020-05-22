# ebk_coronalogin
system to store corona related attendence-lists encrypted


## Install

```
git clone https://github.com/Eigenbaukombinat/ebk_coronalogin.git
cd ebk_coronalogin
python3.8 -m venv .
bin/pip install -r requirements.txt
```

## Prepare

Import the public key you want to use into a gpg keychain.
Refer to gnupg docs how to do that.

## Configuration

You have to configure your .gnupg homedir, the path where
the files will be stored and the uid of the gpg-key to use.

```
cp config.py.example config.py
<editor> config.py
```

## Run

```
bin/python login.py
```

## Make it secure

You might want to take measures that users are not able to access or change the code too easily.


