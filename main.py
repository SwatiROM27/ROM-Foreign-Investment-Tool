import csv
import re
from ranking import read_csv, get_company_analysis


def parse_markdown_row(markdown_row):
    parts = markdown_row.strip().strip("|").split("|")
    return [part.strip() for part in parts]


def main():
    input_file = "Project/IBC_2025_Complete -Dealroom and Achilles data.csv"
    output_file = "Project/output.csv"

    input_data = read_csv(input_file)

    if not input_data:
        print("No data found.")
        return

    original_headers = list(input_data[0].keys())

    gpt_fields = [
        "Analyzed Sector",
        "GPT Score",
        "GPT Score Explanation",
        "GPT Dutch Ecosystem Fit & Chain Partners",
        "Potential connections and partnerships in Utrecht Region",
        "GPT Source"
    ]

    # Insert new GPT fields after "Short description" field
    short_desc_index = None
    for i, header in enumerate(original_headers):
        if 'description' in header.lower() or 'summary' in header.lower():
            short_desc_index = i
            break
    
    if short_desc_index is not None:
        # Remove ALL existing GPT-related columns to avoid duplicates
        # This includes variations and partial matches
        original_headers_clean = []
        for col in original_headers:
            is_gpt_column = False
            for gpt_field in gpt_fields:
                # Check for exact matches and partial matches
                if (gpt_field.lower() in col.lower() or 
                    col.lower() in gpt_field.lower() or
                    any(word in col.lower() for word in ['gpt', 'score', 'sector', 'explanation', 'ecosystem', 'connections', 'source'])):
                    is_gpt_column = True
                    break
            if not is_gpt_column:
                original_headers_clean.append(col)
        

        
        reordered_headers = (
            original_headers_clean[:short_desc_index + 1] + 
            gpt_fields + 
            original_headers_clean[short_desc_index + 1:]
        )
    else:
        # Fallback: append at end if no description field found
        reordered_headers = original_headers + gpt_fields

    # Ensure clean output by removing existing file if it exists
    import os
    if os.path.exists(output_file):
        os.remove(output_file)
    
    with open(output_file, "w", newline='', encoding="utf-8-sig") as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=reordered_headers)
        writer.writeheader()

        # Store processed rows to save periodically
        processed_rows = []
        
        for idx, row in enumerate(input_data, 1):
            print(f"Processing row {idx}: {row.get('Firm name')}")
            markdown_row = get_company_analysis(row)
            print(f"AI Response for row {idx}: {markdown_row[:200]}...")

            try:
                lines = markdown_row.split('\n')
                sector = ""
                score = "N/A"
                explanation = ""
                ecosystem_fit = ""
                potential_connections = ""
                sources_details = ""

                for line in lines:
                    if line.strip().startswith('|') and '|' in line:
                        parsed = parse_markdown_row(line)
                        # Expected 9 columns per prompt: [0]=Short desc, [1]=Analyzed Sector, [2]=empty,
                        # [3]=GPT Score, [4]=Explanation, [5]=Dutch Ecosystem Fit & Chain Partners,
                        # [6]=Potential connections, [7]=empty, [8]=GPT Source
                        if len(parsed) >= 9:
                            # [0]=Short desc, [1]=Analyzed Sector, [2]=empty,
                            # [3]=GPT Score, [4]=Explanation, [5]=Dutch Ecosystem Fit & Chain Partners,
                            # [6]=Potential connections, [7]=empty, [8]=GPT Source
                            sector = parsed[1].strip()
                            score = parsed[3].strip()
                            explanation = parsed[4].strip()
                            ecosystem_fit = parsed[5].strip()
                            potential_connections = parsed[6].strip()
                            sources_details = parsed[8].strip()
                            break

                if score == "N/A":
                    score_patterns = [
                        r'score[:\s]*(\d{1,3})',
                        r'rating[:\s]*(\d{1,3})',
                        r'(\d{1,3})/100',
                        r'(\d{1,3})\s*out\s*of\s*100',
                        r'assessment[:\s]*(\d{1,3})'
                    ]
                    for line in lines:
                        for pattern in score_patterns:
                            match = re.search(pattern, line.lower())
                            if match:
                                score_val = int(match.group(1))
                                if 0 <= score_val <= 100:
                                    score = str(score_val)
                                    break
                        if score != "N/A":
                            break

                    meaningful_lines = []
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('|') and not line.startswith('ANALYSIS:') and len(line) > 20:
                            meaningful_lines.append(line)
                            if len(meaningful_lines) >= 3:
                                break
                    if meaningful_lines:
                        explanation = ' '.join(meaningful_lines)
                        words = explanation.split()
                        if len(words) > 100:
                            explanation = ' '.join(words[:100]) + "..."

                    dutch_mentions = [
                        line.strip() for line in lines
                        if any(word in line.lower() for word in ['dutch', 'netherlands', 'amsterdam', 'rotterdam', 'eindhoven'])
                    ]
                    if dutch_mentions:
                        ecosystem_fit = ' '.join(dutch_mentions[:2])
                        words = ecosystem_fit.split()
                        if len(words) > 100:
                            ecosystem_fit = ' '.join(words[:100]) + "..."
                    else:
                        ecosystem_fit = "No specific Dutch market mention found"

                    # Extract sources details from text if not found in table
                    if not sources_details:
                        sources_mentions = []
                        for line in lines:
                            if any(word in line.lower() for word in ['linkedin', 'website', 'news', 'source', 'patent', 'trade', 'industry', 'regulatory', 'publication', 'database', 'project', 'accelerator', 'portxl', 'buccaneer', 'horizon', 'interreg', 'emsa', 'imo']):
                                sources_mentions.append(line.strip())
                        
                        if sources_mentions:
                            sources_details = ' '.join(sources_mentions[:4])  # Take up to 4 sources
                            if len(sources_details) > 250:
                                sources_details = sources_details[:250] + "..."
                        else:
                            sources_details = "No specific sources mentioned"

                enriched_row = {
                    **row,
                    gpt_fields[0]: sector,
                    gpt_fields[1]: score,
                    gpt_fields[2]: explanation,
                    gpt_fields[3]: ecosystem_fit,
                    gpt_fields[4]: potential_connections,
                    gpt_fields[5]: sources_details
                }

                ordered_row = {field: enriched_row.get(field, "") for field in reordered_headers}
                processed_rows.append(ordered_row)
                
                # Save progress every 5 companies
                if idx % 5 == 0:
                    print(f"💾 Saving progress after {idx} companies...")
                    # Write all processed rows to file
                    with open(output_file, "w", newline='', encoding="utf-8-sig") as temp_csv:
                        temp_writer = csv.DictWriter(temp_csv, fieldnames=reordered_headers)
                        temp_writer.writeheader()
                        temp_writer.writerows(processed_rows)
                    print(f"✅ Progress saved! {idx}/{len(input_data)} companies completed.")

            except Exception as e:
                print(f"❌ Failed to process row {idx}: {e}")
                continue
        
        # Final save - write all processed rows
        print(f"💾 Final save - writing all {len(processed_rows)} companies to output file...")
        with open(output_file, "w", newline='', encoding="utf-8-sig") as final_csv:
            final_writer = csv.DictWriter(final_csv, fieldnames=reordered_headers)
            final_writer.writeheader()
            final_writer.writerows(processed_rows)
        print(f"🎉 All done! Output saved to {output_file}")


if __name__ == "__main__":
    main()
