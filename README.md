# Muslim Ban
Compile and analyze public statements by D. Trump, his administration officials, associates, surrogates, and others, to prove discriminatory intent. (Including statements made during the campaign and earlier.)

# SET UP
## Firefox
```
cd ~/bin
wget https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-linux64.tar.gz 
tar -xvzf geckodriver-v0.15.0-linux64.tar.gz
rm geckodriver-v0.9.0-linux64.tar.gz
chmod +x geckodriver
```

In `~/.bashrc`
```
export PATH=$PATH:/home/<user>/bin/geckodriver
```

## Chrome
```
wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
```
