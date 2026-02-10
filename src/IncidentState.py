import typing
from typing import Optional, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END,START
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import json
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


intake_prompt="""  
You are an Incident Intake Agent in a production system.

Your task:
- Convert a human incident description into a structured incident summary.
- Do NOT investigate, explain, or suggest fixes.

Rules:
- Use only information explicitly or implicitly present.
- If service is unclear, infer the most likely service.
- Output must be valid JSON and match the schema exactly.
- Do not add extra fields.

Severity rules:
- login failures impacting users → high
- degraded performance → medium
- informational → low

json_format: 
 raw_report,
 service_name,
 system,
 suspected_trigger,  
 severity 


Input:
{raw_report}


Output JSON:

"""

intake_prompt_template = PromptTemplate(
    template=intake_prompt,
    input_variables=["raw_report"]
)


class IncidentState(TypedDict):
      raw_report:str
      service_name:Optional[str]
      system:Optional[str]
      suspected_trigger:Optional[str]
      severity:Optional[str]
      
      

def extract_incident_states(incident_state:IncidentState) ->IncidentState:
    prompt=intake_prompt_template.format    (raw_report=incident_state["raw_report"])
    response=llm.invoke(prompt)
    content = response.content.strip()

    # 🔥 Strip markdown code fences
    if content.startswith("```"):
        content = content.split("```")[1].strip()
        if content.startswith("json"):
            content = content[4:].strip()

    data = json.loads(content)
    return {
        **incident_state,
        "service_name": data.get("service_name"),
        "system": data.get("system"),
        "suspected_trigger": data.get("suspected_trigger"),
        "severity": data.get("severity"),
    }
    
    return incident_state   


state_graph=StateGraph(IncidentState)
state_graph.add_node("extract_incident_states",extract_incident_states)

state_graph.add_edge(START,"extract_incident_states")
state_graph.add_edge("extract_incident_states",END)
app=state_graph.compile()


def run_incident_intake(raw_report:str)->IncidentState:
    initial_state:IncidentState={"raw_report":raw_report}
    final_state=app.invoke(input=initial_state)
    print("Final Incident State:",final_state)
    return final_state

 
 
     