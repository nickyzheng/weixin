cd /Users/jizheng/Documents/Work/Programming/Django/djcode/weixin
git add *
git commit -m "commit by shell script"
git push origin master
ssh james@1stloop.com 'bash -s' < gitpull.sh
