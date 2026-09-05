SRC_DIRS := simulator_3dof

.PHONY: format check-format

format:
	@isort --profile black -q $(SRC_DIRS)
	@black $(SRC_DIRS) 2>&1 | grep -E "reformatted|left unchanged" || true
check-format:
	@isort --check-only $(SRC_DIRS)
	@black --check $(SRC_DIRS) 2>&1 | grep -E "would be reformatted|would be left unchanged" || true