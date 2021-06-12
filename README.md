# ebk_coronalogin
system to store corona related attendence-lists encrypted
implemented as a cli application


## Install

```
git clone https://github.com/Eigenbaukombinat/ebk_coronalogin.git
cd ebk_coronalogin
make
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

## Content

You have to configure the content you want to use in another python
module.

```
cp content_config.py.example content_config.py
<editor> content_config.py
```

The provided example shows how to import your content.


## Run

```
bin/python login.py
```

## Make it secure

You might want to take measures that users are not able to change the code or modify/access the created encrypted files too easily.


