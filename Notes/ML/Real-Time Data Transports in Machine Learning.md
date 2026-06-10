

Machine learning systems don't just need models; they need reliable ways to move data between producers (applications, sensors, users) and consumers (models, databases, dashboards, alerting systems). The choice of transport *depends on latency requirements and system scale*.

HTTP is the most common transport in production ML. A client sends features to a prediction endpoint and receives a response. This works well for loan approvals, customer churn predictions, recommendation requests, and most business applications where predictions are generated on demand. If decisions can wait seconds or longer, HTTP is usually sufficient.

**Kafka** is used when data arrives continuously and multiple systems need access to the same events. Producers publish events to topics, and consumers read them independently. Common use cases include fraud detection, recommendation systems, online feature stores, clickstream analysis, and real-time monitoring. Kafka's major advantage is event retention and replay, allowing teams to recompute features or retrain systems using historical streams.

**RabbitMQ** serves a different purpose. It functions primarily as a task queue rather than an event log. Messages are processed and removed. It is commonly used for asynchronous ML workloads such as document classification, image processing, and background inference jobs where replaying historical data is unnecessary.

**WebSockets** provide persistent client-server connections and are useful when predictions must be pushed continuously to users. Examples include real-time dashboards, stock prediction interfaces, and anomaly monitoring systems. They are typically used between backend services and user interfaces rather than between internal ML components.

gRPC is a high-performance alternative to REST APIs. It uses Protocol Buffers instead of JSON and is common in low-latency microservice environments where models communicate with other backend services at high throughput.

**MQTT** is a lightweight messaging protocol designed for IoT and sensor networks. Small devices with limited memory and power publish data to topics through a broker. Other systems subscribe to those topics. Sensors do not need to know who consumes their data.

Example topics:

- factory/line1/temperature
    
- factory/line1/vibration
    
- factory/line1/humidity
    

A typical sensor ML pipeline looks like:

<mark style="background: #BBFABBA6;">Sensors → MQTT Broker → Stream Processing → ML Model → Alerts</mark>

The MQTT broker acts as a central hub. Sensors publish readings, while databases, dashboards, and ML systems subscribe to the same streams. This decouples devices from downstream systems.

Raw sensor values are often insufficient for prediction. Streaming systems compute features such as rolling averages, rates of change, moving windows, and historical trends before sending enriched data to models. For predictive maintenance, a model may care less about a temperature of 75°C and more about the fact that temperature has risen steadily over the past 10 minutes.

Large architectures often combine MQTT and Kafka:

Sensors → MQTT → Broker → Kafka → ML Systems

MQTT handles communication with devices, while Kafka handles large-scale backend event processing.

> Rule of thumb: use HTTP for request-response predictions, Kafka for event-driven streaming systems, RabbitMQ for queued tasks, WebSockets for live client updates, gRPC for high-performance service communication, and MQTT for sensor and IoT data collection.