import google.generativeai as genai
import os


def setup_stem_advisor():
    """
    Sets up a specialized STEM career guidance chatbot
    """
    GOOGLE_API_KEY = ""
    genai.configure(api_key=GOOGLE_API_KEY)

    # Initialize the model
    model = genai.GenerativeModel('gemini-pro')

    # Define the context and role
    context = """You are a supportive STEM career advisor specifically focused on helping young women 
    in developing countries explore and pursue careers in Science, Technology, Engineering, and Mathematics. 
    Your guidance should:
    - Be encouraging and empowering
    - Consider common challenges in developing regions (limited resources, internet access, etc.)
    - Provide practical advice about educational paths
    - Suggest local and online learning resources
    - Share stories of successful women in STEM from similar backgrounds
    - Include information about scholarships and educational opportunities
    - Address cultural and social considerations respectfully
    - Focus on both traditional and emerging STEM careers
    - Provide guidance on building support networks
    """

    # Start chat with context
    chat = model.start_chat(history=[
        {
            "role": "user",
            "parts": [context]
        },
        {
            "role": "model",
            "parts": [
                "I understand my role as a STEM career advisor for young women in developing countries. I'm ready to provide guidance."]
        }
    ])

    return chat


def provide_stem_guidance():
    """
    Run an interactive STEM career guidance session
    """
    chat = setup_stem_advisor()

    # Initial welcome message
    welcome_message = """
    Welcome to your STEM Career Advisor! 👋
    I'm here to help you explore exciting careers in Science, Technology, Engineering, and Mathematics.

    You can ask me about:
    - Different STEM careers
    - Educational paths and requirements
    - Scholarships and opportunities
    - Success stories of women in STEM
    - How to overcome challenges
    - Study tips and resources

    What would you like to know about pursuing a STEM career?

    Type 'quit' when you're done.
    """
    print(welcome_message)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == 'quit':
            print("\nGoodbye! Remember, you have the potential to achieve great things in STEM! 💫")
            break

        try:
            # Get response from the chatbot
            response = chat.send_message(user_input)
            print("\nAdvisor:", response.text, "\n")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


def suggest_stem_resources():
    """
    Returns a list of STEM learning resources suitable for developing countries
    """
    resources = {
        "Online Learning Platforms": [
            "Khan Academy (free, works offline)",
            "MIT OpenCourseWare",
            "UNESCO's STEM Education for Girls"
        ],
        "Mobile Apps": [
            "Brilliant (works offline)",
            "Google Grasshopper (coding)",
            "Physics 101"
        ],
        "Organizations": [
            "African Women in Science and Engineering",
            "Women Who Code",
            "TechWomen"
        ],
        "Scholarship Information": [
            "Mastercard Foundation Scholars Program",
            "UNESCO Prize for Girls' and Women's Education",
            "Study.com Academic Scholarships"
        ]
    }
    return resources


if __name__ == "__main__":
    provide_stem_guidance()
