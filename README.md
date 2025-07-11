# langgraph

**Run on python environment for feasibility**

Step 1: Install requirements.txt

` pip install -r requirements.txt`

Step 2: Run langgrpah studio command on terminal.

` langgraph dev`

# HOW IT WORKS

The program goes like this: User asks which model is fit for his usecase, like (what do i use for image generation or audio transcribe?) and the langgraph will match the tools , explain the reason and give combined response at the end all through graph.
![image](https://github.com/user-attachments/assets/f9580af0-8e6f-428f-99d3-e9fd7fe4766c) 


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

![image](https://github.com/user-attachments/assets/6da0e04e-9bc6-4193-a0ba-a9eb56b0be96)


when running `langgrpah dev` this graph is triggered and the flow will start from here.

Firstly it will run **create_graph()** function

A node represents a destination, and an edge is the path that connects it to another node, defined by a start and end point.

![image](https://github.com/user-attachments/assets/79972740-ddbf-4007-b9ae-21e094b46ac5)


# HERE IS THE FLOW

When **Create_graph** function is triggered
it goes to start node **get_query**
Here it accepts query from user

then,
The user query, received via state.get("message"), is passed from node to node, following the path defined by the edges. At each node, the query is processed with the respective tools or LLM prompt, and a response is generated. The updated message is then passed to the next node in the pipeline, continuing until the process is complete.

This is a basic flow of langgraph.
