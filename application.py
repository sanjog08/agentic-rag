from app import app, routes


app.debug = True

routes.add_resources()

app.run()