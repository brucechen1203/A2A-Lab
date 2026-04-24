async def handle_task(request) -> str:
	text_parts = [p.text for p in request.message.parts if p.type == "text"]
	combined = " ".join(text_parts).strip()

	if combined.startswith("!summarise"):
		return "This is a one-sentence mock summary of your request."

	# ECHO skill: return the input unchanged.
	return combined
