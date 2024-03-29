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

Also store your private key securely, but in a way that you can find it in case you need it.


## Decrypt data for the Gesundheitsamt

The used script requires that you have the private key in your gpg keychain.

First, you have to checkout this code.

```
git clone https://github.com/Eigenbaukombinat/ebk_coronalogin.git
cd ebk_coronalogin
```

Copy the directory containing the data of the day you want to decrypt and the `logouts.txt` file into your checkout and call the `get_day_data.py` script from the day-directory.  

```
cp -r /storage_with_workdir/yyyy-mm-dd .
cp /storage_with_workdir/logouts.txt .
cd yyyy-mm-dd/
../get_day_data.py
```

The Script will tell you when its finished. Now import the generated csv file into your spreadsheet. When done, press "Enter" to delete the csv with decrypted data.

Repeat if you need more days. As a last step you have to manually fill in missing contact data for logins of members in your spreadsheet.
