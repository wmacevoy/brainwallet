import tkinter as tk
import subprocess

# if you are still working under a Python 2 version, 
# comment out the previous line and uncomment the following line
#import Tkinter as tk

AVAILABLE_LANGUAGES = { 'english', 'spanish', 'french', 'japanese', 'chinese_traditional', 'italian', 'chinese_simplified' } 
BIT_OPTIONS = ('128', '160', '192', '224', '256')
MAX_SHARES = 10
MIN_SHARES = 2

def widget_handler(widget_type, label, parent, params={}):
    if label is not None:
        label_widget = tk.Label(parent, text=label)
        label_widget.pack()
    else:
        label_widget = None

    if widget_type == 'spinbox_value_list':
        trace_var = tk.StringVar(parent)
        if 'default' in params:
            trace_var.set(params['default'])
        final_widget = tk.Spinbox(parent, values=params['value_list'], textvariable=trace_var)

    elif widget_type == 'spinbox_range':
        trace_var = tk.StringVar(parent)
        start = 1
        end = 10
        if 'default' in params:
            trace_var.set(params['default'])
        if 'start' in params:
            start = int(params['start'])
        if 'end' in params:
            end = int(params['end'])
        final_widget = tk.Spinbox(parent, from_=start, to=end, textvariable=trace_var)

    elif widget_type == 'text_box':
        trace_var = tk.StringVar(parent)
        if 'default' in params:
            trace_var.set(params['default'])
        final_widget = tk.Entry(parent, textvariable=trace_var)

    elif widget_type == 'checkbox':
        trace_var = tk.IntVar()
        if 'default' in params:
            trace_var.set(int(params['default']))
        if 'text' in params:
            text = params['text']
        else:
            text = ''
        final_widget = tk.Checkbutton(parent, text=text, variable=trace_var)

    elif widget_type == 'combobox':
        trace_var = tk.StringVar(parent)
        if 'default' in params:
            trace_var.set(params['default'])
        final_widget = tk.OptionMenu(parent, trace_var, *params['choices'])

    elif widget_type == 'radio_button':
        if 'trace_var' in params:
            trace_var = params['trace_var']
        else:
            trace_var = tk.StringVar(parent)
        if 'default' in params:
            trace_var.set(params['default'])
        if 'button_value' in params:
            button_value = params['button_value']
        else:
            button_value = 1 
        if 'text' in params:
            text = params['text']
        else:
            text = ''
        final_widget = tk.Radiobutton(parent, text=text, variable=trace_var, value=button_value)

    elif widget_type == 'button':
        trace_var = None
        if 'text' in params:
            text = params['text']
        else:
            text = ''
        final_widget = tk.Button(parent, text=text, command=params['command'])

    else:
        raise Exception('Invalid widget type parameter')

    final_widget.pack(expand=True)

    return label_widget, trace_var, final_widget

