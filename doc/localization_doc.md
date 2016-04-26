##1.descritpion:
localization.py has a simple mission ,just translate your locale file items.It includes two class,those classes are responsible for reading your locale file  and translate them.
##2.class
```python
1.LocaleProxyer #this class is responsible for provide proxy reader for different locale file
2.Locale        #this class is responsible for translating locale file items
```
##3.preparation
When you decide to use Locale,need to config your default locale in your project config file,then you need  make a localization file's directory in your project localization directory, that localization file directory is related to your localization(ex.,when you want to use english country localization,you must make a directory named by langeuage name ,like english,this name is related to your localization file in your config file),after making localization file's directory ,you can create your own localization file ,it's name is part of keys when you access localization file item,the file's content must be json format
##4.quickstart
```python
Locale().translate("message:register.email") #it represents accessing 'email' item under the 'register'  item in your localization file named by 'message',the format of message file is following:
#message.py
#"register":{"email":"32828373@gmail.com"}
```

