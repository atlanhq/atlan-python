# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Hand-authored overlays for generated app builders.

An overlay is a mixin (``<ClassName>Overlay``) holding the few methods a generated
builder needs but the app's UI configmap can't express — e.g. a contract field
declared ``str`` that is really a JSON-encoded list, or an update/re-scope
lifecycle that acts against an existing workflow slug.

The generator (:mod:`pyatlan.generator.generate_apps`) detects an overlay whose
filename matches the generated module, makes the generated builder inherit the
mixin, and skips regenerating any method the overlay defines. The base thus keeps
regenerating from the contract while the hand-authored tweaks stay isolated here —
no per-app special-cases in the generator script and no fully hand-written module.
"""
