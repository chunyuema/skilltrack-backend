from django.core.management.base import BaseCommand
from profiles.models import SkillTheme, SkillSubCategory, Skill

class Command(BaseCommand):
    help = 'Populates the initial skills matrix'

    def handle(self, *args, **options):
        themes_data = [
            {
                'id': 'foundations',
                'name': 'Low-Level Foundations & Core CS',
                'description': 'The mechanical "physics" of software before frameworks.',
                'subCategories': [
                    {
                        'id': 'arch',
                        'name': 'Computer Architecture',
                        'skills': [
                            {'id': 'cpu-cache', 'name': 'CPU Caching (L1/L2/L3)'},
                            {'id': 'instruction-sets', 'name': 'Instruction Sets (x86 vs ARM)'},
                            {'id': 'memory-alignment', 'name': 'Memory Alignment'},
                        ]
                    },
                    {
                        'id': 'os',
                        'name': 'Operating Systems',
                        'skills': [
                            {'id': 'process-thread', 'name': 'Process vs Thread Mgmt'},
                            {'id': 'kernel-syscalls', 'name': 'Kernel Syscalls'},
                            {'id': 'file-systems', 'name': 'File Systems (NTFS/Ext4)'},
                            {'id': 'io-multiplexing', 'name': 'I/O Multiplexing (epoll/kqueue)'},
                        ]
                    },
                    {
                        'id': 'networking',
                        'name': 'Networking (L4–L7)',
                        'skills': [
                            {'id': 'transport', 'name': 'Transport (TCP/UDP/QUIC)'},
                            {'id': 'app-proto', 'name': 'App Protocols (HTTP/3, gRPC)'},
                            {'id': 'mtls', 'name': 'mTLS & WebSockets'},
                        ]
                    },
                    {
                        'id': 'data-structures',
                        'name': 'Data Structures',
                        'skills': [
                            {'id': 'b-trees', 'name': 'B-Trees (Databases)'},
                            {'id': 'bloom-filters', 'name': 'Bloom Filters (Caching)'},
                            {'id': 'crdts', 'name': 'CRDTs (Collab Editing)'},
                        ]
                    }
                ]
            },
            {
                'id': 'language',
                'name': 'Language & Runtime Mastery',
                'description': 'How code behaves under pressure, beyond syntax.',
                'subCategories': [
                    {
                        'id': 'memory-mgmt',
                        'name': 'Memory Management',
                        'skills': [
                            {'id': 'stack-heap', 'name': 'Stack vs Heap Allocation'},
                            {'id': 'raii', 'name': 'RAII / Borrow Checking'},
                            {'id': 'gc-tuning', 'name': 'GC Tuning (JVM/V8)'},
                        ]
                    },
                    {
                        'id': 'type-systems',
                        'name': 'Type Systems',
                        'skills': [
                            {'id': 'static-dynamic', 'name': 'Static vs Dynamic'},
                            {'id': 'nominal-structural', 'name': 'Nominal vs Structural'},
                            {'id': 'generics', 'name': 'Generics & Metaprogramming'},
                        ]
                    },
                    {
                        'id': 'functional',
                        'name': 'Functional Programming',
                        'skills': [
                            {'id': 'immutability', 'name': 'Immutability'},
                            {'id': 'monads', 'name': 'Monads & Higher-Order Fn'},
                            {'id': 'lazy-eval', 'name': 'Lazy Evaluation'},
                        ]
                    },
                    {
                        'id': 'compiler',
                        'name': 'Compiler Basics',
                        'skills': [
                            {'id': 'ast', 'name': 'Abstract Syntax Trees (AST)'},
                            {'id': 'jit', 'name': 'JIT Compilation'},
                        ]
                    }
                ]
            },
            {
                'id': 'backend',
                'name': 'Backend & Distributed Systems',
                'description': 'How services talk to each other and stay alive at scale.',
                'subCategories': [
                    {
                        'id': 'arch-patterns',
                        'name': 'Architectural Patterns',
                        'skills': [
                            {'id': 'microservices', 'name': 'Microservices'},
                            {'id': 'event-sourcing', 'name': 'Event Sourcing & CQRS'},
                            {'id': 'hexagonal', 'name': 'Hexagonal Architecture'},
                        ]
                    },
                    {
                        'id': 'concurrency',
                        'name': 'Concurrency Models',
                        'skills': [
                            {'id': 'actor-model', 'name': 'Actor Model (Erlang/Akka)'},
                            {'id': 'csp', 'name': 'CSP (Go Channels)'},
                            {'id': 'event-loops', 'name': 'Event Loops (Node.js)'},
                        ]
                    },
                    {
                        'id': 'consensus',
                        'name': 'Distributed Consensus',
                        'skills': [
                            {'id': 'paxos-raft', 'name': 'Paxos / Raft'},
                            {'id': 'gossip', 'name': 'Gossip Protocols'},
                        ]
                    },
                    {
                        'id': 'messaging',
                        'name': 'Messaging & Streams',
                        'skills': [
                            {'id': 'message-queues', 'name': 'Message Queuing (RabbitMQ)'},
                            {'id': 'event-streaming', 'name': 'Event Streaming (Kafka)'},
                            {'id': 'cdc', 'name': 'Change Data Capture (CDC)'},
                        ]
                    }
                ]
            },
            {
                'id': 'data',
                'name': 'Data Engineering & Persistence',
                'description': 'Managing the most expensive part of any system.',
                'subCategories': [
                    {
                        'id': 'rdbms',
                        'name': 'Relational DBs',
                        'skills': [
                            {'id': 'sql-opt', 'name': 'Deep SQL Optimization'},
                            {'id': 'acid', 'name': 'ACID & Isolation Levels'},
                            {'id': 'sharding', 'name': 'Partitioning & Sharding'},
                        ]
                    },
                    {
                        'id': 'nosql',
                        'name': 'NoSQL Ecosystem',
                        'skills': [
                            {'id': 'document-db', 'name': 'Document (Mongo/Couch)'},
                            {'id': 'kv-store', 'name': 'Key-Value (Redis/Bitmaps)'},
                            {'id': 'wide-column', 'name': 'Wide-Column (Cassandra)'},
                        ]
                    },
                    {
                        'id': 'vector-search',
                        'name': 'Vector & Search',
                        'skills': [
                            {'id': 'vector-db', 'name': 'Vector DBs (HNSW/IVF)'},
                            {'id': 'search-engines', 'name': 'Inverted Indexes (Elastic)'},
                        ]
                    }
                ]
            },
            {
                'id': 'frontend',
                'name': 'Frontend & Client-Side',
                'description': 'Distributed systems running in a browser.',
                'subCategories': [
                    {
                        'id': 'rendering',
                        'name': 'Rendering Patterns',
                        'skills': [
                            {'id': 'ssr-ssg', 'name': 'SSR / SSG / ISR'},
                            {'id': 'hydration', 'name': 'Partial Hydration'},
                        ]
                    },
                    {
                        'id': 'browser',
                        'name': 'Browser Internals',
                        'skills': [
                            {'id': 'crp', 'name': 'Critical Rendering Path'},
                            {'id': 'v8-opt', 'name': 'V8 Engine Optimization'},
                            {'id': 'web-workers', 'name': 'Web Workers'},
                        ]
                    },
                    {
                        'id': 'wasm',
                        'name': 'WebAssembly',
                        'skills': [
                            {'id': 'wasm-rust', 'name': 'Wasm (Rust/C++)'},
                        ]
                    },
                    {
                        'id': 'state',
                        'name': 'State Management',
                        'skills': [
                            {'id': 'atomic-state', 'name': 'Atomic (Recoil/Jotai)'},
                            {'id': 'flux', 'name': 'Flux (Redux)'},
                            {'id': 'server-state', 'name': 'Server State (React Query)'},
                        ]
                    }
                ]
            },
            {
                'id': 'cloud',
                'name': 'Cloud & Infrastructure',
                'description': 'Owning the environment.',
                'subCategories': [
                    {
                        'id': 'containers',
                        'name': 'Containerization',
                        'skills': [
                            {'id': 'oci', 'name': 'OCI Images & Multi-stage'},
                            {'id': 'runtimes', 'name': 'Runtimes (containerd)'},
                        ]
                    },
                    {
                        'id': 'orchestration',
                        'name': 'Orchestration',
                        'skills': [
                            {'id': 'k8s', 'name': 'Kubernetes (CRDs/Operators)'},
                            {'id': 'service-mesh', 'name': 'Service Mesh (Istio)'},
                        ]
                    },
                    {
                        'id': 'serverless',
                        'name': 'Serverless',
                        'skills': [
                            {'id': 'faas', 'name': 'FaaS (Lambda)'},
                            {'id': 'edge', 'name': 'Edge Computing (Workers)'},
                        ]
                    },
                    {
                        'id': 'iac',
                        'name': 'Infrastructure as Code',
                        'skills': [
                            {'id': 'terraform', 'name': 'Declarative (Terraform)'},
                            {'id': 'pulumi', 'name': 'Imperative (Pulumi/CDK)'},
                        ]
                    }
                ]
            },
            {
                'id': 'security',
                'name': 'Security (Shift-Left)',
                'description': 'Security as a technical requirement.',
                'subCategories': [
                    {
                        'id': 'iam',
                        'name': 'Identity & Access',
                        'skills': [
                            {'id': 'oauth-oidc', 'name': 'OAuth2 / OIDC / SAML'},
                            {'id': 'rbac-abac', 'name': 'RBAC / ABAC'},
                        ]
                    },
                    {
                        'id': 'app-sec',
                        'name': 'Application Security',
                        'skills': [
                            {'id': 'owasp', 'name': 'Injection/XSS/CSRF/SSRF'},
                        ]
                    },
                    {
                        'id': 'crypto',
                        'name': 'Cryptography',
                        'skills': [
                            {'id': 'hashing', 'name': 'Hashing (Argon2)'},
                            {'id': 'encryption', 'name': 'Sym/Asymmetric Encryption'},
                            {'id': 'zkp', 'name': 'Zero-Knowledge Proofs'},
                        ]
                    },
                    {
                        'id': 'supply-chain',
                        'name': 'Supply Chain',
                        'skills': [
                            {'id': 'sbom', 'name': 'SBOM & Vuln Scanning'},
                        ]
                    }
                ]
            },
            {
                'id': 'quality',
                'name': 'Quality & Observability',
                'description': 'Keeping the system green.',
                'subCategories': [
                    {
                        'id': 'testing',
                        'name': 'Testing Strategy',
                        'skills': [
                            {'id': 'prop-testing', 'name': 'Property-based Testing'},
                            {'id': 'chaos', 'name': 'Chaos Engineering'},
                            {'id': 'load-test', 'name': 'Load/Stress (k6)'},
                        ]
                    },
                    {
                        'id': 'observability',
                        'name': 'Observability Pillars',
                        'skills': [
                            {'id': 'logs', 'name': 'Logs (ELK/Loki)'},
                            {'id': 'metrics', 'name': 'Metrics (Prometheus)'},
                            {'id': 'traces', 'name': 'Tracing (Jaeger)'},
                        ]
                    },
                    {
                        'id': 'sre',
                        'name': 'SRE Principles',
                        'skills': [
                            {'id': 'slis-slos', 'name': 'Error Budgets & SLOs'},
                        ]
                    }
                ]
            },
            {
                'id': 'ai',
                'name': 'AI Engineering',
                'description': 'Integrating machine intelligence.',
                'subCategories': [
                    {
                        'id': 'llm-ops',
                        'name': 'LLM Orchestration',
                        'skills': [
                            {'id': 'langchain', 'name': 'LangChain/LlamaIndex'},
                            {'id': 'prompt-eng', 'name': 'Technical Prompt Eng'},
                        ]
                    },
                    {
                        'id': 'rag',
                        'name': 'RAG Pipelines',
                        'skills': [
                            {'id': 'chunking', 'name': 'Chunking & Embeddings'},
                            {'id': 'semantic', 'name': 'Semantic Search'},
                        ]
                    },
                    {
                        'id': 'deployment',
                        'name': 'Model Deployment',
                        'skills': [
                            {'id': 'quantization', 'name': 'Quantization'},
                            {'id': 'api-opt', 'name': 'API Optimization'},
                        ]
                    }
                ]
            }
        ]

        for t_idx, t_data in enumerate(themes_data):
            theme, created = SkillTheme.objects.update_or_create(
                id=t_data['id'],
                defaults={'name': t_data['name'], 'description': t_data['description'], 'order': t_idx}
            )
            for sc_idx, sc_data in enumerate(t_data['subCategories']):
                subcat, created = SkillSubCategory.objects.update_or_create(
                    id=sc_data['id'],
                    defaults={'theme': theme, 'name': sc_data['name'], 'order': sc_idx}
                )
                for s_idx, s_data in enumerate(sc_data['skills']):
                    Skill.objects.update_or_create(
                        id=s_data['id'],
                        defaults={'sub_category': subcat, 'name': s_data['name'], 'order': s_idx}
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated skills matrix'))
