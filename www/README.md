# django-rrweb.com


## Notes


### Load Database from Production

```
ssh dokku@django-rrweb.com postgres:export postgres144-django-rrweb | pv > dump.export
/opt/local/bin/pg_restore -cd django-rrweb dump.export
```

- Change password for users to "password".


### Reset Database

```
ssh dokku@django-rrweb.com ps:stop django-rrweb
ssh dokku@django-rrweb.com postgres:unlink postgres144-django-rrweb django-rrweb
ssh dokku@django-rrweb.com postgres:destroy postgres144-django-rrweb
ssh dokku@django-rrweb.com postgres:create postgres144-django-rrweb -I 14.4
ssh dokku@django-rrweb.com postgres:link postgres144-django-rrweb django-rrweb
```


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


### Django Config

```
DJANGO_SECRET_KEY=$(cat /dev/urandom | env LC_ALL=C tr -dc a-zA-Z0-9 | fold -w ${1:-60} | head -n 1)
ssh dokku@django-rrweb.com config:set --no-restart django-rrweb DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ssh dokku@django-rrweb.com config:set --no-restart django-rrweb DJANGO_RRWEB_ENVIRONMENT=production
```


### Local Database Config

```
sudo su - postgres
(postgres) /opt/local/bin/createdb -O grantjenks django-rrweb
```


### Remote Git Config

```
git remote add dokku dokku@django-rrweb.com:django-rrweb
git push dokku main:main
```
