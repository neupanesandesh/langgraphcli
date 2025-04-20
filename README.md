# langgraph

**Run on python environment for feasibility**

Step 1: Install requirements.txt

` pip install -r requirements.txt`

Step 2: Run langgrpah studio command on terminal.

` langgraph dev`

# HOW IT WORKS

It has a langgraph.json file to run on langgraph studio that looks like this:

```
{
  "dependencies": ["./requirments.txt"],
  "graphs": {
    "agent": "./lang.py:graph"
  }
}
```

The `langgraph dev` command will run the langgraph.json from where dependencies and the graph is triggered.

This is where the graph resides in code:

![image](https://github.com/user-attachments/assets/eb4080aa-1c98-48e6-8a04-d100393d9f40)

when running `langgrpah dev` this graph is triggered and the flow will start from here.

Firstly it will run **create_graph()** function

A node represents a destination, and an edge is the path that connects it to another node, defined by a start and end point.

![image](https://github.com/user-attachments/assets/63602eca-b5ca-412d-a928-559ce086352a)

# HERE IS THE FLOW

When **Create_graph** function is triggered
it goes to start node **get_query**
Here it accepts query from user

then,
The user query, received via state.get("message"), is passed from node to node, following the path defined by the edges. At each node, the query is processed with the respective tools or LLM prompt, and a response is generated. The updated message is then passed to the next node in the pipeline, continuing until the process is complete.

This is a basic flow of langgraph, an langgraph interrupt example for confirmation is also provided in the lang.py file commented below the current flow.
