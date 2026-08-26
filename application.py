from app import app, routes


app.debug = True

routes.add_resources()

if __name__ == '__main__':
    app.run()