cd /Users/jizheng/Documents/Work/Programming/Django/djcode/weixin
git add *
git commit -m "commit by shell script"
git push origin master
ssh james@1stloop.com
expect james@1stserver
cd ~/codes/sandbox/weixin
git pull origin master
exit
