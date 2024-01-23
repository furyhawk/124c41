# MQTT


https://github.com/furyhawk/scratchpad/tree/main/mtqq

## RabbitMQ

```bash
# latest RabbitMQ 3.12
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```

## HiveMQ

```bash
docker run --name hivemq-edge -d -p 1883:1883 -p 8080:8080 hivemq/hivemq-edge
``````