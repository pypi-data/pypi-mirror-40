# DiSwarm
Discord-based Swarm Protocol Library

## Usage
Main class: `Swarm`

Initialize like so:
```swarm = Swarm(discord channel id: str, discord bot token: str, swarm id: str)```

Sending message to swarm:
```swarm.send(string message)```

Getting messages from swarm:
```swarm.get_queue()```
returns a list of ```(timestamp, decoded message)``` tuples from your swarm members

### Important:
Before you end your program, call ```swarm.end()``` to cleanly end the discord bot process

## Notes
- Swarm ID: the same for all bots in your swarm, but it should be unique from any other swarm, at least on your swarm channel. To be safe, use a randomly generated string or number. Make sure every bot in your swarm has the same id, because bots with different ids cannot see eachother's messages.
- ```get_queue()``` will only return messages from your swarm, so you can have multiple swarms in the same channel.
- DiSwarm uses Fernet encryption, provided by the `cryptography` library. Install this library through `pip install cryptography`.
- Also requires `pip install discord`
