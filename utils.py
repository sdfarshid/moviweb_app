from flask import render_template


def load_page(template_name: str, args=None):
    if args is None:
        args = {}
    return render_template(f'{template_name}.html', **args)
