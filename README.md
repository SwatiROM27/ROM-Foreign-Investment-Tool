# ROM Foreign Investment Analysis Tool

A Python-based tool for analyzing foreign direct investment (FDI) opportunities in the Utrecht Region using AI-powered company analysis.

## Overview

This tool processes trade fair participant data to identify promising candidates for establishing a presence in the Netherlands. It uses OpenAI's GPT models to analyze company information and provide insights on:

- Sector analysis and scoring
- Dutch ecosystem fit assessment
- Potential connections and partnerships in the Utrecht Region
- Investment readiness evaluation

## Features

- **AI-Powered Analysis**: Uses GPT-4 to analyze company data and provide insights
- **Comprehensive Scoring**: Evaluates companies based on multiple criteria including revenue, growth, funding, and industry fit
- **Dutch Market Focus**: Specifically targets companies suitable for the Utrecht Region ecosystem
- **Batch Processing**: Handles large datasets with progress tracking and periodic saves
- **Flexible Input**: Supports various data formats and can be easily adapted for different trade fairs

## Prerequisites

- Python 3.7+
- OpenAI API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ROMForeignInvestment/Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
python create_env.py
```
Or manually create a `.env` file with:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Place your input CSV file in the Project directory
2. Update the input file path in `main.py` if needed
3. Run the analysis:
```bash
python main.py
```

The tool will process each company and generate an enriched output CSV with AI analysis results.

## Input Data Format

The tool expects a CSV file with the following columns (among others):
- Firm name
- Company Website
- Company Summary
- Industries
- Revenue data
- Employee information
- Funding details
- Location information

## Output

The tool generates an enriched CSV file with additional columns:
- Analyzed Sector
- GPT Score
- GPT Score Explanation
- GPT Dutch Ecosystem Fit & Chain Partners
- Potential connections and partnerships in Utrecht Region
- GPT Source

## Configuration

Key configuration options can be found in:
- `prompts.py`: AI prompt templates and analysis criteria
- `ranking.py`: API configuration and data processing logic
- `main.py`: Main processing logic and file paths

## Project Structure

```
Project/
├── main.py              # Main execution script
├── ranking.py           # Company analysis and ranking logic
├── prompts.py           # AI prompt templates
├── create_env.py        # Environment setup script
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For questions or support, please contact [your contact information].

## Disclaimer

This tool is designed for internal use by ROM Utrecht Region for FDI analysis. Please ensure compliance with data protection regulations when processing company information.
