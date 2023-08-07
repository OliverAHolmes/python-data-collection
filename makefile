run:
	export ENV=development && uvicorn main:app --reload --host 0.0.0.0

clean-run:
	export ENV=development && rm -f database.db && uvicorn main:app --reload --host 0.0.0.0

generate_requirements_txt:
	pipenv requirements --dev  > requirements.txt

test:
	rm -f test.db
	export ENV=testing && pytest tests -x -vv

install:
	pipenv install --dev
