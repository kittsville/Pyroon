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
					'content': 'data(name)'
				}
			}
		]
	});
	
	cy.on('tap', 'node', function(event) {	
		window.open(this.data('url'));
	});
	
	cy.on('tap', 'edge', function(event) {
		window.open(this.data('url'));
	});
	
	if(window.location.hash) {
		var roo_node = cy.$(window.location.hash);
		
		if (roo_node) {
			cy.fit(roo_node, 100);
		}
	}
	
	document.getElementById('wrap').removeChild(document.getElementById('loading'));
});
