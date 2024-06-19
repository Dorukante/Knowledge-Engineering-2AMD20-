// Function to handle node clicks
function handleNodeClick(nodeId) {
    const clickedNode = document.getElementById(nodeId);
    if (clickedNode) {
        const currentColor = clickedNode.getAttribute('fill');
        if (currentColor !== 'yellow') {
            clickedNode.setAttribute('fill', 'yellow');
        } else {
            clickedNode.setAttribute('fill', 'white');
        }
        // Send clicked node ID back to Streamlit
        const clickedNodeId = nodeId.split('_')[1]; // Extract node ID
        const message = {'event': 'node_click', 'node_id': clickedNodeId};
        parent.postMessage(message, '*'); // Send message to parent (Streamlit)
    }
}

