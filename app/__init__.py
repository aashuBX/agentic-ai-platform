"""Agentic AI Platform — independent, public-safe portfolio implementation.

See README.md for the public-safe disclaimer and requirement.md for the full brief this
package implements progressively, phase by phase.
"""

import os

# The optional local RAG stack (faiss-cpu, torch/sentence-transformers, scikit-learn — all pulled
# in transitively by the "rag"/"faiss" extras) each bundle their own OpenMP runtime. Loading more
# than one in the same process — e.g. FAISS as the vector store alongside the cross-encoder
# reranker, or simply running this repo's test suite — can deadlock or crash on macOS unless this
# is set before any of them initialize (a known, common workaround for this class of native-library
# conflict, not a bug in this codebase). Must happen at the top of the package's own `__init__`,
# before any submodule has a chance to import one of these libraries.
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("OMP_NUM_THREADS", "1")

__version__ = "0.1.0"
