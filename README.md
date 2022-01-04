<div>
<h1>Docker</h1>
<div>
<p> Build a docker image from Dockerfile: sudo docker build -t flask-app:1.0 . </p>
<p> Identify image id: sudo docker images </p>
<p> Take the "IMAGE ID" value for the flask-app with TAG 1.0 </p>
<p> Start the container in detached mode: sudo docker run -d -p 5000:5000 "IMAGE ID" </p>
<h4>Start/Stop Docker Container:</h4>
<p>Get the "CONTAINER ID" value for Image with "IMAGE ID"
<p>Stop container: sudo docker stop "CONTAINER ID"</p>
<p>Start container: sudo docker start "CONTAINER ID"</p>
</div>
<div>

<div>
<h1>
Swaggers
</h1>
<div>
<p> Friend Api Swagger url: <b> http://localhost:5000/friends/ </b> </p>
<p> Users Api Swagger url: <b> http://localhost:5000/users/ </b> </p>
</div>
</div>

<div>
<h1>Api Usage</h1>
<div>

<div>
<h3> Auth Routes </h3>
<div>
<p>This routes are used to Log In/Log Out users from api</p>
<p>Log In url: <b>POST request: localhost:5000/users/auth/ </b>. You can use this valid data in body in order 
to Log In {"email": "mihai@yahoo.com","password": "mihai"}. At Success you will receive the user's data</p>
<p>Log Out url: <b>Delete request: localhost:5000/users/auth/ </b>. You should be logged in 
to access this functionality.</p>
</div>
</div>

<br> 

<div>
<h3>Users Routes</h3>
<div>
<p>Create user: <b>POST request: localhost:5000/users/users/ . </b> Example of valid data in body: {
"email": "postman@yahoo.com","password": "postman","first_name": "postman","last_name": "postman"}. The email should be
unique.</p>
<p>List all users: <b>GET request: localhost:5000/users/users/ .</b></p>
<p>The users created with the db are in "build_database.py" file, if you want to access their credentials for auth.</p>
</div>
</div>

<br>

<div>
<h3>Friends Routes</h3>
<div>
<p>In order to work this routes you should be logged in.In this section we will refer to the logged in user.</p>
<p>Get user's friends: <b>GET request: POST request: localhost:5000/users/users/ .</b></p>
<p>Add new friend for user: <b>POST request: POST request: localhost:5000/users/users/ .</b>Example of valid data 
in body: {"first_name": "user1","last_name": "user1","number": "0234567890"}. The phone number should contain 10 digits
and start with 0</p>
<p>Get a specified friend: <b> GET request: localhost:5000/friends/friend/friend_id/ .</b></p>
<p>Update a specified friend: <b> PUT request: localhost:5000/friends/friend/friend_id/ .</b>Example of valid data in 
body {"first_name": "mihai3","last_name": "user3","number": "0123456789"}</p>
<p>Delete a specified friend: <b> DELETE request: localhost:5000/friends/friend/friend_id/ .</b></p>
</div>
</div>

<div>
<h1>Testing</h1>
<div>
Run the following commands:
<p>sudo docker ps</p>
<p>Get the "CONTAINER ID" value for Image with "IMAGE ID"(from docker section)
<p>sudo docker exec -it "CONTAINER ID" bash</p>
<h5>Now you can run the testing files with following command:</h5>
<p>PYTHONPATH=. pytest tests</p>
<p>If you want to close the interactive terminal run: exit </p>
</div>
</div>