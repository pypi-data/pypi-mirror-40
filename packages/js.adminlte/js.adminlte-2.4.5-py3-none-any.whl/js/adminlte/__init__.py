from fanstatic import Library, Resource, Group
from js.bootstrap import bootstrap_css, bootstrap_js

library = Library('adminlte', 'resources')

adminlte_css = Resource(library, 'css/adminlte.css',
						minified='css/adminlte.min.css',
						depends=[bootstrap_css])

adminlte_skin_blue_css = Resource(library,'css/skin-blue.css',
									minified='css/skin-blue.min.css',
									depends=[adminlte_css])

adminlte_js = Resource(library, 'js/adminlte.js',
	                   minified='js/adminlte.min.js',
	                   depends=[bootstrap_js, adminlte_skin_blue_css])










