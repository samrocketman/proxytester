#! /bin/sh
python ./check-status-proxy-address.py
echo "Updating the refined list"
rm proxylist.txt
mv new_list.txt proxylist.txt
echo "Done."