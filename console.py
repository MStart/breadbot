#!/usr/bin/env python3
import core

while True:
    command = input('> ')
    if command == 'q':
        break
    if command == '':
        continue
    print(core.bot.chat().response(command, False))
