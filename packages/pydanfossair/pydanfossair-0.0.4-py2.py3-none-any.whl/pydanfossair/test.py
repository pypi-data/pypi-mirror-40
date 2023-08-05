from danfossclient import DanfossClient
from commands import ReadCommand

config = {}
config["host"] = "10.100.0.11"
client = DanfossClient(config)

print(client.command(ReadCommand.exhaustTemperature))
print(client.command(ReadCommand.supplyTemperature))
print(client.command(ReadCommand.extractTemperature))
print(client.command(ReadCommand.outdoorTemperature))






