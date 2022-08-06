# django-rrweb.com


## Setup

1. Buy domain on domains.google.com
2. Configure DNS A records for subdomains '' and 'www' -> 35.235.126.200
3. Configure email forwarding for webmaster@ and grant@


### App Setup

```
ssh dokku@django-rrweb.com apps:create django-rrweb
```


### Domain Setup

```
ssh dokku@django-rrweb.com domains:add django-rrweb django-rrweb.com
ssh dokku@django-rrweb.com domains:add django-rrweb www.django-rrweb.com
ssh dokku@django-rrweb.com redirect:set django-rrweb www.django-rrweb.com django-rrweb.com
```


### Database Config

```
ssh dokku@django-rrweb.com postgres:create postgres144-django-rrweb -I 14.4
ssh dokku@django-rrweb.com postgres:link postgres144-django-rrweb django-rrweb
```


### SSL Config

```
ssh dokku@django-rrweb.com config:set --no-restart django-rrweb DOKKU_LETSENCRYPT_EMAIL=webmaster@django-rrweb.com
ssh dokku@django-rrweb.com letsencrypt:enable django-rrweb
```
