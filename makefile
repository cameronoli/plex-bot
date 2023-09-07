update:
	docker pull linuxserver/plex:latest
	docker pull linuxserver/radarr
	docker pull linuxserver/sonarr
	docker pull linuxserver/bazarr
	docker pull linuxserver/overseerr
	docker pull linuxserver/tautulli
	docker pull linuxserver/jackett
	docker pull linuxserver/sabnzbd
	docker pull jlesage/nginx-proxy-manager
	docker pull linuxserver/qbittorrent:latest

stack:
	docker stack rm prod
	docker container prune
	docker stack deploy -c docker-compose.yml prod
	docker image prune