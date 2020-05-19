# Toontown Offline Docker Image
This Image will allow you to host a Toontown Offline Mini-Server inside a Docker container.

## How to use this image:

Example run commmand on a current working directory (recommanded):

`$ docker run --name=ttoff-server -v$PWD:/$PWD -w/$PWD -u $(id -u):$(id -g) --rm --net=host -dt littletooncat/ttoffline:latest`

NOTE: The image always checks for updates before starting the server, so whenever a new update releases, simply just restart the container to apply the update.

## Configuration:
 After the game's been downloaded and ran for the first time, a file named `config/server.json` is created.  Modify the file to fit your needs.

 NOTE: You need to restart the container for the changes to take effect.
