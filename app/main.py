import uuid
from backend.orchestrator.state_schema import ProfileBotState
from backend.orchestrator.langgraph_graph import get_graph_runner
from app.ui_utils import get_mock_profile

class SimpleLinkedInGenieTerminal:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.state = ProfileBotState(session_id=self.session_id)
        self.graph_runner = get_graph_runner()

    def run(self):
        print("Welcome to LinkedIn Genie. Type 'exit' to quit.")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            if "linkedin.com/in/" in user_input:
                self.state.linkedin_url = user_input
                self.state.linkedin_data = get_mock_profile()
            self.state.user_input = user_input
            self.state.conversation_history.append({"role": "user", "content": user_input})
            updated_state_dict = self.graph_runner.invoke(
                self.state.model_dump(),
                config={"configurable": {"thread_id": self.state.session_id}},
            )
            self.state = ProfileBotState.model_validate(updated_state_dict)
            if self.state.current_bot_response:
                print("Bot:", self.state.current_bot_response)

def main():
    app = SimpleLinkedInGenieTerminal()
    app.run()

if __name__ == "__main__":
    main()
