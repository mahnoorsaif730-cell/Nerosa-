import streamlit as st
import rag


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="MediSense AI",
    page_icon="💊",
    layout="centered"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #666666;
        margin-bottom: 30px;
    }

    .info-card {
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #dddddd;
        margin-top: 20px;
        background-color: #ffffff;
    }

    .safety-card {
        padding: 16px;
        border-radius: 12px;
        margin-top: 18px;
        background-color: #fff7e6;
        border-left: 5px solid #f0a000;
    }

    .source-card {
        padding: 14px;
        border-radius: 12px;
        margin-top: 15px;
        background-color: #f5f7fa;
    }

    .disclaimer-card {
        padding: 16px;
        border-radius: 12px;
        margin-top: 25px;
        background-color: #f1f1f1;
        color: #555555;
        font-size: 14px;
    }

    .footer {
        text-align: center;
        color: #888888;
        font-size: 13px;
        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">💊 MediSense AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Assisted Medicine Information Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Enter a medicine name to receive clear, simple and "
    "educational information."
)


# ---------------------------------------------------------
# SEARCH INPUT
# ---------------------------------------------------------

user_input = st.text_input(
    "🔎 Search for a medicine",
    placeholder="Example: Paracetamol"
)


# ---------------------------------------------------------
# SEARCH BUTTON
# ---------------------------------------------------------

if st.button(
    "🔍 Search Medicine",
    use_container_width=True
):

    if not user_input.strip():

        st.warning(
            "Please enter a medicine name first."
        )

    else:

        try:

            result = rag.retrieve_info(user_input)

            # -------------------------------------------------
            # MEDICINE FOUND
            # -------------------------------------------------

            if result:

                st.success(
                    f"Medicine found: {result['medicine_name']}"
                )

                st.markdown(
                    '<div class="info-card">',
                    unsafe_allow_html=True
                )

                st.subheader(
                    f"💊 {result['medicine_name']}"
                )

                st.write(
                    f"**Drug Type:** "
                    f"{result['drug_type']}"
                )

                st.write(
                    f"**Main Use:** "
                    f"{result['main_use']}"
                )

                st.write(
                    f"**Common Forms:** "
                    f"{result['common_forms']}"
                )

                # -------------------------------------------------
                # SAFETY INFORMATION
                # -------------------------------------------------

                st.markdown(
                    f"""
                    <div class="safety-card">
                        <b>⚠️ Important Safety Note</b>
                        <br><br>
                        {result['safety_note']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # -------------------------------------------------
                # SOURCE
                # -------------------------------------------------

                if result["source_reference"]:

                    st.markdown(
                        f"""
                        <div class="source-card">
                            <b>📚 Source Reference</b>
                            <br><br>
                            {result['source_reference']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

                # -------------------------------------------------
                # DISCLAIMER
                # -------------------------------------------------

                st.markdown(
                    """
                    <div class="disclaimer-card">
                        <b>⚕️ Educational Disclaimer</b>
                        <br><br>
                        This tool provides general educational
                        information only. It does not diagnose
                        medical conditions, prescribe medicines,
                        recommend personalized treatment, or
                        replace advice from a qualified healthcare
                        professional.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # -------------------------------------------------
            # MEDICINE NOT FOUND
            # -------------------------------------------------

            else:

                st.error(
                    "Medicine not found in the current reference dataset."
                )

                st.info(
                    "Please check the spelling and try again."
                )

        except Exception as error:

            st.error(
                "Sorry, the medicine information could not "
                "be loaded."
            )

            st.caption(
                f"System message: {error}"
            )


# ---------------------------------------------------------
# AVAILABLE MEDICINES
# ---------------------------------------------------------

with st.expander("📋 View reference medicines"):

    try:

        medicines = rag.get_all_medicines()

        if medicines:

            for medicine in medicines:

                st.write(
                    f"• {medicine['medicine_name']}"
                )

        else:

            st.write(
                "No medicines are currently available."
            )

    except Exception as error:

        st.warning(
            "The medicine list could not be loaded."
        )

        st.caption(
            f"System message: {error}"
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        MediSense AI • Hackathon MVP<br>
        AI-Assisted Educational Medicine Information
    </div>
    """,
    unsafe_allow_html=True
)
