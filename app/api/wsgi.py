try:
    from app.api import create_app
except ImportError:
    import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
