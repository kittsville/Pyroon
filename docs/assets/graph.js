$.getJSON("/graph.json", function(json) {
	cy = cytoscape({
		
		container: document.getElementById('graph'),
		
		elements: json.graph,

		layout: {
			name: 'dagre'
		},
		
		wheelSensitivity: 0.1,

		// so we can see the ids etc
		style: [
			{
				selector: 'node',
				style: {
					'content': 'data(text)'
				}
			}
		]
	});
	
	document.getElementById('wrap').removeChild(document.getElementById('loading'));
});
