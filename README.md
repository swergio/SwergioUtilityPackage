# Utility Package for swergio

This is a utility package for a SwarnAnalytics set-up including several reusable modules and functions. 

## Modules:

#### SocketIO Client
A default SocketIOClient to communicate with Flask-SocketIO server.

#### Message Utilities
Definition of several classes for a common interpretation of messages including:
- the definition of the "external" message class (Message Interface) to communicate between separate components
- classes for representation of messages as neural nets inputs (internal messages) like "Chat Type", "MessageType", and "Text of the Message".

#### Expert Data
A module to read and prepare a CSV file including observations and actions of optimal (expert) trajectories. 

The provided CSV file needs to have the following header format:

O_Namespace = Observation Namespace (e.g. AGENT_A)
O_Type = Observation Type (e.g. QUESTION)
O_Text = Observation Text (e.g. "What is zero minus four")
A_Namespace  = Action Namespace (e.g. AGENT_A)
A_Type = Observation Type (e.g. ANSWER)
A_Text = Observation Text (e.g. -4)
A_DoAct = Is the Action actionable? 0 or 1?
ComID = An ID to group a full communication (e.g. a request of a client)
Step = ID of the current step

#### Communication Environment
Basic class for  swergio agents to communicate with other components. Includes several functionalities like: 
- initializing of all needed classes (e.g. setting, interface, types etc.)
- transformation of external messages and internal neural network representation
- review of messages before sending
- feedback functionality  as response to provided answers

## Settings
The default settings of all modules are defines as JSON file in "Settings/DEFAULT_settings.json".
They can be customized by providing the path to a custom setting file with the same structure.

## References
Flask-SocketIO - https://github.com/miguelgrinberg/Flask-SocketIO 
