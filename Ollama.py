import ollama
import re
import os
import time
import json
from typing import List, Dict, Optional, Tuple, Any

# ANSI escape codes for clean UI
class Colors:
    RED = '\033[91m' 
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    GRAY = '\033[90m' 
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def spinner(seconds: int):
    """Display a spinner animation for the specified number of seconds."""
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    start_time = time.time()
    while time.time() - start_time < seconds:
        for char in spinner_chars:
            print(f"\r{Colors.CYAN}Thinking {char}{Colors.RESET}", end='', flush=True)
            time.sleep(0.1)
    print('\r' + ' ' * 30 + '\r', end='', flush=True)

def extract_final_answer(text: str) -> str:
    """
    Extracts the final answer from the chain-of-thought text.
    If the text contains "Final Answer:", returns the content after it;
    otherwise, returns the last non-empty paragraph.
    """
    # Look for the Final Answer tag
    pattern = r"Final Answer:(.*?)(?=\n\n|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # If no Final Answer tag, try to extract the conclusion from the last paragraph
    paragraphs = text.split("\n\n")
    for paragraph in reversed(paragraphs):
        if paragraph.strip() and not paragraph.startswith("Thought:") and not paragraph.startswith("Analysis:") and not paragraph.startswith("Reflection:") and not paragraph.startswith("Next Step:"):
            return paragraph.strip()
    
    # If nothing else works, return the last non-empty line
    lines = text.strip().split("\n")
    for line in reversed(lines):
        if line.strip():
            return line.strip()
    
    return ""

def contains_final_answer(text: str) -> bool:
    """Returns True if 'Final Answer:' is found in the text (case-insensitive)."""
    return bool(re.search(r'Final Answer:', text, re.IGNORECASE))

class ReasoningConfig:
    """Holds configuration parameters for the reasoning process."""
    def __init__(
        self, 
        max_iterations: int = 5, 
        temperature: float = 0.7, 
        model: str = 'reasonchat'
    ):
        self.max_iterations = max_iterations
        self.temperature = temperature
        self.model = model

def build_system_prompt(max_iterations: int) -> str:
    """
    Constructs the system prompt to enforce a hidden internal chain-of-thought.
    """
    return f"""
You are a Reasoning AI assistant designed to provide accurate, concise, and relevant answers.

For each user query, follow this structured process:

1. **Complexity Assessment**
- Assess query complexity (1-Simple to 3-Complex):
  1: Direct recall (facts, definitions, greetings)
  2: Moderate analysis or connecting concepts
  3: Deep reasoning or complex analysis
- Perform assessment internally

2. **Reasoning Process** (NEVER SHOWN TO USER)
- Break complex questions into manageable steps
- Consider multiple approaches when appropriate
- Think step-by-step through calculations and logic
- Verify work and check for errors
- Consider edge cases and counterarguments
- Use up to {max_iterations} internal thinking steps
- Focus on accuracy over complexity
- Reduce hallucinations by cross-referencing facts

3. **Response Structure**
- Keep all reasoning completely internal
- ONLY share what follows "Final Answer:"
- Format:

Final Answer: [Your complete, verified response]

4. **Quality Standards**
- Prioritize accuracy above all
- Verify facts and calculations internally
- Provide clear, concise answers
- Address the question directly
- Acknowledge limitations when uncertain
- Choose reasonable interpretations for ambiguity

Core Rules:
- NEVER show internal thinking to users
- ALWAYS use "Final Answer:" tag
- Focus on correct answers over showing work
- Take time to verify complex solutions
- Maintain helpful but direct tone

Remember: Provide accurate, helpful answers, keeping all reasoning internal and for your use only.
"""

