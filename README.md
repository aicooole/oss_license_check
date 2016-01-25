# oss_license_check
This is a test script written in Python.  
Reading composer.lock, parse which package(oss) the app using,  
and check license file uploaded on Github.  
Finally, this script make authors file.

## How to use.
```
$ oss_license_check.py -O {OUTPUT_AUTHOR_FILE} --dir {PATH_TO_APP_DIR}
```
-O : Authors file name. If you don't appoint, "AUTHORS" is a default.  
--dir : Directory where "composer.lock" is put.  

## AUTHORS example
```
----
dnoegel/php-xdg-base-dir    0.1

MIT License

Copyright (c) 2014 Daniel Nögel

https://raw.githubusercontent.com/dnoegel/php-xdg-base-dir/master/LICENSE

----
doctrine/inflector  v1.1.0

MIT License

Copyright (c) 2006-2015 Doctrine Project

https://raw.githubusercontent.com/doctrine/inflector/master/LICENSE

----
...
```
