from apps import create_app

app = create_app()
# source ~/.bash_profile

if __name__ == '__main__':
    app.run(port=4912)