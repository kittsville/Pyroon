---
---
{% capture graph_styles %}
{% include graph.css %}
{% endcapture %}
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

$.ajax({
	cache: {% if jekyll.environment == "production" %}true{% else %}false{% endif %},
    url: "{{ site.url }}/graph.json",
    dataType: "json",
    success: function(json) {
		progress.increment();
		
		cy = cytoscape({
			
			container: document.getElementById('graph'),
			
			elements: json.graph,

			layout: {
				name: 'dagre'
			},
			
			wheelSensitivity: 0.1,
			
			autoungrabify: true,
			
			hideLabelsOnViewport: true,
			hideEdgesOnViewport: true,

			// so we can see the ids etc
			style: '{{ graph_styles | strip | strip_newlines }}',
		});
		
		cy.ready(function(){
			progress.increment();
			
			cy.on('tap', 'node, edge', function(event) {	
				window.open(this.data('url'));
			});
			
			if(window.location.hash) {
				var roo_node = cy.$(window.location.hash);
				
				if (roo_node) {
					cy.fit(roo_node, 100);
				}
			} else {
				var firstRoo = cy.$('node[?first]');
				
				if (firstRoo) {
					cy.fit(firstRoo, 150);
				}
			}
			
			delete progress;
			document.getElementById('wrap').removeChild(document.getElementById('splash'));
		});
	}
});
