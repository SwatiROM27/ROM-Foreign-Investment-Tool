import csv
import openai
import os
from dotenv import load_dotenv
from prompts import FDI_RANKING_PROMPT, ROM_FDI_PROMPT_TEMPLATE


def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as file:
        return list(csv.DictReader(file))


def get_company_analysis(row_data):
    # Try multiple ways to get the API key
    api_key = None
    
    # Method 1: Try to load from .env file in the same directory as this script
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
            api_key = os.getenv('OPENAI_API_KEY')
    except Exception as e:
        print(f"⚠️ Warning: Could not load .env file: {e}")
    
    # Method 2: Try to get from system environment variables
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
    
    # Method 3: Fallback to hardcoded key (not recommended for production)
    if not api_key:
        print("⚠️ Warning: Using hardcoded API key. Consider setting OPENAI_API_KEY environment variable.")
        api_key = "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"
    
    if not api_key:
        raise ValueError("No OpenAI API key found. Please set OPENAI_API_KEY environment variable or check your .env file.")
    
    prompt = ROM_FDI_PROMPT_TEMPLATE.format(
        company_name=row_data.get('Firm name', ''),
        company_website=row_data.get('Company Website', ''),
        boothnr=row_data.get('Booth nr', ''),
        short_description=row_data.get('Company Summary', ''),
        industries=row_data.get('All Industries', ''),
        revenue=row_data.get('Revenue', ''),
        revenue_growth=row_data.get('Revenue growth', ''),
        employees_latest_number=row_data.get('Employees', ''),
        employees_growth=row_data.get('Employee growth % (last 12 months)', ''),
        launch_year=row_data.get('Year Founded', ''),
        company_status=row_data.get('Ownership Status', ''),
        total_funding=row_data.get('Total funding (EUR M)', ''),
        last_funding_date=row_data.get('Last funding date', ''),
        last_round=row_data.get('Last round', ''),
        last_funding_amount=row_data.get('Last funding amount', ''),
        hq_country=row_data.get('HQ Country', ''),
        hq_city=row_data.get('HQ City', ''),
        other_office_locations=row_data.get('Other office locations', ''),
        linkedin_url=row_data.get('LinkedIn URL', ''),
        number_of_patents=row_data.get('Number of patents', ''),
        in_achilles=row_data.get('In Achilles', ''),
        in_NL=row_data.get('In NL?', ''),
        provinces_and_employees=row_data.get('Provinces and Employees', ''),
        last_projects=row_data.get('Last projects', ''),
        project_teams=row_data.get('Project Teams', '')
    )

    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")
    
    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI FDI analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI API error for {row_data.get('Firm name', '')}: {e}")
        return "API_ERROR"
