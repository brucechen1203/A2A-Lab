"""Agent Card definition and validation utilities for the A2A server."""

AGENT_CARD = {
	"id": "echo-agent-v1",
	"name": "Echo Agent",
	"version": "1.0.0",
	"description": "A simple agent that echoes back any text it receives.",
	"url": "http://localhost:8000",  # updated at deploy time
	"capabilities": {
		"streaming": False,
		"pushNotifications": False,
	},
	"defaultInputModes": ["text/plain"],
	"defaultOutputModes": ["text/plain"],
	"contact": {
		"email": "echo-agent@example.com",
	},
	"skills": [
		{
			"id": "echo",
			"name": "Echo",
			"description": "Returns the user message verbatim.",
			"inputModes": ["text/plain"],
			"outputModes": ["text/plain"],
		},
		{
			"id": "summarise",
			"name": "Summarise",
			"description": "Returns a concise summary of the user message.",
			"inputModes": ["text/plain"],
			"outputModes": ["text/plain"],
		},
	],
}


def validate_card(card: dict) -> bool:
	"""Return True when an Agent Card includes all required A2A fields."""
	required_top_level = {
		"id",
		"name",
		"version",
		"description",
		"url",
		"capabilities",
		"defaultInputModes",
		"defaultOutputModes",
		"contact",
		"skills",
	}

	if not isinstance(card, dict):
		return False

	if not required_top_level.issubset(card.keys()):
		return False

	capabilities = card.get("capabilities")
	if not isinstance(capabilities, dict):
		return False
	if "streaming" not in capabilities or "pushNotifications" not in capabilities:
		return False

	contact = card.get("contact")
	if not isinstance(contact, dict) or "email" not in contact:
		return False

	skills = card.get("skills")
	if not isinstance(skills, list) or not skills:
		return False

	required_skill_fields = {"id", "name", "description", "inputModes", "outputModes"}
	for skill in skills:
		if not isinstance(skill, dict):
			return False
		if not required_skill_fields.issubset(skill.keys()):
			return False

	return True
