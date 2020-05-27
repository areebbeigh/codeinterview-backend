from django import forms


class CodeEditor(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(CodeEditor, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'code-editor'

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.54.0/codemirror.min.css',
                # 'https://codemirror.net/theme/ayu-dark.css',
            )
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.54.0/codemirror.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.54.0/addon/edit/closebrackets.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.54.0/addon/edit/matchbrackets.min.js',
            '/static/codemirror-init.js',
        )
