# https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver/41220267

cp ./chromedriver ./chromedriver.bak
perl -pi -e 's/cdc_/ctg_/g' ./chromedriver
