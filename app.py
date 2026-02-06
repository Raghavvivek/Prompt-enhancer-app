import streamlit as st
from openai import OpenAI

# ----------------------------
# Streamlit Page Configuration
# ----------------------------
st.set_page_config(page_title="Prompt Enhancer App", layout="centered")

st.title("🧠 Raghav's Prompt Enhancer App")
st.write("Improve your prompt before sending it to GPT")

# ----------------------------
# Secure API Key Input
# ----------------------------
api_key = st.text_input(
    "Enter your OpenAI API Key",
    type="password",
    help="Your key is used only for this session"
)

# ----------------------------
# User Inputs
# ----------------------------
role = st.text_area("Role", placeholder="e.g. You are an experienced Python developer")
context = st.text_area("Context", placeholder="e.g. I am a beginner learning AI for coding")
task = st.text_area("Task", placeholder="e.g. Help me build a Streamlit app")

# ----------------------------
# Button
# ----------------------------
if st.button("Enhance Prompt"):

    if not api_key:
        st.error("Please enter your OpenAI API key")
    elif not role or not context or not task:
        st.error("Please fill all inputs")
    else:
        try:
            # Initialize OpenAI Client
            client = OpenAI(api_key=api_key)

            # ----------------------------
            # System Prompt
            # ----------------------------
            system_prompt = """
            You are an expert prompt engineer.
            Your job is to improve the given prompt.
            DO NOT answer the task.
            The enhanced prompt must:
            - Be clear and structured
            - Explicitly instruct GPT to clarify assumptions before responding
            - Ask clarifying questions if needed
            - Be suitable for high-quality GPT output
            """

            user_prompt = f"""
            Role:
            {role}

            Context:
            {context}

            Task:
            {task}
            """

            # ----------------------------
            # OpenAI API Call
            # ----------------------------
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            enhanced_prompt = response.choices[0].message.content

            # ----------------------------
            # Output Formats
            # ----------------------------
            st.subheader("✅ Enhanced Prompt (Plain Text)")
            st.code(enhanced_prompt)

            st.subheader("📄 Enhanced Prompt (XML)")
            xml_output = f"""
<prompt>
  <role>{role}</role>
  <context>{context}</context>
  <task>
    {enhanced_prompt}
  </task>
</prompt>
"""
            st.code(xml_output, language="xml")

            st.subheader("🧾 Enhanced Prompt (JSON)")
            json_output = {
                "role": role,
                "context": context,
                "enhanced_prompt": enhanced_prompt
            }
            st.json(json_output)

        except Exception as e:
            st.error(f"Something went wrong: {e}")