# Module 2 — Notification Service

## Goal

The objective of this module was **not** to build a production-ready notification platform.

The objective was to understand **why modern messaging systems are designed the way they are** by building our own simplified implementation first.

Instead of starting with RabbitMQ, Kafka, or cloud messaging services, we evolved the system one problem at a time.

---

# Tech Stack

- **Backend:** Python
- **Framework:** FastAPI
- **Validation:** Pydantic
- **Concurrency:** Python Threads
- **Messaging:** Custom In-Memory Message Broker

---

# Learning Philosophy

Throughout this module we followed one rule:

> **Never introduce a new component until the current design exposes a real problem.**

Instead of beginning with queues, workers, retries and acknowledgements, we started with the simplest implementation and evolved the architecture naturally.

---

# Version 1

The first implementation was completely synchronous.

```text
HTTP Request
      │
      ▼
Generate Email
      │
      ▼
Send Email
      │
      ▼
HTTP Response
```

This solved the initial requirement:

> Send an email notification.

---

# Problem 1

The Product Manager reported:

> Registration now takes 8 seconds because email sending is slow.

The application worked correctly, but the user experience was poor.

---

# Version 2

We introduced a background worker.

```text
HTTP Request
      │
      ▼
Generate Email
      │
      ▼
In-Memory Message Broker
      │
      ▼
202 Accepted
```

Background:

```text
Worker
    │
    ▼
Email Provider
```

The HTTP request no longer waited for SMTP.

---

# Producer / Consumer

The application naturally evolved into the Producer / Consumer pattern.

Producer:

- Notification Endpoint

Consumer:

- Email Worker

Communication:

- In-Memory Message Broker

---

# Worker

The EmailWorker became responsible for:

- Background processing
- Worker lifecycle
- Thread ownership
- Retry execution
- Delivery acknowledgement

The application no longer knew anything about threads.

Instead it interacted with:

```python
worker.start()

worker.stop()
```

---

# Application Lifecycle

As background resources were introduced, the application required startup and shutdown phases.

This naturally led to FastAPI's lifespan API.

The application lifecycle became:

```text
Create Resources
        │
        ▼
Start Worker
        │
        ▼
Application Running
        │
        ▼
Shutdown
```

---

# Dependency Injection

Shared resources are owned by the application.

Application Resources:

- Message Broker
- Email Provider
- Email Worker

Resources are stored in:

```text
app.state.resources
```

Endpoints receive dependencies through FastAPI Dependency Injection rather than creating them themselves.

---

# In-Memory Message Broker

The broker evolved from a simple queue into a simplified message broker.

Responsibilities:

- Publish messages
- Deliver messages
- Track messages currently being processed
- Dead Letter Queue
- Acknowledgements

Internally it maintains:

```text
Ready Queue

Processing Map

Dead Letter Queue
```

---

# Retry Mechanism

Immediate retries were introduced for temporary failures.

Current strategy:

- Maximum retry attempts: 3
- Retry immediately
- On permanent failure:
    - Move message to Dead Letter Queue

This intentionally exposes the limitations of immediate retry strategies.

---

# Dead Letter Queue

Instead of silently dropping failed messages, permanently failed messages are moved to a Dead Letter Queue.

Purpose:

- Operational visibility
- Manual inspection
- Future replay

---

# Acknowledgements (ACK)

The broker no longer deletes a message immediately after it is consumed.

Instead:

```text
Ready

↓

Processing

↓

ACK

↓

Removed
```

This prevents premature deletion before successful processing.

---

# Design Principles Learned

## Separation of Concerns

- Endpoint orchestrates work.
- Template service generates email content.
- Worker processes messages.
- Broker transports messages.
- Provider sends emails.

---

## Single Responsibility

Every component owns exactly one responsibility.

Examples:

- EmailTemplateService → Generate email content.
- EmailWorker → Process messages.
- EmailProvider → Deliver emails.
- MessageBroker → Transport messages.

---

## Dependency Injection

Objects should receive dependencies rather than constructing them.

Workers receive:

- Broker
- Provider

Endpoints receive:

- Broker

through FastAPI dependency injection.

---

## Application Ownership

Resources belong to the application rather than global variables or singletons.

```text
Application

↓

Resources

↓

Broker

Worker

Provider
```

---

## Object Ownership

The project repeatedly emphasized asking:

> **Who owns this state?**

Examples:

- Running flag → Worker
- Processing map → Broker
- Email content → Email
- Retry policy → Worker (current version)

---

# Known Limitations

The current implementation intentionally leaves several production problems unsolved.

Examples:

- Immediate retries cause head-of-line blocking.
- Processing state is lost after process crashes.
- In-memory broker is not durable.
- No visibility timeout.
- No replay of Dead Letter Queue.
- No delayed retries.
- No exponential backoff.
- No distributed workers.

These limitations were intentionally left unresolved because they motivate real message brokers such as RabbitMQ.

---

# What We Chose Not To Build

The following features were intentionally deferred:

- Retry scheduler
- Exponential backoff
- Delayed delivery
- Priority queues
- Distributed broker
- Production logging
- Monitoring
- Metrics

These are important production features but were outside the learning goals of this module.

---

# Key Takeaways

This module was not about learning FastAPI.

It was about learning the concepts behind messaging systems.

By building our own broker first, we naturally discovered why production systems introduce concepts such as:

- Workers
- Producer / Consumer
- Blocking Queues
- Dependency Injection
- Application Lifecycle
- Retries
- Dead Letter Queues
- Acknowledgements

Only after understanding these problems are we ready to appreciate dedicated messaging systems such as RabbitMQ.

---

# Next Module

## Module 3 — Real-Time Chat System

The next system will build on everything learned here while introducing a completely different set of distributed system challenges.

New concepts include:

- WebSockets
- Persistent connections
- User presence (online/offline)
- One-to-one messaging
- Message ordering
- Read receipts
- Typing indicators
- Heartbeats and connection management
- Fan-out (one sender → many recipients)
- Pub/Sub
- Horizontal scaling
- Redis Pub/Sub (later)
- Multi-server message routing
- Offline message delivery
- Chat history persistence

Just like previous modules, the architecture will evolve naturally from the problems we encounter rather than being designed upfront.