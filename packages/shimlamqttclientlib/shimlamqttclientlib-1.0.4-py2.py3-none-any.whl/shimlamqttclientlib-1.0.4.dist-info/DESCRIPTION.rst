# SHIMLA MQTT Python 3.x Client Library

A library that does the following:
* Acts as a wrapper around paho mqtt python library - supports **asynchronous connect/pub/sub APIs**
* Tests periodically if a client is connected to a specified broker, reconnects on any failure
* Provides ability to connect to secondary broker in case of primary broker connection repetitive failures
* Tests if client could connect to the internet to help narrow down any general connectivity issues
* Implements a **periodic publish API** from a separate thread


