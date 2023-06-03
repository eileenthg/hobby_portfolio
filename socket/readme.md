# python socket

Some python files to establish pinging between two computers in a single lan network. 
This was a prototype in an attempt to implement multiplayer capabilities between two computers for [pong](https://github.com/eileenthg/hobby_portfolio/tree/main/ping%20pong%20backup), but nothing much came out of it.
Felt like the approach was wrong.

## Echo
How to run:
1. Download echoclient.py for the computer that will be sending out pings.
2. Download echoserver.py for the computer that will be receiving pings.
3. Configure the ip address and ports of echoclient.py and echoserver.py
4. Run echoserver.py in terminal. Ensure it is waiting for a message.
5. Run echoclient.py in terminal. Send a message.
6. The message will appear on echoserver.py's terminal. A reply should also appear on echoclient.py's terminal.

Note: A single computer can run both echoclient.py and echoserver.py at the same time. They just have to be run in separate instances.

## Multi-echo
How to run:
1. Download echoclient.py for every computer that will be sending out pings.
2. Download echoserver.py for the computer that will be receiving pings.
3. Configure the ip address and ports of echoclient.py and echoserver.py
4. Run echoserver.py in terminal. Ensure it is waiting for a message.
5. Run echoclient.py in terminal. Send a message.
6. The message will appear on echoserver.py's terminal. A reply should also appear on echoclient.py's terminal.

Multi-echo will be able to handle messages from multiple clients, even if they are sent simultaneously.
