build:
	python3 build.py
	python3 test/test.py _build/index.html _deploy/index.html

deploy: build
	cp data.json dynamics.json _deploy/
	cd _deploy && git add -A && git commit -m "update" || true
	cd _deploy && git push

push:
	cd _deploy && git add -A && git commit -m "update" || true
	cd _deploy && git push

.PHONY: build deploy push
