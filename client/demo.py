from client import A2AClient


def main() -> None:
	agent_url = "http://localhost:8000"

	with A2AClient(agent_url) as client:
		card = client.fetch_agent_card()
		print(f"Agent name: {card.get('name', '<unknown>')}")
		print(f"Skills: {client.get_skills()}")

		response = client.send_task("Hello from the client!")
		echoed = client.extract_text(response)
		print(f"Echoed response: {echoed}")


if __name__ == "__main__":
	main()

