systemctl stop mintbooking.service
cp /var/jenkins_home/workspace/sfia1/script/mintbooking.service /etc/systemd/system
systemctl daemon-reload
systemctl enable mintbooking.service
systemctl start mintbooking.service