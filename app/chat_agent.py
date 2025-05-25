# app/chat_agent.py
from __future__ import annotations

import json
from typing import Dict, List

from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_openai import ChatOpenAI


# ──────────────────────────── PROMPT ────────────────────────────
CHAT_PROMPT = PromptTemplate.from_template(
    """
You are an enthusiastic job-search assistant.  
Your mission: get the user's **country, city, and desired job title**, then
return a JSON array of matching positions.

Conversation so far:
{chat_history}

Current details you know  
‣ Country: {country}  
‣ City:    {city}  
‣ Title:   {job_title}

If any of those is still "Unknown", ask only for what's missing.  
Once you have everything, run a search.

You can use these tools:
{tools}

Follow the ReAct format **exactly**:

Question: <the latest user message>
Thought: <your reasoning>
Action: <one of [{tool_names}]>
Action Input: <tool input>
Observation: <tool result>
… (repeat Thought/Action as needed)
Thought: I now know the final answer
Final Answer: <pure JSON array of jobs>

Each job object must contain:
• position_name 
• company 
• location 
• description (≤ 5 sentences)
• link_to_position 
• link_to_apply

avoid duplicated jobs and inactive jobs 

Begin!

Question: {input}
{agent_scratchpad}
"""
)


class JobSearchAgent:
    """Keeps session state and talks to Tavily + OpenAI."""

    def __init__(self) -> None:
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.search_tool = TavilySearchResults(max_results=5)
        self.tools = [self.search_tool]

        # Persistent memory for the chat session
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="input"
        )

        # Internal state that must never be None
        self.country: str = "Unknown"
        self.city: str = "Unknown"
        self.job_title: str = "Unknown"

        # Build the agent & executor
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=CHAT_PROMPT,
        )
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
        )

    # ────────────────────────────────────────────────────────────
    # Small helper LLM calls to pull entities from user sentences
    # ────────────────────────────────────────────────────────────
    def _extract_location(self, text: str) -> Dict[str, str]:
        prompt = (
            f'Extract country and city from: "{text}". '
            "Return JSON like {\"country\": \"X\" , \"city\": \"Y\"} "
            "or {} if nothing found."
        )
        resp = self.llm.invoke([HumanMessage(content=prompt)]).content
        try:
            data = json.loads(resp)
            return {
                "country": data.get("country", self.country),
                "city": data.get("city", self.city),
            }
        except Exception:
            return {"country": self.country, "city": self.city}

    def _extract_title(self, text: str) -> str:
        prompt = (
            f'Extract the job title from: "{text}". '
            'Return **only** the job title, or "Unknown" if not found. '
            'Examples:\n'
            'Input: "I want to be a software engineer"\n'
            'Output: "Software Engineer"\n'
            'Input: "Looking for a job"\n'
            'Output: "Unknown"\n'
            'Input: "product manager"\n'
            'Output: "Product Manager"'
        )
        resp = self.llm.invoke([HumanMessage(content=prompt)]).content.strip()
        # Clean up the response and ensure proper capitalization
        if resp.lower() == "unknown" or not resp:
            return "Unknown"
        return resp.title()  # Capitalize first letter of each word

    def validate_position_values(self) -> tuple[bool, List[str]]:
        """
        Validates if all required position values are present.
        Returns a tuple of (is_valid, missing_fields)
        """
        missing: List[str] = [
            name
            for name, val in [
                ("country", self.country),
                ("city", self.city),
                ("job title", self.job_title),
            ]
            if val == "Unknown"
        ]
        return len(missing) == 0, missing

    # ────────────────────────────────────────────────────────────
    # Core entry-point
    # ────────────────────────────────────────────────────────────

    def process_chat_message(self, message: str) -> str:
        # --- update state -----------------------------------------------------
        loc = self._extract_location(message)
        self.country, self.city = loc["country"], loc["city"]
        
        # Extract job title and ensure it's not empty
        extracted_title = self._extract_title(message)
        self.job_title = extracted_title if extracted_title and extracted_title.lower() != "unknown" else "Unknown"

        # Validate position values
        is_valid, missing = self.validate_position_values()
        if not is_valid:
            nice_list = ", ".join(missing)
            return f"Got it. Could you also tell me your {nice_list}?"

        return "All info present."

    def process_message(self, message: str) -> str:
        # --- update state -----------------------------------------------------
        loc = self._extract_location(message)
        self.country, self.city = loc["country"], loc["city"]
        self.job_title = self._extract_title(message)

        # Validate position values
        is_valid, missing = self.validate_position_values()
        if not is_valid:
            nice_list = ", ".join(missing)
            return f"Got it. Could you also tell me your {nice_list}?"

        # --- All info present → run the search agent -------------------------
        search_prompt = (
            f"Search for open \"{self.job_title}\" roles in "
            f"{self.city}, {self.country}. "
            "Return **only** the JSON array specified in the prompt."
        )
        result = self.executor.invoke(
            {
                "input": search_prompt,
                "country": self.country,
                "city": self.city,
                "job_title": self.job_title,
            }
        )

        raw = result.get("output", "")
        raw = json.loads(raw)
        if "Final Answer:" in raw:
            raw = raw.split("Final Answer:")[-1].strip()
        return raw

    def reset(self) -> None:
        """Reset the agent's memory and state."""
        self.memory.clear()
        self.country = "Unknown"
        self.city = "Unknown"
        self.job_title = "Unknown"  