#!/usr/bin/python3

import argparse
import os
import shutil
import subprocess

HOME = os.getenv("HOME")
CS444_BASE = f"{HOME}/.cs444"

def ask_intent(string):
    answer = 'z'
    while answer not in ('y', 'n'):
        print(string + " (y/n) ?")
        answer = input().strip().lower()

    return answer == 'y'

def backup_and_write_file(fn, data):
    # backup file
    if os.path.exists(fn):
        for i in range(1000):
            # fn.bak.[number] is backup
            backup_fn = f'{fn}.bak.{i}'
            if not os.path.exists(backup_fn):
                shutil.copyfile(fn, backup_fn)
                break
    with open(fn, 'w') as f:
        f.write(data)

def clone():
    os.system('git config --global core.autocrlf false')
    if os.path.exists(CS444_BASE):
        os.system(f"rm -rf {CS444_BASE}")
    try:
        r = os.system(f'git clone https://github.com/stackunderfl0w/peda {CS444_BASE}')
    except:
        print("Cloning cs444 git repository has failed!")
        return

    if r != 0:
        print("Cloning cs444 git repository has failed!")
        return

def install_gdb():
    if not ask_intent("Do you want to install peda to ~/.gdbinit"):
        return
    with open(f"{CS444_BASE}/gdbinit", 'r') as f:
        gdbinit = f.read()
    backup_and_write_file(f'{HOME}/.gdbinit', gdbinit)

def install_bash():
    if not ask_intent("Do you want to install .bashrc"):
        return

    with open(f"{CS444_BASE}/bashrc", 'r') as f:
        bashrc = f.read()
    backup_and_write_file(f'{HOME}/.bashrc', bashrc)

    if os.path.exists(f"{HOME}/.cshrc"):
        with open(f"{HOME}/.cshrc", 'r') as f:
            cshrc = f.read()
            if 'exec /bin/bash' not in cshrc:
                cshrc += "\nexec /bin/bash\n"
        backup_and_write_file(f'{HOME}/.cshrc', cshrc)

def install_vim():
    if not ask_intent("Do you want to install .vimrc and vim plugins"):
        return

    with open(f"{CS444_BASE}/vimrc", 'r') as f:
        vimrc = f.read()
    backup_and_write_file(f'{HOME}/.vimrc', vimrc)

    os.system("vim +PlugInstall +qall")

def install_tmux():
    if not ask_intent("Do you want to install cs444 custom tmux configuration"):
        return

    with open(f"{CS444_BASE}/tmux.conf", 'r') as f:
        tmux_conf = f.read()
    backup_and_write_file(f'{HOME}/.tmux.conf', tmux_conf)

def copy_qemu():
    copy_file_to_bin('qemu-system-i386')
    copy_file_to_bin('qemu-system-x86_64')
    copy_file_to_bin('mmd')
    copy_file_to_bin('mcopy')
    copy_file_to_bin('kill-qemu')
    copy_file_to_bin('kill-all-tmux')
    copy_file_to_bin('ta-help')

def copy_file_to_bin(name):
    if not os.path.exists(f"{HOME}/bin"):
        os.makedirs(f"{HOME}/bin")

    shutil.copyfile(f"{CS444_BASE}/bin/{name}", f"{HOME}/bin/{name}")
    os.system(f"chmod +x {HOME}/bin/{name}")

def main():
    clone()
    copy_qemu()
    print('')
    print('')
    install_gdb()
    install_tmux()
    install_bash()
    install_vim()

if __name__ == '__main__':
    main()
