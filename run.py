from app import create_app
my_app = create_app()
my_app.run(host='0.0.0.0', port=80, debug=True)