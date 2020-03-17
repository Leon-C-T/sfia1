sudo systemctl stop mintbooking.service
sudo cp "/var/lib/jenkins/workspace/sfia1/script/mintbooking.service" /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable mintbooking.service
sudo systemctl start mintbooking.service