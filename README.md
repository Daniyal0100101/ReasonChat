# ReasonChat+

## Description

ReasonChat+ is a reasoning-enhanced chat application that leverages the Ollama models to provide accurate, concise, and relevant answers. It uses a chain-of-thought approach to break down complex questions into manageable steps, ensuring a higher quality of response.

## Features

- **Reasoning-Enhanced Chat:** Employs a chain-of-thought process for better accuracy.
- **Ollama Integration:** Uses Ollama models for natural language processing.
- **Customizable:** Allows users to adjust temperature, model, and maximum iterations.
- **Conversation History:** Saves conversation logs for future reference.
- **Command-Line Interface:** Provides a simple and intuitive command-line interface.

## Benchmark Results

### Performance Comparison

The following benchmark illustrates the performance of ReasonChat compared to a general LLM (Large Language Model) in terms of reasoning capabilities:

![Benchmark Results](benchmark_comparison_reasonchat.png)

- **General LLM:**  
  - Performance Score: 40–50  
  - Characteristics: Standard language processing capabilities without specialized reasoning.

- **ReasonChat:**  
  - Performance Score: 80–90  
  - Characteristics: Enhanced reasoning capabilities achieved through a chain-of-thought approach, without the need for fine-tuning.

### Key Highlights

- **Reasoning Augmentation:**  
  ReasonChat utilizes a unique reasoning augmentation technique that allows it to break down complex queries into manageable steps, leading to more accurate and relevant responses.

- **No Fine-Tuning Required:**  
  Unlike traditional models that often require extensive fine-tuning for improved performance, ReasonChat achieves its results through its inherent design and reasoning process.

## Getting Started

### Prerequisites

- [Ollama](https://ollama.com/): Make sure you have Ollama installed and running.
- Python 3.6+

### Installation

1. Clone the repository:

    ```bash
    git clone [your_repository_url]
    cd ReasonChat
    ```

2. Install the required packages:

    ```bash
    pip install ollama
    ```

### Usage

Run the `Ollama.py` script:

```bash
python Ollama.py
```

Follow the prompts in the command-line interface. Type `/help` for a list of available commands.

## Commands

- `/exit`, `/quit`: Exit the application  
- `/model [name]`: Change the model (e.g., `/model llama3`)  
- `/temp [0.0-1.0]`: Set temperature  
- `/quiet`: Hide thinking process  
- `/verbose`: Show thinking process  
- `/clear`: Clear screen  
- `/history`: Show conversation history  
- `/save`: Save conversation log  
- `/iterations [2-10]`: Set maximum iterations  
- `/debug`: Show technical details  

## Configuration

*(Optional)*  
You can configure the application by modifying the `config/config.json` file or by using environment variables.

## Logging

Conversation logs are saved in the `logs/` directory.

## License

This project is licensed under the [License Name] – see the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please submit a pull request or create an issue to discuss potential changes.

## Acknowledgements

- [Ollama](https://ollama.com/)
- Other libraries or resources used

## Contact

Created by **Daniyal** — [dasif1477@gmail.com](mailto:dasif1477@gmail.com)  
For questions, feedback, or collaboration, feel free to reach out.
# ReasonChat+

## Description

ReasonChat+ is a reasoning-enhanced chat application that leverages the Ollama models to provide accurate, concise, and relevant answers. It uses a chain-of-thought approach to break down complex questions into manageable steps, ensuring a higher quality of response.

## Features

- **Reasoning-Enhanced Chat:** Employs a chain-of-thought process for better accuracy.
- **Ollama Integration:** Uses Ollama models for natural language processing.
- **Customizable:** Allows users to adjust temperature, model, and maximum iterations.
- **Conversation History:** Saves conversation logs for future reference.
- **Command-Line Interface:** Provides a simple and intuitive command-line interface.

## Benchmark Results

### Performance Comparison

The following benchmark illustrates the performance of ReasonChat compared to a general LLM (Large Language Model) in terms of reasoning capabilities:

![Benchmark Results](benchmark_comparison_reasonchat.png)

- **General LLM:**  
  - Performance Score: 40–50  
  - Characteristics: Standard language processing capabilities without specialized reasoning.

- **ReasonChat:**  
  - Performance Score: 80–90  
  - Characteristics: Enhanced reasoning capabilities achieved through a chain-of-thought approach, without the need for fine-tuning.

### Key Highlights

- **Reasoning Augmentation:**  
  ReasonChat utilizes a unique reasoning augmentation technique that allows it to break down complex queries into manageable steps, leading to more accurate and relevant responses.

- **No Fine-Tuning Required:**  
  Unlike traditional models that often require extensive fine-tuning for improved performance, ReasonChat achieves its results through its inherent design and reasoning process.

## Getting Started

### Prerequisites

- [Ollama](https://ollama.com/): Make sure you have Ollama installed and running.
- Python 3.6+

### Installation

1. Clone the repository:

    ```bash
    git clone [your_repository_url]
    cd ReasonChat
    ```

2. Install the required packages:

    ```bash
    pip install ollama
    ```

### Usage

Run the `Ollama.py` script:

```bash
python Ollama.py
```

Follow the prompts in the command-line interface. Type `/help` for a list of available commands.

## Commands

- `/exit`, `/quit`: Exit the application  
- `/model [name]`: Change the model (e.g., `/model llama3`)  
- `/temp [0.0-1.0]`: Set temperature  
- `/quiet`: Hide thinking process  
- `/verbose`: Show thinking process  
- `/clear`: Clear screen  
- `/history`: Show conversation history  
- `/save`: Save conversation log  
- `/iterations [2-10]`: Set maximum iterations  
- `/debug`: Show technical details  

## Configuration

*(Optional)*  
You can configure the application by modifying the `config/config.json` file or by using environment variables.

## Logging

Conversation logs are saved in the `logs/` directory.

## License

This project is licensed under the [License Name] – see the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please submit a pull request or create an issue to discuss potential changes.

## Acknowledgements

- [Ollama](https://ollama.com/)
- Other libraries or resources used

## Contact

Created by **Daniyal** — [dasif1477@gmail.com](mailto:dasif1477@gmail.com)  
For questions, feedback, or collaboration, feel free to reach out.
