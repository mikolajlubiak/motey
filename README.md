# Motey

## Showcase: [https://diode.zone/w/aXNYaER47MnTu8uw4LZSFW](https://diode.zone/w/aXNYaER47MnTu8uw4LZSFW)

## Discord bot setup

- Go to https://discord.com/developers/applications and create a new app
- ![Bot setup step 1](README_IMAGES/bot_setup_1.png)
- In the Bot section copy your bot token
- ![Bot setup step 2](README_IMAGES/bot_setup_2.png)
- Enable the message content intent
- ![Bot setup step 3](README_IMAGES/bot_setup_3.png)
- In the OAuth2 section copy your client id and secret
- ![Bot setup step 4](README_IMAGES/bot_setup_4.png)
- Add the redirect url, for the default .env the correct url is: http://127.0.0.1:8080/process_oauth
- ![Bot setup step 5](README_IMAGES/bot_setup_5.png)
- In the url generator enable the bot scope
- ![Bot setup step 6](README_IMAGES/bot_setup_6.png)
- Set the integration type to Guild install and enable the following permissions: Manage Webhooks, View Channels, Send Messages, Manage Messages, Attach Files
- ![Bot setup step 7](README_IMAGES/bot_setup_7.png)
- Copy the generated url and use it to add the bot to your server
- ![Bot setup step 8](README_IMAGES/bot_setup_8.png)

## Setup

* Create .env file from template:
```shell
cp .env.dist .env
```
Replace default variables with your own, note that most default values will work just fine for local testing/development environments:

* Run the script:
```shell
./setup.sh
```

## Run

### Local/Testing:

* Source the script:
```shell
source run_local.sh
```

### Production:

* Change the domain in `Caddyfile`
* Run the script:
```shell
./run_prod.sh
```
