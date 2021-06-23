#!flask/bin/python

from app import create_app

app = create_app()
           
if __name__ == "__main__":
	print("Running main with debug mode")
	app.run(debug=True)
            
#if running on heroku these 3 lines shouldnt be running- delete them