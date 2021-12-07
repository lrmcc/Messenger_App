# Messenger_App
A messenger app for users to send messages and files directly to individuals or to a group. The application is built with TCP sockets using Python Standard Library modules. 

The application's server configuration is determined by on whether it is hosted locally or as web application. A closed network could launch a server instance to allow clients to connect within the network. Alternatively, a web hosting platform of some kind could be selected and configured in order to launch a web-based server instance to allow clients to connect from the internet. 

## Developer Objective
To provide a usable and customizable messaging application built in the Python language. 

## Purpose
Users can communicate with one another over a messaging application 

## Prerequisites	
Messenger_App will require Python version 3+ be installed. 
[Get Python here](https://www.python.org/).

## Local Host Installation
#### 1. Clone the repo or download and unzip the repo.

#### 2.1 To launch a server from terminal run main.py with the argument server: 
	example: python3 main.py server

#### 2.2 Alternatively, to launch a server from script file: 
	For MacOS/Linux, double-click on launch_server.command
	For Windows, double-click on launch_server.bat

#### 3.1 To launch a client from the terminal run main.py with the argument client 
	example: python3 main.py client

#### 3.2 Alternatively, to launch a client from script file: 
	For MacOS/Linux, double-click on launch_client.command
	For Windows, double-click on launch_client.bat

## Current Functionality
- User launches client in the terminal.
- User creates username for each session.
- User can broadcast messages to all clients connected to server.
- User can retrieve list of all users connected to server.
- User can direct message another user without message being broadcast.
- User can exit from program.

## Future Functionality 
- User can launch client in a browser application.
- User accounts holds user information and dictates what data is retained.
- User data is retained per user requirements set at account creation and can be changed at any time.
- User can block any other user from communicating or seeing connection status.
- User has total control of data storage and can destroy an account at any time.
- User can create a public or private group that allows members to communicate within.
- User can retrieve a list of all public groups.
- Public groups allow anyone to join.
- Private groups allow anyone that receives an invitation to join.
- Admin accounts have ability to interact with users, ban users, and shutdown servers.
- Admin accounts are created at server instantiation, after that only admin accounts can create new admin accounts.
- Server instance can save it's state as a file to allow for preservation in the case a running server instance fails.
- Server state can be loaded upon server instantiation as part of configuration.
- Some Server characteristics, such as save frequency, can be managed by Admin by updating the instance configuration.
- Some Server characteristics, such as ID and certain meta-data, cannot be changed and are unique to each instance.
- End-to-end encryption for messages.
- File Transfer.