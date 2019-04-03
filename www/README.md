# data website #

## packages ##
**1. nginx**
* install nginx.
```angular2
sudo apt-get update
sudo apt-get install nginx
sudo ufw allow 'Nginx HTTP'  
sudo ufw status
```
* edit config file.
```angular2
sudo vim /etc/nginx/sites-enabled/default  ## modified line36: replace to "root /home/benchmark/benchmarking/www;" 
systemctl restart nginx
```
* need "x" permissions in every parent directory of all ".html" & ".png" files to access that file for every user.(include guest user)
command (chmod a+x xxxxxxx).
```
chmod a+x /home/benchmark/benchmarking
chmod -R a+x /home/benchmark/benchmarking/www 
```

