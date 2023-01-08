from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug = True) # app.run will start up the flask webserver 
                          # When Debug == True, anychanges made to the website will cause the webserver to restart which means I can write code and refresh the webpage to check for changes without restarting the server. 
                          # This value should always be 'False' once the website will be deployed to the Quechen Tribe.
