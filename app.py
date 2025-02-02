import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Initialize the LLM with Groq API
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key="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"  # Replace with your actual Groq API key
)

# Define the updated investment strategy prompt template
prompt_template_investment = PromptTemplate.from_template(
    """
    User inputs:
- Financial Goals: {financial_goals}
- Risk Tolerance: {risk_tolerance}
- Investment Capacity: ₹{investment_capacity}
- Expenses: ₹{expenses}
- Income: ₹{income}
- Age: {age}
- Retirement Age: {retirement_age}
- Expected Return: {expected_return}
- Required Corpus: ₹{corpus}
- Existing Assets: {assets}
- Existing Investments: {existing_investments}
    You are a professional financial AI advisor. Based on the given user inputs, provide a personalized investment strategy. 
        keep in mind the finacial goals of the person and the time frame he has given himself for it.Other than his own retirement if he need s a sum of money for any reason by a time then make sure to mention what to do for that person.

The response should roughly be like this format make sure that this is the u give like best option mention and all the bestion should add up to the amount he will invest:

**Investment Strategy **  This is just a rough frame work if he wnats someting llike real estate add that too 
- **Risk Tolerance:** (Conservative / Moderate / Aggressive)  also if he is young he can take maore risk then some one who is old
- **Investment Plan:**  
  - **Stocks (X%)**  Divide the stocks into **Small Cap**, **Mid Cap**, and **Large Cap** categories as applicable. For each and you can have more than 1 if a person s looing towards any like specific stocks like tech or pharma then make sure to add them
      - [Stock Name] ([Category]) – ₹[Amount] (CAGR: X%)  
  - **Mutual Funds (X%)**  
    - [Mutual Fund Name] – ₹[Amount] SIP/Lump Sum (CAGR: X%). Include recommendations for quant funds if the user is interested.
  - **Fixed Deposits (X%)**  
    - [Bank Name] – ₹[Amount] (Interest: X%). Omit this section if the user specifies 'no fd' in their inputs.
  - **Crypto (X%)** (if he said ok)  
    - [Crypto Name] – ₹[Amount]  
  - **Government Schemes (X%)**  
    - [Scheme Name] – ₹[Amount] (Interest: X%)  
**Additional Advice:**  
- [Investment strategy recommendations] This is the most important part explaining your choice in each and telling when and how u should take your money out and when yu should put money in to complete the goals aslo mention a berif time line of like stuff


"""
)


# Function to generate investment recommendations using the prompt template
def generate_investment_plan(user_inputs):
    try:
        chain_investment = prompt_template_investment | llm
        result_investment = chain_investment.invoke(input={
            'financial_goals': user_inputs['financial_goals'],
            'risk_tolerance': user_inputs['risk_tolerance'],
            'investment_capacity': user_inputs['investment_capacity'],
            'expenses': user_inputs['expenses'],
            'income': user_inputs['income'],
            'age': user_inputs['age'],
            'retirement_age': user_inputs['retirement_age'],
            'expected_return': user_inputs['expected_return'],
            'corpus': user_inputs['corpus_required'],
            'assets': user_inputs['owned_assets'],
            'existing_investments': user_inputs['specific_investments']
        })
        investment_output = result_investment.content
        return investment_output
    except Exception as e:
        return f"Error during investment plan generation: {str(e)}"


# Streamlit UI following your provided design
def main():
    st.set_page_config(page_title="Personalized Investment Advisor", layout="centered")

    st.title("Personalized Investment Portfolio Advisor")
    st.write("Fill in your details to get a personalized investment strategy.")

    # User Inputs
    age = st.number_input("Your Age", min_value=0, max_value=100, value=30)
    retirement_age = st.number_input("Expected Retirement Age", min_value=age, max_value=100, value=60)
    expected_return = st.number_input("Expected Annual Return (%)", min_value=1.0, max_value=50.0, value=8.0)

    income = st.number_input("Monthly Income (INR)", min_value=0, value=50000)
    expenses = st.number_input("Monthly Expenses (INR)", min_value=0, value=20000)
    investment_capacity = st.number_input("How much can you invest per month? (INR)", min_value=0, value=10000)
    corpus_required = st.number_input("Target Corpus Amount for Retirement (INR)", min_value=0, value=10000000)

    risk_tolerance = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])
    risky_assets = st.checkbox("Interested in high-risk investments like Crypto?")

    # Persistent session state storage for text inputs
    if "financial_goals" not in st.session_state:
        st.session_state.financial_goals = ""
    if "owned_assets" not in st.session_state:
        st.session_state.owned_assets = ""
    if "specific_investments" not in st.session_state:
        st.session_state.specific_investments = ""

    st.session_state.financial_goals = st.text_area("What are your financial goals?", st.session_state.financial_goals)
    st.session_state.owned_assets = st.text_area("What assets do you own?", st.session_state.owned_assets)
    st.session_state.specific_investments = st.text_area(
        "Which investment plans do you already use, and which ones do you want to change (e.g., specific stocks)?",
        st.session_state.specific_investments)

    if st.button("Generate Investment Plan"):
        st.write("Processing your data...")
        # Combine inputs into a dictionary for the prompt template
        user_inputs = {
            "financial_goals": st.session_state.financial_goals,
            "age": age,
            "retirement_age": retirement_age,
            "expected_return": expected_return,
            "income": income,
            "expenses": expenses,
            "investment_capacity": investment_capacity,
            "corpus_required": corpus_required,
            "risk_tolerance": risk_tolerance,
            "owned_assets": st.session_state.owned_assets,
            "specific_investments": st.session_state.specific_investments
        }

        investment_plan = generate_investment_plan(user_inputs)
        st.subheader("Generated Investment Plan")
        with st.expander("View Investment Plan", expanded=True):
            st.markdown(investment_plan, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
