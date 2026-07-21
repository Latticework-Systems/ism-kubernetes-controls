# Local validation helper for this repository.
#
# Step by step:
# 1. `make install-kyverno` downloads the configured Kyverno CLI release into
#    `.tools/bin` if it is not already present.
# 2. `make validate` renders the root first-wave kustomization into
#    `.tools/first-wave-audit.yaml`.
# 3. `make validate` then runs the Kyverno CLI test suite under `policies/`.
# 4. `make test` runs the full Kyverno CLI test suite without rendering the
#    first-wave bundle.
# 5. Named test targets run one policy family's tests at a time.
#
# This Makefile does not apply policies to a cluster, install Kyverno in a
# cluster, label namespaces, run Kubescape, or contain cluster-specific config.
# KYVERNO_VERSION only pins the local test CLI and can be overridden per run.
KYVERNO_VERSION ?= v1.17.1
LOCAL_BIN ?= .tools/bin
KYVERNO ?= $(LOCAL_BIN)/kyverno
KYVERNO_DIR := $(dir $(KYVERNO))
FIRST_WAVE_RENDER ?= .tools/first-wave-audit.yaml
FIRST_WAVE_RENDER_DIR := $(dir $(FIRST_WAVE_RENDER))

# Detect OS/arch for CLI download.
UNAME_OS   := $(shell uname -s | tr '[:upper:]' '[:lower:]')
UNAME_ARCH := $(shell uname -m)
ifeq ($(UNAME_ARCH),x86_64)
  KYVERNO_ARCH := x86_64
else ifeq ($(UNAME_ARCH),aarch64)
  KYVERNO_ARCH := arm64
else ifeq ($(UNAME_ARCH),arm64)
  KYVERNO_ARCH := arm64
else
  KYVERNO_ARCH := $(UNAME_ARCH)
endif
KYVERNO_TARBALL := kyverno-cli_$(KYVERNO_VERSION)_$(UNAME_OS)_$(KYVERNO_ARCH).tar.gz
KYVERNO_SHA256_darwin_arm64 := 851d1fcc4427a317674cc1892af4f43dcd19983c94498a1a913b6b849f71ef8c
KYVERNO_SHA256_darwin_x86_64 := d221d8d93c622b68a2933f4e0accd61db4f41100336f1ddad141259742f70948
KYVERNO_SHA256_linux_arm64 := 6f6a66711ba8fc2bd54a28aa1755a62605d053a6a3a758186201ba1f56698ced
KYVERNO_SHA256_linux_s390x := ba54fbc42418731441c57afa55aef0f89204f33ffd25a52cb19c79c76fcf8969
KYVERNO_SHA256_linux_x86_64 := d0c0f52e8fc8d66a3663b63942b131e5f91b63f7644b3e446546f79142d1b7a3
KYVERNO_SHA256 ?= $(KYVERNO_SHA256_$(UNAME_OS)_$(KYVERNO_ARCH))

.PHONY: install-kyverno validate test mapping-generate mapping-check \
        test-application-control test-patch-applications test-workload-hardening \
        test-privileged-access test-patch-operating-systems test-backups

install-kyverno:
	@set -e; \
	if [ -x "$(KYVERNO)" ]; then \
		echo "kyverno already installed: $$($(KYVERNO) version 2>&1 | head -1)"; \
	else \
		echo "Installing kyverno CLI $(KYVERNO_VERSION) ($(UNAME_OS)/$(KYVERNO_ARCH))..."; \
		test -n "$(KYVERNO_SHA256)" || { echo "No pinned checksum for $(KYVERNO_TARBALL)"; exit 1; }; \
		mkdir -p "$(KYVERNO_DIR)"; \
		tmp_dir="$$(mktemp -d)"; \
		trap 'rm -rf "$$tmp_dir"' EXIT; \
		curl -fsSLo "$$tmp_dir/$(KYVERNO_TARBALL)" "https://github.com/kyverno/kyverno/releases/download/$(KYVERNO_VERSION)/$(KYVERNO_TARBALL)"; \
		printf '%s  %s\n' "$(KYVERNO_SHA256)" "$$tmp_dir/$(KYVERNO_TARBALL)" | shasum -a 256 -c -; \
		tar -xzf "$$tmp_dir/$(KYVERNO_TARBALL)" -C "$$tmp_dir" kyverno; \
		chmod +x "$$tmp_dir/kyverno"; \
		mv "$$tmp_dir/kyverno" "$(KYVERNO)"; \
		echo "Installed: $$($(KYVERNO) version 2>&1 | head -1)"; \
	fi

# kyverno test can report a result mismatch as an overall pass: the detailed
# row says "Want fail, got pass" while the summary and exit code stay green
# (observed with CLI v1.17.1 on Audit-mode policies). Grep the detailed
# results so mismatches fail the build.
define kyverno_test
	@out="$$($(KYVERNO) test $(1) --detailed-results 2>&1)" || { printf '%s\n' "$$out"; exit 1; }; \
	printf '%s\n' "$$out"; \
	if printf '%s\n' "$$out" | grep -q "Want "; then \
		echo "ERROR: kyverno test reported result mismatches ('Want' rows) despite a passing exit"; \
		exit 1; \
	fi
endef

## Render the first-wave Audit bundle and run all policy tests.
validate: install-kyverno
	@echo "==> Rendering first-wave Audit bundle..."
	@mkdir -p "$(FIRST_WAVE_RENDER_DIR)"
	@kubectl kustomize . > "$(FIRST_WAVE_RENDER)"
	@echo "==> Rendered first-wave Audit bundle to $(FIRST_WAVE_RENDER)"
	@echo "==> Running Kyverno policy tests..."
	$(call kyverno_test,policies/)
	@echo "==> Validation complete"

## Run Kyverno tests for all published policy families.
test: install-kyverno
	$(call kyverno_test,policies/)

mapping-generate:
	python3 scripts/generate_views.py

mapping-check:
	python3 scripts/validate_mapping.py
	python3 scripts/generate_views.py --check

## Run tests per policy family.
test-application-control: install-kyverno
	$(call kyverno_test,policies/application-control/)

test-patch-applications: install-kyverno
	$(call kyverno_test,policies/patch-applications/)

test-workload-hardening: install-kyverno
	$(call kyverno_test,policies/workload-hardening/)

test-privileged-access: install-kyverno
	$(call kyverno_test,policies/privileged-access/)

test-patch-operating-systems: install-kyverno
	$(call kyverno_test,policies/patch-operating-systems/)

test-backups: install-kyverno
	$(call kyverno_test,policies/backups/)
