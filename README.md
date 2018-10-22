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
