# deb-check-mirror
Check package mirror origin for Debian OS

# command
ostree admin unlock

wget https://raw.githubusercontent.com/ChenQi1989/deb-check-mirror/main/deb-check.py

chmod +x deb-check.py

./deb-check.py | tee list
