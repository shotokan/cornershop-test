## cornershop-backend-test

### Running the development environment

* `make up`
* `dev up`

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`

### Hostnames for accessing the service directly

* Local: http://127.0.0.1:8000


### About building local environment with Linux systems

If you bring up the local environment in a linux system, maybe you can get some problems about users permissions when working with Docker.
So we give you a little procedure to avoid problems with users permissions structure in Linux.:

1- Delete containers

```
# or docker rm -f $(docker ps -aq) if you don't use docker beyond the test
make down
```

2- Give permissions to your system users to use Docker

```
## Where ${USER} is your current user
sudo usermod -aG docker ${USER}
```

3- Confirm current user is in docker group

```
## If you don't see docker in the list, then you possibly need to log off and log in again in your computer.
id -nG
```


4-  Get the current user id

```
## Commonly your user id number is near to 1000
id -u
```

5- Replace user id in Dockerfiles by your current user id

Edit `.docker/Dockerfile_base` and replace 1337 by your user id.

6- Rebuild the local environment 

```
make rebuild
make up
```


# Project Solution

> Hostnames for accessing the service directly
 - Local: http://127.0.0.1:8000

```bash
To avoid complexity in the front end, I limited the options 
that can be had per menu to 4 like in the example. However, the database schema could accept more options per menu.

I am using django forms and templates because it is an internal platform 
and We can start as a monolithic.
```

There are 2 users: super-admin (django superadminm) and staff.

### Superadmin access

> /menu/list/
> 
Show all the menus and their items that have been created

> /menu/create/
> 
Display a form to create a new menu and assign its items

> /menu/orders/

List all the orders of the current day tha are requested by the staff

> /menu/reminder/

Send a Slack reminder with today's menu to all chilean employees (this process needs to be asynchronous and implemented by using Celery tasks)

### Staff

> staff/orders/

List all the orders created by the session user

### No authentication required
> /account/signup/

Form to add a new staff user

> /account/login/

Form to login

> /menu/{<uuid:menu_id>}

 The slack message contains an URL to today's menu with the following pattern. this page must not require authentication of any kind, just when you need to order the user is redirect to login and be able to select the item. Other way to avoid authentication shold be to add a query param with an encryted value that allow us to find the user.

> /account/logout/
Close user sessionb


### NOTES

```
There is a share director which contains a notification module that is used to send notification via slack, the idea of this has been to create a wrapper for the slack clien so we can change it to other platform like whatsapp, or other one with few changes.

```

```
Account directory has all the logic to manage authentication and account features.

Staff directory or app has all the logic to create an order for the staff and validations that are needed to crete it.

Menu directory has all the logic to create a menu and validate it.

```

```
Every app has its own test directory.
```
## TODO

- More unit tests and integration tests to validate views and logic
- Improve design
