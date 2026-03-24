import streamlit as st
import json
import os

st.set_page_config(page_title="Military Vehicle Catalogue", layout="wide")


@st.cache_data
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            return json.load(f)
    return {}


def render_section_dict(title, data_dict):
    if data_dict:
        st.markdown(f"**{title}**")
        for key, value in data_dict.items():
            st.markdown(f"- **{key}:** {value}")
        st.write("")  # Spacer


def render_section_list(title, data_list):
    if data_list:
        st.markdown(f"**{title}**")
        for item in data_list:
            st.markdown(f"- {item}")
        st.write("")  # Spacer


def main():
    st.title("🛡️ RP Military Vehicle Catalogue")

    data = load_data()

    if not data:
        st.warning("No data found. Please run the local manager script to add companies and vehicles.")
        return

    # Sidebar for Company Selection
    companies = list(data.keys())
    selected_company = st.sidebar.selectbox("Select a Company", companies)

    st.header(selected_company)
    company_data = data[selected_company]

    # Tabs for Domains
    tab_naval, tab_land, tab_air = st.tabs(["⚓ Naval", "🪖 Land", "✈️ Air"])

    domains = [
        ("Naval", tab_naval),
        ("Land", tab_land),
        ("Air", tab_air)
    ]

    for domain_name, tab in domains:
        with tab:
            vehicles = company_data.get(domain_name, [])
            if not vehicles:
                st.info(f"No {domain_name.lower()} vehicles available for {selected_company}.")
                continue

            # Display vehicles in expanders to keep the UI clean
            for vehicle in vehicles:
                with st.expander(vehicle.get("Name", "Unnamed Vehicle"), expanded=False):
                    col1, col2 = st.columns(2)

                    with col1:
                        render_section_dict("Cost and Build Time", vehicle.get("Cost and Build Time", {}))

                        # Domain specific specs
                        if domain_name == "Naval":
                            render_section_dict("Vessel Specs", vehicle.get("Vessel Specs", {}))
                            render_section_list("Aircraft Carried", vehicle.get("Aircraft Carried", []))
                        elif domain_name == "Land":
                            render_section_dict("Vehicle Specs", vehicle.get("Vehicle Specs", {}))
                            render_section_list("Drones Carried", vehicle.get("Drones Carried", []))
                        elif domain_name == "Air":
                            render_section_dict("Dimensions & Capacity", vehicle.get("Dimensions & Capacity", {}))
                            render_section_dict("Performance", vehicle.get("Performance", {}))
                            render_section_list("Drones Carried", vehicle.get("Drones Carried", []))

                    with col2:
                        render_section_list("Weapons", vehicle.get("Weapons", []))
                        render_section_list("Systems", vehicle.get("Systems", []))


if __name__ == "__main__":
    main()