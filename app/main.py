import uuid
import json
from backend.orchestrator.state_schema import ProfileBotState
from backend.orchestrator.langgraph_graph import get_graph_runner
from linkedin.mock_profiles import get_mock_profile

class SimpleLinkedInGenieTerminal:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.state = ProfileBotState(session_id=self.session_id)
        self.graph_runner = get_graph_runner()

    def _format_suggestions(self, suggestions_dict):
        """Format structured suggestions for display"""
        if not suggestions_dict:
            return ""
        
        formatted_output = ""
        for section, content in suggestions_dict.items():
            if isinstance(content, list):
                formatted_output += f"\n{section.upper().replace('_', ' ')}:\n"
                for i, item in enumerate(content, 1):
                    if isinstance(item, dict):
                        formatted_output += f"  Option {i}:\n"
                        for key, value in item.items():
                            formatted_output += f"    {key}: {value}\n"
                    else:
                        formatted_output += f"  {i}. {item}\n"
            elif isinstance(content, dict):
                formatted_output += f"\n{section.upper().replace('_', ' ')}:\n"
                for key, value in content.items():
                    formatted_output += f"  {key}: {value}\n"
            else:
                formatted_output += f"\n{section.upper().replace('_', ' ')}: {content}\n"
        return formatted_output

    def _display_analysis_report(self, report):
        """Display profile analysis report in a readable format"""
        if not report:
            return
        
        print("\n" + "="*50)
        print("PROFILE ANALYSIS REPORT")
        print("="*50)
        
        for section, content in report.items():
            print(f"\n{section.upper().replace('_', ' ')}:")
            if isinstance(content, list):
                for item in content:
                    print(f"  • {item}")
            elif isinstance(content, dict):
                for key, value in content.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {content}")

    def _display_content_suggestions(self, suggestions):
        """Display content rewrite suggestions in a readable format"""
        if not suggestions:
            return
        
        print("\n" + "="*50)
        print("CONTENT SUGGESTIONS")
        print("="*50)
        
        formatted = self._format_suggestions(suggestions)
        if formatted:
            print(formatted)

    def _display_job_fit_report(self, report):
        """Display job fit evaluation report"""
        if not report:
            return
        
        print("\n" + "="*50)
        print("JOB FIT EVALUATION")
        print("="*50)
        
        if 'score' in report:
            print(f"Overall Fit Score: {report['score']}")
        
        formatted = self._format_suggestions(report)
        if formatted:
            print(formatted)

    def _display_career_guidance(self, guidance):
        """Display career guidance notes"""
        if not guidance:
            return
        
        print("\n" + "="*50)
        print("CAREER GUIDANCE")
        print("="*50)
        
        formatted = self._format_suggestions(guidance)
        if formatted:
            print(formatted)

    def run(self):
        print("Welcome to LinkedIn Genie. Type 'exit' to quit.")
        
        # Track what we've already shown to avoid duplicates
        last_shown_analysis = None
        last_shown_suggestions = None
        last_shown_job_fit = None
        last_shown_guidance = None
        
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            if "linkedin.com/in/" in user_input:
                self.state.linkedin_url = user_input
                self.state.linkedin_data = get_mock_profile(linkedin_url=self.state.linkedin_url)
            self.state.user_input = user_input
            self.state.conversation_history.append({"role": "user", "content": user_input})
            updated_state_dict = self.graph_runner.invoke(
                self.state.model_dump(),
                config={"configurable": {"thread_id": self.state.session_id}},
            )
            self.state = ProfileBotState.model_validate(updated_state_dict)
            
            # Display the bot's response
            if self.state.current_bot_response:
                print("Bot:", self.state.current_bot_response)
            
            # Automatically display new structured data when it becomes available
            if self.state.profile_analysis_report and self.state.profile_analysis_report != last_shown_analysis:
                self._display_analysis_report(self.state.profile_analysis_report)
                last_shown_analysis = self.state.profile_analysis_report
            
            if self.state.content_rewrites_suggestions and self.state.content_rewrites_suggestions != last_shown_suggestions:
                self._display_content_suggestions(self.state.content_rewrites_suggestions)
                last_shown_suggestions = self.state.content_rewrites_suggestions
            
            if self.state.job_fit_evaluation_report and self.state.job_fit_evaluation_report != last_shown_job_fit:
                self._display_job_fit_report(self.state.job_fit_evaluation_report)
                last_shown_job_fit = self.state.job_fit_evaluation_report
            
            if self.state.career_guidance_notes and self.state.career_guidance_notes != last_shown_guidance:
                self._display_career_guidance(self.state.career_guidance_notes)
                last_shown_guidance = self.state.career_guidance_notes

def main():
    app = SimpleLinkedInGenieTerminal()
    app.run()

if __name__ == "__main__":
    main()
