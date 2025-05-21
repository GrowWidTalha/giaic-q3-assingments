import streamlit as st
import re
st.set_page_config(page_title="Password Strength Checker", page_icon="🔒")
st.title("🔐Password Strength Checker")
st.markdown("""
            ## Welcome to the ultimate password checker!👋
use this tool to check the strength of your password and get suggestion on how to make it stronger.
               we will give helpful tips to create a **Strong Password**🔒""")

password = st.text_input("Enter your password",type="password")

feedback = []

score = 0

if password:
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌Password should be 8 characters long")

        if re.search(r'[A-Z]',password) and re.search(r'[a-z]',password):
             score+=1
        else:
          feedback.append("❌Password should contain both upper case and lower case characters.")

          if re.search(r'[0-9]', password):
              score += 1
          else:
              feedback.append("❌Password should be contain atleast 1 digit")

              if re.search(r'[!@#$%*]',password):
                  score += 1
              else:
                feedback.append("❌Password should be contain atleast 1 Special character(!@#$%*).")

                if score == 4:
                 feedback.append("🟢Your Password id Strong!🎉")
                elif score==3:
                   feedback.append("🟡Your Password is medium Strength. it Could be stronger.")
                else:
                   feedback.append("Your Password is weak. please make it Strong.")

                   if feedback:
                      st.markdown("## Improvement Suggestion")
                      for tip in feedback:
                         st.write(tip)

else:
   st.info("Please enter your Password to get Started.")