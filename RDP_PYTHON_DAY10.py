# start=1
# end=7
#
# while start<=end:
#     print("start",start)
#     if start==3:
#         print("start inside if",start)
#         start = start + 1
#         continue
#     elif start==5:
#         print("start inside elif",start)
#         break
#     else:
#         start=start+1
#     print("We are outside of while loop...")
#
#


import streamlit as st
from datetime import datetime
from functools import reduce
from operator import mul

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Smart Calculator",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp {
        background-color: #F4F7FB;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #172554;
        text-align: center;
    }

    .subtitle {
        text-align: center;
        color: #64748B;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .result-card {
        background: linear-gradient(135deg, #1D4ED8, #6366F1);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-top: 20px;
    }

    .result-label {
        font-size: 16px;
        opacity: 0.9;
    }

    .result-value {
        font-size: 36px;
        font-weight: bold;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] {
        background-color: #E8EEF9;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

if "expression" not in st.session_state:
    st.session_state.expression = ""


# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🧮 Smart Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'A simple and powerful calculator for your everyday calculations'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚙️ Calculator Settings")

    operator = st.radio(
        "Select Operation",
        ["Addition (+)", "Subtraction (-)",
         "Multiplication (*)", "Division (/)"],
        index=0
    )

    st.divider()

    st.markdown("### 📌 Instructions")
    st.write("1. Select an operation.")
    st.write("2. Enter the required values.")
    st.write("3. Click Calculate.")
    st.write("4. View your result.")

    st.divider()

    st.markdown("### 📊 Total Calculations")
    st.metric("Calculations performed", len(st.session_state.history))


# ---------------- MAIN CALCULATOR ----------------
st.subheader("Perform Your Calculation")

col1, col2 = st.columns([1, 1])

result = None
expression = ""

with st.form("calculator_form"):

    if operator in ["Addition (+)", "Multiplication (*)"]:

        st.info("Enter multiple numbers separated by commas.")

        values = st.text_input(
            "Enter your values",
            placeholder="Example: 10, 20, 30, 40"
        )

    else:

        col1, col2 = st.columns(2)

        with col1:
            val1 = st.number_input(
                "Enter first value",
                value=0.0,
                format="%.6f"
            )

        with col2:
            val2 = st.number_input(
                "Enter second value",
                value=0.0,
                format="%.6f"
            )

    calculate = st.form_submit_button(
        "🚀 Calculate",
        type="primary"
    )


# ---------------- CALCULATION LOGIC ----------------
if calculate:

    try:

        if operator == "Addition (+)":

            if not values.strip():
                st.error("Please enter at least one value.")

            else:
                converted_values = [
                    float(v.strip())
                    for v in values.split(",")
                ]

                if not all(v == v and abs(v) != float("inf")
                           for v in converted_values):
                    raise ValueError("Please enter finite numbers.")

                result = sum(converted_values)

                expression = " + ".join(map(str, converted_values))

        elif operator == "Subtraction (-)":

            result = val1 - val2

            expression = f"{val1} - {val2}"

            reverse_result = val2 - val1

        elif operator == "Multiplication (*)":

            if not values.strip():
                st.error("Please enter at least one value.")

            else:
                converted_values = [
                    float(v.strip())
                    for v in values.split(",")
                ]

                if not all(v == v and abs(v) != float("inf")
                           for v in converted_values):
                    raise ValueError("Please enter finite numbers.")

                result = reduce(mul, converted_values, 1)

                expression = " × ".join(map(str, converted_values))

        elif operator == "Division (/)":

            if val2 == 0:
                st.error("You cannot divide by zero!")

            else:
                result = val1 / val2

                expression = f"{val1} ÷ {val2}"

        # Store successful calculations
        if result is not None:

            st.session_state.result = result
            st.session_state.expression = expression

            st.session_state.history.insert(
                0,
                {
                    "Time": datetime.now().strftime("%H:%M:%S"),
                    "Operation": operator,
                    "Expression": expression,
                    "Result": result
                }
            )

            st.success("Calculation completed successfully!")

            if operator == "Subtraction (-)":
                st.info(
                    f"Reverse subtraction: "
                    f"{val2} - {val1} = {reverse_result}"
                )

    except ValueError:
        st.error(
            "Invalid input! Please enter valid numbers "
            "separated by commas."
        )

    except OverflowError:
        st.error("The calculation result is too large.")

    except Exception as e:
        st.error(f"Something went wrong: {e}")


# ---------------- RESULT DISPLAY ----------------
if st.session_state.result is not None:

    st.markdown(f"""
        <div class="result-card">
            <div class="result-label">YOUR CALCULATION RESULT</div>
            <div class="result-value">
                {st.session_state.result:,.6f}
            </div>
            <div>{st.session_state.expression}</div>
        </div>
    """, unsafe_allow_html=True)


# ---------------- CALCULATION HISTORY ----------------
st.divider()

st.subheader("📜 Calculation History")

if st.session_state.history:

    st.dataframe(
        st.session_state.history,
        use_container_width=True,
        hide_index=True
    )

    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.session_state.result = None
        st.session_state.expression = ""
        st.rerun()

else:
    st.info("No calculation history available yet.")


# ---------------- FOOTER ----------------
st.divider()

st.markdown(
    "<center style='color:gray;'>"
    "Smart Calculator | Built with Python & Streamlit"
    "</center>",
    unsafe_allow_html=True
)
