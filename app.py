import streamlit as st
import pandas as pd
import networkx as nx
from graphviz import Digraph

# Load the CSV files and preprocess data
@st.cache_data
def load_data():
    # Load Protein data
    protein_df = pd.read_csv('Protein.csv')
    # Load Recipe data
    recipe_df = pd.read_csv('recipe.csv')
    
    # Remove quotes and convert columns in Protein data
    for column in protein_df.columns:
        if protein_df[column].apply(lambda x: isinstance(x, str) and x.startswith('"') and x.endswith('"')).all():
            protein_df[column] = protein_df[column].str.replace('"', '')
        try:
            protein_df[column] = pd.to_numeric(protein_df[column])
        except ValueError:
            pass
        if pd.api.types.is_numeric_dtype(protein_df[column]) and (protein_df[column] % 1 == 0).all():
            protein_df[column] = protein_df[column].astype(int)
    
    # Remove quotes and convert columns in Recipe data
    for column in recipe_df.columns[recipe_df.columns.get_loc('directions')+1:]:  # Select columns after 'directions'
        if recipe_df[column].apply(lambda x: isinstance(x, str) and x.startswith('"') and x.endswith('"')).all():
            recipe_df[column] = recipe_df[column].str.replace('"', '')
        try:
            recipe_df[column] = pd.to_numeric(recipe_df[column])
        except ValueError:
            pass
    
    return protein_df, recipe_df

# Function to create a knowledge graph
def create_knowledge_graph(df, recipe_id):
    filtered_df = df[df['recipe_id'] == recipe_id]
    if filtered_df.empty:
        return None, "No data found for the given recipe ID."

    G = nx.DiGraph()
    central_node = filtered_df['replaced_food_name'].iloc[0].strip()

    for _, row in filtered_df.iterrows():
        target = row['substitute_food_name'].strip()
        quantity = row['substitute_food_quantity']
        G.add_edge(central_node, target, weight=quantity)
    
    return G, None

# Function to plot the knowledge graph
def render_graph(G):
    dot = Digraph()
    for node in G.nodes():
        dot.node(node, node, href=f"#", onclick=f"handleNodeClick('{node}')")
    for edge in G.edges(data=True):
        dot.edge(edge[0], edge[1], label=str(edge[2]['weight']))

    dot.attr('graph', concentrate='true')

    return dot.source

def streamlit_node_click(message):
    if message['event'] == 'node_click':
        clicked_node_id = message['node_id']
        st.sidebar.write(f"Clicked node: {clicked_node_id}")
        
def main():
    st.title('Protein Knowledge Graph Dashboard')

    # Load data
    protein_data, recipe_data = load_data()

    # Selection field for recipe name
    recipe_names = protein_data['recipe_name'].unique()
    selected_recipe_name = st.selectbox('Select Recipe:', recipe_names)

    # Get corresponding recipe_id
    recipe_id = protein_data[protein_data['recipe_name'] == selected_recipe_name]['recipe_id'].iloc[0]

    # Display recipe details
    selected_recipe_details = recipe_data[recipe_data['recipe_title'] == selected_recipe_name]['directions'].iloc[0]
    st.text_area('Recipe Details:', selected_recipe_details, height=200)

    # Display nutritional values table
    st.subheader('Total Nutritional Values:')
    selected_recipe_nutrition = recipe_data[recipe_data['recipe_title'] == selected_recipe_name].iloc[0]
    nutritional_values = selected_recipe_nutrition[selected_recipe_nutrition.index[selected_recipe_nutrition.index.get_loc('directions')+1:]]
    st.table(nutritional_values)

    G, error_message = create_knowledge_graph(protein_data, recipe_id)

    if error_message:
        st.error(error_message)
        return

    if G is not None:
        dot_source = render_graph(G)
        st.graphviz_chart(dot_source)

        with open('scripts.js', 'r', encoding='utf-8') as f:
            js_code = f.read()

        st.markdown(
            """
            <script type="text/javascript">
            {}
            </script>
            """.format(js_code),
            unsafe_allow_html=True,
        )

        if 'node_click' not in st.session_state:
            st.session_state.node_click = None

        if st.session_state.node_click:
            streamlit_node_click(st.session_state.node_click)

if __name__ == '__main__':
    main()
