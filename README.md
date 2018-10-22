# song_reviewer
Application to create automatic reviews from uploaded songs


## Setting up developments environment
Song-reviewer backend is developed entirely through docker.
- First you need to have docker installed on your machine https://www.docker.com/get-started.
- Then use this magic spell to start the backend:
```docker run -p 8000:8000 -v /path/to/repository/song_reviewer/backend/:/usr/src/app/ mahtis/song_reviewer_backend```
Remember to change the path to the repository correctly! And be sure to set the path to point in the backend-folder.
- If this is your first time starting, docker will first download and pull the image from docker hub, so it will take a while.
After docker is finished building the image, the application should start running automatically.
- Navigate to localhost:8000/api/ping on your browser, and you should see "pong" on your screen. That's it, you are good to go!

Instead of pulling the image from docker hub, you can also just call ```docker build . -tag song_reviewer_backend``` in the backend folder. This is a better option if you need to add imports, because the whole image needs to be rebuild in order to install the imports. You can use the same command as above to run, just remove the 'mahtis/' part from the end, so it matches the tag argument you gave it.

Be vary that docker images can be quite large, and every time you build one, it is saved on your computer. Use ```docker images``` to see all the images you have in docker and remove all images that you don't need using ```docker rmi <IMAGE ID's separated by spaces>```
