# igrepper - Interactive curses-based grepping tool

## Usage

__Pipe input text:__

    dmesg | i

__Read input from file:__

    i /path/to/file

__Commands__:

    ctrl-j: Select next match
    ctrl-k: Select previous match
    ctrl-y: Copy selected match to clipboard
    ctrl-g: Copy grep command to clipboard
    ctrl-n: New subsearch
    ctrl-p: Cancel subsearch
    ctrl-i: Toggle case sensitivity
    Up/Down/PageUp/PageDown: scroll

Recommended bash alias:

    alias i='igrepper'
    iman() { man "$1" | igrepper -c 4}




