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
					'content': 'data(name)'
				}
			}
		]
	});
	
	progress.increment();
	
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
	
	delete progress;
	document.getElementById('wrap').removeChild(document.getElementById('splash'));
});
