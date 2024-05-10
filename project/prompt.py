system_message = "You are an expert text summarizer."


def generate_prompt(company):
    prompt = f"""
    Provide a concise summary of the most critical information from this 10-K filing that would be important for traders. Focus on financial performance, liquidity, market trends, risk factors, and any strategic initiatives that might impact the company's stock price in the short to medium term.

    Here is the 10-k filing:
    {company}
    """
    return prompt
