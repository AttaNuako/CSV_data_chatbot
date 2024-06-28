import os
import pandas as pd
import openai

# Function to get the OpenAI API key from environment variables
def get_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print('OpenAI API key not found in environment variables.')
        exit()
    return api_key

# Function to generate a response using OpenAI's GPT-3.5-turbo model
def generate_response(prompt, model="gpt-3.5-turbo"):
    openai.api_key = get_openai_api_key()
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error: {e}"

# Function to read CSV data into a DataFrame
def read_csv(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        exit()

# Function to create a prompt based on user input and CSV data
def create_prompt(user_input, df):
    # You can customize this function to create a prompt based on your CSV data structure
    prompt = f"User asked: {user_input}\n"
    prompt += "Here is some related information:\n\n"
    for index, row in df.iterrows():
        prompt += f"Function: {row['Function']}, Building: {row['Building']}, Office: {row['Office']}, Office Number: {row['Office Number']}, Additional information: {row['Additional information']}\n"
    return prompt

def main():
    openai.api_key = get_openai_api_key()

    # Read CSV data
    df = read_csv("new_nsu_data.csv")

    print("Welcome to the Chatbot. Type 'exit' to end the session.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Create a prompt using the user input and CSV data
        prompt = create_prompt(user_input, df)

        # Generate response from the prompt
        response = generate_response(prompt)
        print(f"Chatbot: {response}")


if __name__ == "__main__":
    main()
