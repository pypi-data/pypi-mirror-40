# DiSwarm Handler
Basic DiSwarm bot handling class, and standardized communication protocol

## Usage
Main class: `Handler(channel, token, swarm_id, bot_id, lead_timeout=5, role=None)`
Channel: Discord server channel to run swarm in
Token: Discord bot token
Swarm_id: Unique id of entire swarm
Bot_id: Unique id of bot
Lead_timeout: Seconds before bot declares itself swarm leader
Role: Role in swarm. Changing this from None overrides leader/drone selection.


Subclass this, and redefine the function `process_one(self, response)` to perform different tasks based on input. This is much like the `socketserver.BaseRequestHandler.handle()` method.

Other functions:
`request(req, args=())` Requests data from swarm. 
Req: Request text
Args: tuple of arguments to pass to swarm

`process()`: Processes swarm queue and returns list of `process_one()` outputs

## Notes
- Swarm ID: the same for all bots in your swarm, but it should be unique from any other swarm, at least on your swarm channel. To be safe, use a randomly generated string or number. Make sure every bot in your swarm has the same id, because bots with different ids cannot see eachother's messages.

## Requires
- `pip install DiSwarm` (Will install all dependencies

As an alternative, run `pip install diswarm-handler` to download this and all dependencies.
