This repository is the graphic partt in python of the repository Server.

In this repository, you have an MVP architecture. 
The Model is the same Weapon we have in the repository Server.
The View is the administrator of the rendering and the windows update. He send's also requests to the Presenter.
The Presenter manages the requests and send's them to the server and return response to the View. he is a REST API.

When you start the project, the main window renders with buttons and text fields.
When you click on a button that ask something to the server, the view share the information to the presenter. 
If this is a button to navigate between the windows, the view make's it without presenter.
The presenter send the request to the server C# with the good URL.
The presenter wait the response of the server. 
If the response is valid, the presenter notify the view of a modification.
Then, the view update's the window.

You can use Visual Studio Code for this code.

You have to modify, every time you see {port_number} in the URL's in the Presenter, by the port number you will see when
you run your server C# in the URL of Swagger. 
For example, if you see http://localhost:3000/swagger/index.html, so you will modify all the {port_number} in Presenter by 3000.
