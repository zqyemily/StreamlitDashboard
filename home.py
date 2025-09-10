import streamlit as st

st.set_page_config(
    page_title="HelpDesk Dashboard Platform Home",
    page_icon="🏠",
    layout='wide'

)
st.image('img/help-logo.png', width=300)
st.write("# Welcome to HelpDesk Dashboard Platform! 🏠")

## st.sidebar.success("Select a demo above.")


st.markdown(
    """
    Pico HelpDesk Dashboard Platform is tailored for Pico's internal users to help team members visualize and analyze data effectively. It provides insights into various aspects of our operations, enabling data-driven decision-making and enhancing overall efficiency.
    ### Useful Links
    - Pico HelpDesk [helpdesk.pico.com](https://helpdesk.pico.com)
    - Pico intranet [intranet](https://picofareast.sharepoint.com/sites/intranet)
    ### Feedback and Suggestions
    - Feedback Survey [Feedback Form](https://forms.cloud.microsoft/r/Ah0guCUd30)
    ### New Demands
    - if you have any new demands, please contact Emily Zhou from HelpDesk Product Team [Emily Zhou](mailto:emily.zhou@pico.com)
"""
)
Home = st.sidebar.page_link("home.py", label="Home", icon="🏠")

dashboard_picox = st.sidebar.page_link(
    "pages/streamlit_app_picox.py", label="Pico Queue for Pico X", icon="📑"
)
dashboard_designer_sh = st.sidebar.page_link(
    "pages/streamlit_app_designer.py", label="Pico Queue for Designer Shanghai", icon="🎨"
)

