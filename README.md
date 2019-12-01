# digital_photo_frame
Instructions &amp; Code on how I got my custom digital photo frame up and running

Blog Post for the project can be found [here](http://khrishan.co.uk/blog/post/digital_photo_frame)

## Instructions for Docker

1. _Optional_ (If you want to build + run locally)
	```bash
	git clone https://github.com/khrishan/digital_photo_frame
	cd digital_photo_frame/
	docker build -t [NAME OF TAG] .
	```
1. Create your version of `config.json` (instructions [here](#) and store it somewhere locally.
1. Run this command (presuming you have docker running) : 
	```bash
	docker run -d -p 8081:8081 -v [PATH TO YOUR CONFIG.JSON]:/app/config/ [IMAGE_ID | DOCKERHUB LINK]	

	```