def generate_thinking_process(
    config: ReasoningConfig,
    user_input: str,
    conversation_history: List[Dict[str, str]],
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Generates the assistant's response using internal chain-of-thought reasoning.
    Iterates until a final answer is found or max iterations are reached.
    
    Returns a dictionary with:
    - 'answer': The final answer to show the user
    - 'thinking': The complete thinking process
    - 'iterations': Number of iterations used
    """
    # Handle simple inquiries directly
    simple_responses = {
        "hello": "Hey there! What can I help you with today?",
        "hi": "Hi! What's up?",
        "hey": "Hey! What's on your mind?",
        "hello there": "Hey there! How can I help?",
        "hi there": "Hi there! Need anything?",
        "what is your name?": "I'm an AI assistant powered by reasoning. What can I help you with?",
        "who are you?": "I'm your AI assistant with some serious thinking skills! What's on your mind?",
        "thank you": "No problem! Let me know if you need anything else!",
        "thanks": "Anytime! Anything else you're curious about?",
        "goodbye": "Later! Come back if you have more questions!",
        "bye": "See ya! Have a good one!"
    }
    
    user_input_lower = user_input.lower().strip()
    if user_input_lower in simple_responses:
        return {
            'answer': simple_responses[user_input_lower],
            'thinking': f"Simple greeting detected: '{user_input}'. Providing direct response.",
            'iterations': 0
        }
    
    iteration = 0
    final_answer = ""
    system_prompt = build_system_prompt(config.max_iterations)
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add relevant conversation history for context
    # Only include the last 3 exchanges to avoid context overflow
    recent_history = conversation_history[-6:] if len(conversation_history) > 6 else conversation_history
    messages.extend(recent_history)
    
    # Add the current user input
    messages.append({"role": "user", "content": user_input})
    complete_thinking = []
    
    while iteration < config.max_iterations and not final_answer:
        iteration += 1
        if verbose:
            spinner(1)  # Show a spinner during processing

        try:
            # Inform model about current iteration
            current_context = messages[-1]["content"]
            if "Continue" in current_context:
                messages[-1]["content"] = f"Continue thinking about this problem. You can provide a Final Answer when you're ready."
            
            response = ollama.chat(
                model=config.model,
                messages=messages,
                options={"temperature": config.temperature},
                stream=True
            )
            
            thinking_text = ""
            if verbose:
                print(f"\n{Colors.YELLOW}Thinking (Step {iteration}/{config.max_iterations}): ", end="", flush=True)
            
            for chunk in response:
                chunk_text = chunk.get('message', {}).get('content', "")
                thinking_text += chunk_text
                if verbose:
                    print(f"{chunk_text}", end="", flush=True)
            
            if verbose:
                print(Colors.RESET)
            
            complete_thinking.append(f"=== Iteration {iteration} ===\n{thinking_text}")
            messages.append({"role": "assistant", "content": thinking_text})

            if contains_final_answer(thinking_text):
                extracted = extract_final_answer(thinking_text)
                if extracted:
                    final_answer = extracted
                    break

            # Continue thinking - let the model decide when to conclude
            messages.append({"role": "user", "content": "Continue if you need more thinking steps, or provide your Final Answer if you're ready."})

        except Exception as e:
            return {
                'answer': f"Error: {str(e)}",
                'thinking': f"Error occurred during iteration {iteration}: {str(e)}",
                'iterations': iteration
            }

    # Force a final answer if no final answer was reached within the max iterations
    if not final_answer:
        force_prompt = "Please provide your best final answer based on your reasoning so far."
        messages.append({"role": "user", "content": force_prompt})
        try:
            final_response = ollama.chat(
                model=config.model,
                messages=messages,
                options={"temperature": config.temperature},
                stream=False
            )
            forced_text = final_response.get('message', {}).get('content', "")
            complete_thinking.append(f"=== Conclusion ===\n{forced_text}")
            final_answer = extract_final_answer(forced_text) or forced_text
        except Exception as e:
            return {
                'answer': f"Error during final response: {str(e)}",
                'thinking': "\n".join(complete_thinking) + f"\n\nError during final response: {str(e)}",
                'iterations': iteration
            }
    
    full_thinking = "\n\n".join(complete_thinking)
    
    if not final_answer:
        final_answer = "I couldn't reach a clear answer. Please try rephrasing your question!"
    
    return {
        'answer': final_answer,
        'thinking': full_thinking,
        'iterations': iteration
    }

def save_conversation_log(conversation_history: List[Dict[str, str]], thinking_logs: List[Dict[str, Any]]):
    """Saves the conversation history and thinking logs to a file."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"reasonchat_conversation_{timestamp}.json"
    
    data = {
        "timestamp": timestamp,
        "conversation": conversation_history,
        "thinking_logs": thinking_logs
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return filename
    except Exception as e:
        return f"Error saving conversation: {str(e)}"

def chat_with_ollama(
    config: ReasoningConfig = ReasoningConfig(),
    verbose: bool = True
):
    """
    Provides a command-line interface for the reasoning-enhanced chat.
    Maintains conversation history and processes user commands.
    """
    clear_console()
    print(f"{Colors.BOLD}{Colors.BLUE}ReasonChat+ {Colors.CYAN}v2.0{Colors.RESET} | Model: {config.model}")
    print(f"{Colors.GRAY}Type a question or '/help' for commands{Colors.RESET}\n")
    
    conversation_history: List[Dict[str, str]] = []
    thinking_logs: List[Dict[str, Any]] = []
    
    while True:
        try:
            user_input = input(f"{Colors.GREEN}You: {Colors.RESET}")
            
            # Handle commands
            if user_input.lower() in ["/exit", "/quit"]:
                if len(conversation_history) > 0:
                    save = input(f"{Colors.YELLOW}Save conversation history? (y/n): {Colors.RESET}")
                    if save.lower() == 'y':
                        saved_file = save_conversation_log(conversation_history, thinking_logs)
                        print(f"{Colors.CYAN}Conversation saved to: {saved_file}{Colors.RESET}")
                print(f"{Colors.YELLOW}Goodbye!{Colors.RESET}")
                break
                
            elif user_input.lower() == "/help":
                print(f"\n{Colors.CYAN}Commands:{Colors.RESET}")
                print(f"{Colors.CYAN}/exit, /quit - Exit the application{Colors.RESET}")
                print(f"{Colors.CYAN}/model [name] - Change the model (e.g., /model llama3){Colors.RESET}")
                print(f"{Colors.CYAN}/temp [0.0-1.0] - Set temperature{Colors.RESET}")
                print(f"{Colors.CYAN}/quiet - Hide thinking process{Colors.RESET}")
                print(f"{Colors.CYAN}/verbose - Show thinking process{Colors.RESET}")
                print(f"{Colors.CYAN}/clear - Clear screen{Colors.RESET}")
                print(f"{Colors.CYAN}/history - Show conversation history{Colors.RESET}")
                print(f"{Colors.CYAN}/save - Save conversation log{Colors.RESET}")

                print(f"{Colors.CYAN}/iterations [2-10] - Set maximum iterations{Colors.RESET}")
                print(f"{Colors.CYAN}/debug - Show technical details{Colors.RESET}")
                continue
                
            elif user_input.lower() == "/history":
                print("\n=== Conversation History ===")
                for i, msg in enumerate(conversation_history):
                    role = msg["role"].capitalize()
                    content = msg["content"]
                    # Truncate long messages for display
                    if len(content) > 200:
                        content = content[:200] + "..."
                    print(f"\n{Colors.YELLOW}{i+1}. {role}:{Colors.RESET} {content}")
                print("\n=========================")
                continue
                
            elif user_input.lower() == "/save":
                saved_file = save_conversation_log(conversation_history, thinking_logs)
                print(f"{Colors.CYAN}Conversation saved to: {saved_file}{Colors.RESET}")
                continue
                
            elif user_input.lower().startswith("/model "):
                config.model = user_input[7:].strip()
                print(f"{Colors.CYAN}Model set to: {config.model}{Colors.RESET}")
                continue
                
            elif user_input.lower().startswith("/temp "):
                try:
                    temp = float(user_input[6:].strip())
                    if 0 <= temp <= 1:
                        config.temperature = temp
                        print(f"{Colors.CYAN}Temperature set to: {config.temperature}{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}Temperature must be between 0.0 and 1.0{Colors.RESET}")
                except ValueError:
                    print(f"{Colors.RED}Invalid temperature value.{Colors.RESET}")
                continue
                
            elif user_input.lower() == "/verbose":
                verbose = True
                print(f"{Colors.CYAN}Showing thinking process{Colors.RESET}")
                continue
                
            elif user_input.lower() == "/quiet":
                verbose = False
                print(f"{Colors.CYAN}Hiding thinking process{Colors.RESET}")
                continue
                
            elif user_input.lower().startswith("/iterations "):
                try:
                    iters = int(user_input[12:].strip())
                    if 2 <= iters <= 10:
                        config.max_iterations = iters
                        print(f"{Colors.CYAN}Maximum iterations set to: {config.max_iterations}{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}Iterations must be between 2 and 10{Colors.RESET}")
                except ValueError:
                    print(f"{Colors.RED}Invalid iteration value.{Colors.RESET}")
                continue
                
            elif user_input.lower() == "/debug":
                print(f"\n{Colors.CYAN}=== Debug Information ==={Colors.RESET}")
                print(f"Model: {config.model}")
                print(f"Temperature: {config.temperature}")
                print(f"Max iterations: {config.max_iterations}")
                print(f"Conversation history length: {len(conversation_history)} messages")
                print(f"Thinking logs count: {len(thinking_logs)}")
                print(f"{Colors.CYAN}========================{Colors.RESET}")
                continue
                
            elif user_input.lower() == "/clear":
                clear_console()
                print(f"{Colors.BOLD}{Colors.BLUE}ReasonChat+ {Colors.CYAN}v2.0{Colors.RESET} | Model: {config.model}")
                print(f"{Colors.GRAY}Type a question or '/help' for commands{Colors.RESET}\n")
                continue

            if not user_input.strip():
                continue

            # Process the user's question
            if not verbose:
                print(f"{Colors.CYAN}Thinking...{Colors.RESET}")

            conversation_history.append({"role": "user", "content": user_input})
            
            # Let the model handle its own complexity assessment
            
            # Generate response with thinking process
            result = generate_thinking_process(config, user_input, conversation_history, verbose=verbose)
            
            # Store the thinking log
            thinking_logs.append({
                "user_input": user_input,
                "thinking": result['thinking'],
                "iterations": result['iterations']
            })
            
            # Add the final answer to conversation history
            conversation_history.append({"role": "assistant", "content": result['answer']})
            
            # Display the answer
            print(f"\n{Colors.BLUE}Answer: {Colors.RESET}{result['answer']}\n")

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Cancelled. Type /exit to quit.{Colors.RESET}")
        except Exception as e:
            print(f"\n{Colors.RED}Error: {str(e)}{Colors.RESET}")

if __name__ == "__main__":
    chat_with_ollama()