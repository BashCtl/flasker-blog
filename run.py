from src import create_app, db
from src.forms.webforms import SearchForm

app = create_app()


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


if __name__ == "__main__":
    app.run(debug=True)
