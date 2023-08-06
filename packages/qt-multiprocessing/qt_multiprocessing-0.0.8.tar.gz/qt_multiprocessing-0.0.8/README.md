# qt_multiprocessing

Long running process that runs along side of the Qt event loop and allows other widgets to live in the other process.

## Quick Start

```python
import os
import qt_multiprocessing

from qtpy import QtWidgets


class MyPIDLabel(QtWidgets.QLabel):
    def print_pid(self):
        text = self.text()
        print(text, 'PID:', os.getpid())
        return text


class MyPIDLabelProxy(qt_multiprocessing.WidgetProxy):
    PROXY_CLASS = MyPIDLabel
    GETTERS = ['text']


if __name__ == '__main__':
    with qt_multiprocessing.MpApplication() as app:
        print("Main PID:", os.getpid())

        # Proxy
        lbl = MyPIDLabelProxy("Hello")

        widg = QtWidgets.QDialog()
        lay = QtWidgets.QFormLayout()
        widg.setLayout(lay)

        # Form
        inp = QtWidgets.QLineEdit()
        btn = QtWidgets.QPushButton('Set Text')
        lay.addRow(inp, btn)

        def set_text():
            text = inp.text()
            lbl.setText(inp.text())

            # Try to somewhat prove that the label is in a different process.
            # `print_pid` Not exposed (will call in other process. Result will be None)
            print('Set Label text', text + '. Label text in this process', lbl.print_pid())

            # `print_pid` will run in a separate process and print the pid.

        btn.clicked.connect(set_text)

        widg.show()
```

Below is an example for if you want to manually create widgets in a different process without the proxy.

```python
import os
import qt_multiprocessing

from qtpy import QtWidgets


class MyPIDLabel(QtWidgets.QLabel):
    def print_pid(self):
        text = self.text()
        print(text, 'PID:', os.getpid())
        return text


def create_process_widgets():
    lbl = MyPIDLabel('Hello')
    lbl.show()
    return {'label': lbl}


if __name__ == '__main__':
    with qt_multiprocessing.MpApplication(initialize_process=create_process_widgets) as app:
        print("Main PID:", os.getpid())

        widg = QtWidgets.QDialog()
        lay = QtWidgets.QFormLayout()
        widg.setLayout(lay)

        # Form
        inp = QtWidgets.QLineEdit()
        btn = QtWidgets.QPushButton('Set Text')
        lay.addRow(inp, btn)

        def set_text():
            text = inp.text()
            app.add_var_event('label', 'setText', text)

            # The label does not exist in this process at all. Can only access by string names
            print('Set Label text', text + '.')

            # `print_pid` will run in a separate process and print the pid.
            app.add_var_event('label', 'print_pid')

        btn.clicked.connect(set_text)

        widg.show()
```

## How it works

This library works by creating an event loop in a separate process while the Qt application is running in the main 
process. This library is built off of the mp_event_loop library which creates a long running process where events are
thrown on a queue and executed in a separate process. The other process that is created also runs it's own Qt 
application while executing events in a timer.

This library has the ability to:
  * dynamic creation of widgets in a separate process
  * Run methods of widgets in a separate process through variable names
  * Proxy widgets
  

## Manual Example

This example shows how everything comes together manually

```python
import os
import qt_multiprocessing

from qtpy import QtWidgets


class MyPIDLabel(QtWidgets.QLabel):
    def print_pid(self):
        text = self.text()
        print(text, 'PID:', os.getpid())
        return text


def create_process_widgets():
    lbl = MyPIDLabel('Hello')
    lbl.show()
    return {'label': lbl}


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    mp_loop = qt_multiprocessing.AppEventLoop(initialize_process=create_process_widgets)
    print("Main PID:", os.getpid())

    widg = QtWidgets.QDialog()
    lay = QtWidgets.QFormLayout()
    widg.setLayout(lay)

    # Form
    inp = QtWidgets.QLineEdit()
    btn = QtWidgets.QPushButton('Set Text')
    lay.addRow(inp, btn)

    def set_text():
        text = inp.text()
        mp_loop.add_var_event('label', 'setText', text)

        # The label does not exist in this process at all. Can only access by string names
        print('Set Label text', text + '.')

        # `print_pid` will run in a separate process and print the pid.
        mp_loop.add_var_event('label', 'print_pid')

    btn.clicked.connect(set_text)

    widg.show()

    # Run the multiprocessing event loop
    mp_loop.start()

    # Run the application event loop
    app.exec_()

    # Quit the multiprocessing event loop when the app closes
    mp_loop.close()
```
