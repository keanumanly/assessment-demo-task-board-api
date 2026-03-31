# Set Up REDIS in LOCAL MACHINE

installing REDIS in local machine
```bash
# open terminal and type this:
install the redis-cli

# next test the redis 

redis-cli ping

# if the terminal response to PONG thats me you have already redis-server
# if you got this message: Could not connect to Redis at 127.0.0.1:6379
# then this what nexts to do:
brew services start redis

# next type this:
redis-server

# then open new tab in terminal and type again this:
redis-cli
```
just update the env base from you redis address and port and db