fmt:
	black $$(git ls-files | grep .py$$ | grep -v migrations)
	isort training/*.py tiaas/*.py
