# DevOops

DevOops is a monitoring tool that allows you monitor your ip-address, ports and processes.

### Prerequisites

Python version 3.8

```
pip install psutil
```

```
pip install sendgrid
```

### Installing

First, clone the project (Installing section).

```
git clone https://github.com/OmarShaker97/DevOops.git
```

Afterwards, change the values inside the json file named sendgrid

• SENDGRID_API_KEY is the API key that allows you to send emails.
• sender should contain the email of the sender
• recipients should contain the email of the recipients

Then change the values inside the json file named config

• retryAttempts is the number of times that the code will attempt to ping a certain server or process before sending an email.
• waitTime is the number of seconds that the program will wait before attempting to ping a certain server or process again.
• trade-aggregator-servers contain the ip-addresses and ports of the trade aggregator servers.
• trade-aggregator-process contain the process names of the trade aggregator processes.
• order-proxy-service contain the process names of the order proxy service.
• trade-aggregator-proxy contain the ip-addresses, ports and process names of the trade aggregator proxy.

Finally, run this command to run the project

```
python DevOops.py
```

## Built With

- [Python 3.8](https://www.python.org/downloads/release/python-380/) - Programming language used
- [SendGrid](https://github.com/sendgrid/sendgrid-python) - SendGrid Emailing Service

## Authors

- **Omar Shaker** - _Initial work_ - [OmarShaker](https://github.com/OmarShaker97)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
