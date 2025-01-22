try:
    from . import create_app
except ImportError:
    raise ImportError("Unable to import create_app from __init__.py")


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
