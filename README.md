# ovh-mail-redirection-manager

## What is this ?
This project is a python client to manage email redirection from OVH

## Prerequisites

You have to create a .env file with OVH informations :
```
OVH_END_POINT=your_endpoint
OVH_APPLICATION_KEY=your_application_key
OVH_APPLICATION_SECRET=your_application_secret
OVH_CONSUMER_KEY=your_consumer_key

DOMAIN=yourdomain.com
```

To create your APIKeys, follow the link : https://eu.api.ovh.com/createToken/

You have to give the rights below :
  * GET ``/email/domain/*/redirection``
  * POST ``/email/domain/*/redirection``
  * GET ``/email/domain/*/redirection/*``
  * DELETE ``/email/domain/*/redirection/*``

Before first use, install dependencies
```
    pip install -r requirements.yml
```

## Commands

To list current redirection
```
    python mail-redirection.py list
```
You can filter the list by source and destination
```
    python mail-redirection.py list --from <mail source> --to <mail destination>
```

To add a new redirection
```
    python mail-redirection.py add --from <mail source>  --to <mail destination>
```

To remove a redirection
```
    python mail-redirection.py remove --from <mail source>
```

## Author

Julien Vinet <contact@julienvinet.dev>

## License

GNU GENERAL PUBLIC LICENSE Version 3