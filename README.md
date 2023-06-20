# Install dependencies

On terminal:

`pip install -r requirements.txt`

Arguments for website update: run main.py with the `--help` argument (or `-h`) for more information.

Download the chrome driver from:

https://chromedriver.chromium.org/downloads

# Enviroment variables

In the .env file:

```
API_BASE_URL=<API URL>
AUTH_TOKEN=<API AUTH TOKEN>
READM_EMAIL=<THE EMAIL TO LOGIN>
READM_PASSWORD="PASSWORD TO LOGIN"
```

# Execution logs

Execution logs are stored in `exec_logs.log`.

# Install updater as a Linux Service

To install the updater as a Linux service:

```
chmod +x ./install.sh

./install.sh
```

The service can be controlled with the following commands:

### To start

```
sudo systemctl start mangahub.service
```

### To restart

```
sudo systemctl restart mangahub.service
```

### To stop

```
sudo systemctl stop mangahub.service
```

To uninstall:

```
chmod +x ./uninstall.sh

./uninstall.sh
```
