import streamlit as st
from bank import Bank

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Piggy Bank",
    page_icon="🐷",
    layout="wide"
)

bank = Bank()

# ================= CUSTOM CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.big-title {
    font-size: 60px;
    font-weight: 700;
    text-align: center;
    # background: -webkit-linear-gradient(#00f5d4, #9b5de5);
    # -webkit-background-clip: text;/
    # -webkit-text-fill-color: transparent;
}

.tagline {
    text-align: center;
    font-size: 20px;
    color: #bbbbbb;
    margin-top: -20px;
}

.glass-card {
    background: rgba(255, 255, 255, 0.08);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    margin-bottom: 20px;
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-weight: 600;
    background: linear-gradient(90deg, #00f5d4, #9b5de5);
    color: black;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #9b5de5, #00f5d4);
    color: black;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown('<div class="big-title">🐷 Piggy Bank</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">21 din mein paisa half 💰</div>', unsafe_allow_html=True)
st.write("")

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= SIDEBAR =================
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🆕 Create Account", "🔐 Login", "🗑 Delete Account"]
)

# ================= HOME =================
if menu == "🏠 Home":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Welcome to the Future of Banking 🚀")
    st.write("""
    Piggy Bank is not just a bank.  
    It’s an emotion. A vibe. A financial revolution.

    Save smart. Grow faster.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= CREATE ACCOUNT =================
elif menu == "🆕 Create Account":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1)
    email = st.text_input("Email")
    pin = st.number_input("4 Digit PIN", min_value=1000, max_value=9999)
    phone = st.text_input("Phone Number")

    if st.button("🚀 Create My Piggy Account"):
        success, result = bank.create_account(name, age, email, pin, phone)

        if success:
            st.success(f"Account Created Successfully 🎉\n\nAccount No: {result}")
            st.balloons()
        else:
            st.error(result)

    st.markdown('</div>', unsafe_allow_html=True)

# ================= LOGIN =================
elif menu == "🔐 Login":

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    acc_no = st.text_input("Account Number")
    pin = st.number_input("PIN", min_value=1000, max_value=9999)

    if st.button("🔓 Enter Piggy World"):
        user = bank.authenticate(acc_no, pin)
        if user:
            st.session_state.user = user
        else:
            st.error("Invalid Credentials ❌")

    # ================= LOGGED IN DASHBOARD =================
    if st.session_state.user:
        user = st.session_state.user
        st.success(f"Welcome back, {user['name']} 🐷")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("💰 Current Balance", f"₹ {user['balance']}")

        action = st.selectbox(
            "Choose Action",
            ["Deposit", "Withdraw", "Update Profile"]
        )

        amount = st.number_input("Enter Amount", min_value=0)

        # ---------- DEPOSIT ----------
        if action == "Deposit":
            if st.button("💸 Deposit"):
                success, msg = bank.deposit(user, amount)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        # ---------- WITHDRAW ----------
        elif action == "Withdraw":
            if st.button("🏧 Withdraw"):
                success, msg = bank.withdraw(user, amount)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        # ---------- UPDATE PROFILE ----------
        elif action == "Update Profile":

            st.subheader("📝 Update Your Profile")

            new_name = st.text_input("Full Name", value=user["name"])
            new_age = st.number_input("Age", min_value=1, value=user["age"])
            new_email = st.text_input("Email", value=user["email"])
            new_pin = st.number_input(
                "4 Digit PIN",
                min_value=1000,
                max_value=9999,
                value=user["pin"]
            )
            new_phone = st.text_input(
                "Phone Number",
                value=str(user["phone"])
            )

            if st.button("💾 Save Changes"):
                success, msg = bank.update_account(
                    user,
                    new_name,
                    new_age,
                    new_email,
                    new_pin,
                    new_phone
                )

                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ================= DELETE ACCOUNT =================
elif menu == "🗑 Delete Account":

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    acc_no = st.text_input("Account Number")
    pin = st.number_input("PIN", min_value=1000, max_value=9999)

    if st.button("⚠ Permanently Delete"):
        user = bank.authenticate(acc_no, pin)
        if user:
            bank.delete_account(user)
            st.success("Account Deleted Successfully 🗑️")
        else:
            st.error("Invalid Credentials")

    st.markdown('</div>', unsafe_allow_html=True)