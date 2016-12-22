var progress = {
	stage  : 0,
	stages : document.getElementById('progress').getElementsByTagName('p'),
	increment : function() {
		progress.stages[progress.stage].hidden = true;
		progress.stage++;
		if (progress.stages[progress.stage] !== undefined) {
			progress.stages[progress.stage].hidden = false;
		}
	}
}

progress.increment();

$.getJSON("/graph.json", function(json) {
	progress.increment();
	
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
					'label': 'data(name)',
					'text-halign': 'right',
					'text-valign': 'center',
					'text-margin-x': '5px',
					'background-color': '#FF5700',
				}
			}
		]
	});
	
	progress.increment();
	
	cy.on('tap', 'node, edge', function(event) {	
		window.open(this.data('url'));
	});
	
	if(window.location.hash) {
		var roo_node = cy.$(window.location.hash);
		
		if (roo_node) {
			cy.fit(roo_node, 100);
		}
	}
	
	delete progress;
	document.getElementById('wrap').removeChild(document.getElementById('splash'));
});
