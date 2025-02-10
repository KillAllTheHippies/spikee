# Common delimiters and markers
DEFAULT_INJECTION_DELIMITERS = [
	'\nINJECTION_PAYLOAD\n',  # Default from CLI
	'(INJECTION_PAYLOAD)',    # From README example
	'{{INJECTION_PAYLOAD}}',  # Template style
	'[INJECTION_PAYLOAD]',    # Bracket style
	'<INJECTION_PAYLOAD>',    # XML style
	'/*INJECTION_PAYLOAD*/',  # Comment style
	'"INJECTION_PAYLOAD"',    # Quote style
	'INJECTION_PAYLOAD',      # Plain style
]

DEFAULT_SPOTLIGHTING_MARKERS = [
	'\nDOCUMENT\n',          # Default from CLI
	'\n<data>\nDOCUMENT\n</data>\n',  # From workspace example
	'{{DOCUMENT}}',          # Template style
	'[DOCUMENT]',            # Bracket style
	'<DOCUMENT>',            # XML style
	'/*DOCUMENT*/',          # Comment style
	'"DOCUMENT"',            # Quote style
	'DOCUMENT',              # Plain style
]