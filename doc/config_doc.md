##1.description
config.py include all config loader,those config loader read config item 
from config file,and privode a common interface  for you to access all the config item in your config file


##2.class
> DBConfigLoader
> SessionConfigLoader
> AuthConfigLoader
> AppConfigLoader
> FileSystemConfigLoader
> QueueConfigLoader
> MailConfigLoader
> Config


##3.quick start
1.access database config 
```python
Config.database.all #access default driver all config items
Config.database.connection_name #default driver connection name
Config.database.port	#default driver port
Config.database.connection('mysql').all 
Config.database.connection('mysql',True) #the same as last line
```
2.access session config
```python
Config.session.session_dir
Config.session.expire_file
Config.session.expire
Config.session.driver('redis').host
Config.session.driver('redis').port
Config.session.driver('redis').db
Config.session.driver('redis').expire
Config.session.driver('mongo').host
Config.session.driver('mongo').port
Config.session.driver('mongo').db
Config.session.driver('mongo').expire
```
3.access authentication config
```python
Config.authentication.auth_table
Config.authentication.auth_id
Config.authentication.login_url
```
4.access app config
```python
Config.app.template_path
```
5.access file system config
```python
Config.filesystem.access_key
Config.filesystem.secret_key
Config.filesystem.driver_name
Config.filesystem.all
```
6.access queue config
```python
Config.queue.all
Config.queue.host
Config.queue.port
Config.queue.db
Config.queue.driver_name
Config.queue.driver('mysql',True)
Config.queue.driver('mysql').all
Config.queue.driver('mysql').user
Config.queue.driver('mysql').host
Config.queue.driver('mysql').port
Config.queue.driver('mysql').password
Config.queue.driver('mysql').driver_name
Config.queue.driver('mongo',True)
Config.queue.driver('mongo').all
Config.queue.driver('mongo').host
Config.queue.driver('mongo').port
Config.queue.driver('mongo').db
Config.queue.driver('mongo').driver_name
```
7.access mail config
```python
Config.mail.host
Config.mail.user
Config.mail.password
Config.mail.port
```
###updating.................