class Brainwallet_GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Brainwallet")
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side=tk.LEFT)
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(side=tk.RIGHT)
        
        self.labels = {}
        self.trace_vars = {}
        self.widgets = {}

        self.labels['language'], self.trace_vars['language'], self.widgets['language'] = widget_handler('combobox', "Language", self.input_frame, {'choices': AVAILABLE_LANGUAGES, 'default': 'english'})
        self.labels['bits'], self.trace_vars['bits'], self.widgets['bits'] = widget_handler('spinbox_value_list', 'Bits', self.input_frame, {'value_list': BIT_OPTIONS, 'default':'128'})
        self.labels['minimum'], self.trace_vars['minimum'], self.widgets['minimum'] = widget_handler('spinbox_range', 'Minimum', self.input_frame, {'start': MIN_SHARES})
        self.labels['shares'], self.trace_vars['shares'], self.widgets['shares'] = widget_handler('spinbox_range', 'Shares', self.input_frame, {'start': MIN_SHARES + 2, 'end': MAX_SHARES})
        self.labels['secret'], self.trace_vars['secret'], self.widgets['secret'] = widget_handler('text_box', 'Secret', self.input_frame)

        self.key_frame = tk.Frame(self.input_frame)
        self.key_frame.pack()

        self.labels['keys'] = {}
        self.trace_vars['keys'] = {}
        self.widgets['keys'] = {}
        for i in range(0, int(self.widgets['shares'].get())):
            self.labels['keys'][i], self.trace_vars['keys'][i], self.widgets['keys'][i] = widget_handler('text_box', 'Key' + str(i + 1), self.key_frame)

        self.labels['randomize'], self.trace_vars['randomize'], self.widgets['randomize'] = widget_handler('checkbox', "Randomize", self.input_frame, {'default': '1'})
        self.labels['dump'], self.trace_vars['dump'], self.widgets['dump'] = widget_handler('checkbox', "Dump", self.input_frame, {'default': '1'})
        self.labels['master'], self.trace_vars['master'], self.widgets['master'] = widget_handler('checkbox', "Master", self.input_frame, {'default': '0'})
        self.labels['seed'], self.trace_vars['seed'], self.widgets['seed'] = widget_handler('checkbox', "Seed", self.input_frame, {'default': '0'})

        self.labels['generate'], self.trace_vars['generate'], self.widgets['generate'] = widget_handler('radio_button', None, self.input_frame, {'button_value': 'generate', 'text': "Generate", 'default': 'generate'})
        self.labels['recover'], self.trace_vars['recover'], self.widgets['recover'] = widget_handler('radio_button', None, self.input_frame, {'trace_var': self.trace_vars['generate'], 'button_value': 'recover', 'text': "Recover"})
        self.labels['submit'], self.trace_vars['submit'], self.widgets['submit'] = widget_handler('button', None, self.input_frame, {'text': "Submit", 'command': self.submit_callback})
        self.read_only_output = tk.Text(self.output_frame, width=75)
        self.read_only_output.bind("<Key>", lambda e: "break")
        self.read_only_output.config(font=('DejaVu Sans', 12))
        self.read_only_output.pack(side=tk.RIGHT)

        self.trace_vars['bits'].trace('w', self.bits_callback)
        self.trace_vars['minimum'].trace('w', self.minimum_callback)
        self.trace_vars['shares'].trace('w', self.shares_callback)
        self.trace_vars['generate'].trace('w', self.generate_callback)
        self.root.mainloop()

    def bits_callback(self, *args):
        if self.trace_vars['bits'].get() not in BIT_OPTIONS: 
            self.trace_vars['bits'].set('128')

    def minimum_callback(self, *args):
        minimum = self.widgets['minimum']
        shares = self.widgets['shares']
        min_int = int(minimum.get())
        shares_int = int(shares.get())
        if min_int > shares_int:
            minimum.delete(0, "end")
            minimum.insert(0, shares_int)
        if min_int < MIN_SHARES:
            minimum.delete(0, "end")
            minimum.insert(0, MIN_SHARES)

    def shares_callback(self, *args):
        shares = self.widgets['shares']
        keys = self.widgets['keys']
        key_labels = self.labels['keys']
        key_trace_vars = self.trace_vars['keys']

        if int(shares.get()) > MAX_SHARES:
            shares.delete(0, "end")
            shares.insert(0, MAX_SHARES)

        shares_int = int(shares.get())
        if len(keys) > shares_int:
            for i in range(shares_int, len(keys)):
                keys[i].pack_forget()
                key_labels[i].pack_forget()
                keys.pop(i)
                key_labels.pop(i)
        elif len(keys) < shares_int:
            for i in range(len(keys), shares_int):
                key_labels[i], key_trace_vars[i], keys[i] = widget_handler('text_box', "Key" + str(i + 1), self.key_frame)

    def generate_callback(self, *args):
        generate_trace = self.trace_vars['generate']

        if generate_trace.get() == "generate":
            self.widgets['randomize'].config(state=tk.NORMAL)
            self.widgets['dump'].config(state=tk.NORMAL)
            self.widgets['master'].config(state=tk.NORMAL)
            self.widgets['seed'].config(state=tk.NORMAL)

        elif generate_trace.get() == "recover":
            self.widgets['randomize'].config(state=tk.DISABLED)
            self.widgets['dump'].config(state=tk.DISABLED)
            self.widgets['master'].config(state=tk.DISABLED)
            self.widgets['seed'].config(state=tk.DISABLED)

    def submit_callback(self, *args):
        arg_list = ['python', 'brainwallet.py', '--bits=%s' % self.trace_vars['bits'].get(), '--language=%s' % self.trace_vars['language'].get(),
                '--minimum=%s' % self.trace_vars['minimum'].get(), '--shares=%s' % self.trace_vars['shares'].get()]
        if self.trace_vars['secret'].get() != '':
            arg_list.append('--secret=%s' % self.trace_vars['secret'].get())
        for i in range(int(self.trace_vars['shares'].get())):
            if self.trace_vars['keys'][i].get() != '':
                arg_list.append('--key%d=%s' % (i + 1, self.trace_vars['keys'][i].get()))
        if self.trace_vars['randomize'].get() == 1:
            arg_list.append('--randomize')
        if self.trace_vars['dump'].get() == 1:
            arg_list.append('--dump')
        if self.trace_vars['master'].get() == 1:
            arg_list.append('--master')
        if self.trace_vars['seed'].get() == 1:
            arg_list.append('--seed')
        output = subprocess.check_output(arg_list).decode('utf-8')
        if self.read_only_output.get(1.0) != '':
            self.read_only_output.delete(1.0, "end")
        self.read_only_output.insert(1.0, output)

if __name__ == '__main__':    
    UI = Brainwallet_GUI()
