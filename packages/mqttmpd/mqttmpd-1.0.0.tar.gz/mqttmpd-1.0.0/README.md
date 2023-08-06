# MQTT MPD Controller


This is a tiny, simple MPD controller over MQTT written in Python

# howto install

	sudo pip install -r requirements.txt

	sudo cp exemple.py /usr/local/bin/mqtt_mpd
	sudo vim /usr/local/bin/mqtt_mpd # ajust to your needs
	sudo cp mqtt_mpd.service /lib/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable mqtt_mpd.service
	sudo systemctl start mqtt_mpd.service
