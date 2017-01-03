Overview
===
Integrates dad's awesome excel estimation software with the Google API Contacts provider so he can edit contacts in one place and reference them from his software. The idea with this script is as follows; We'll install on your windows machine python and related tools to run this script. We'll create a scheduled task within windows to run this script on a periodic basis, say every hour. The script will output a csv file to a configured location and excel can read from this file to source in its contacts.

Setup
===
The following setup instructions are a one-time process. The objective is to get a `refresh_token` that we'll provide as a configuration to the python script for pulling down the contacts via the API.

#### Enable API Access
We'll need to enable API access to contacts. We'll do this together, my setup was a little different since I enabled my account to play with Google Cloud Engine and so API access was already there.

#### Configure Oauth
Once API access is configured, you'll need to setup an application which gets you a `client_id` and `client_secret`. It'll need to be a web-based application in which you can specify a `redirect_url` from which Google will redirect to containing the authorization code

#### Retrieve authorization code
Place the following URL in your browser replacing the actual `client_id` and `redirect_url` setup from the previous step:
    
    https://accounts.google.com/o/oauth2/v2/auth?client_id=<client_id>&redirect_uri=<redirect_url>&scope=https://www.google.com/m8/feeds/&access_type=offline&response_type=code
    
This will redirect you to a "broken" webpage but it'll contain a `code` query parameter that holds an authorization code, copy this somewhere safe.

#### Retrieve `refresh_token`
We'll then take the authorization code and use it to retrieve the `refresh_token` with the following call:

    curl -v -XPOST https://www.googleapis.com/oauth2/v4/token? -d code=<authorization code> -d redirect_uri=<redirect url> -d client_id=<client_id> -d client_secret=<client_secret> -d grant_type=authorization_code

The authorization code and redirect url must be URL encoded. The results of this call will look like this (example):

    {    
        "access_token": "ya29.Ci_FAxKMm8biL1_bXT55AGIiL3Yo0qtMt41bX7mk3-V52ssjo8", 
        "token_type": "Bearer", 
        "expires_in": 3600, 
        "refresh_token": "1/23lCd-ugPkk0g5k2jvBUHmVmedHzT6MpJnuN4Bmixuxfsks9fms"
    }

The `refresh_token` is what we want. Copy/paste this into the `secrets.yml` file needed by the script.

Script Configuration
====
The script has two configuration files, `config.yml` and `secrets.yml`. The `secrets.yml` is not checked into source code as it will contain the `client_secret` and `refresh_token` that were obtained from the previous steps.

After cloning the repo, simply create a `secrets.yml` file within the project folder with the following, replacing with real values:

    refresh_token: refreshtoken
    client_secret: clientsecret
    
Lastly, in the `config.yml` file set the `csv_location` to an absolute path pointing to a location on your machine to have the script write the csv file to.

Setting up python
====
We'll need to install a 2.x version of python on your machine along with `pip` and `virtualenv`. Then we'll simply clone the repo, run the following:

    virtualenv env
    env/bin/pip install -r requirements.txt