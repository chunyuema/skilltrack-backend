from django.core.management.base import BaseCommand
from skills.models import Track, SkillTheme, SkillSubCategory, Skill

class Command(BaseCommand):
    help = 'Populates the enriched tiered skills matrix and cleans up stale data'

    def handle(self, *args, **options):
        # 1. Define Tracks
        tracks_data = [
            {'id': 'core', 'name': 'Core Essentials', 'track_type': 'CORE'},
            {'id': 'frontend', 'name': 'Frontend Engineering', 'track_type': 'DOMAIN'},
            {'id': 'backend', 'name': 'Backend Engineering', 'track_type': 'DOMAIN'},
            {'id': 'fullstack', 'name': 'Full-Stack Engineering', 'track_type': 'DOMAIN'},
            {'id': 'ai-eng', 'name': 'AI Engineering', 'track_type': 'SPECIAL'},
            {'id': 'hpc', 'name': 'High-Performance Computing', 'track_type': 'SPECIAL'},
            {'id': 'dist-sys', 'name': 'Distributed Systems', 'track_type': 'SPECIAL'},
        ]

        valid_track_ids = []
        for tr_data in tracks_data:
            Track.objects.update_or_create(
                id=tr_data['id'],
                defaults={'name': tr_data['name'], 'track_type': tr_data['track_type']}
            )
            valid_track_ids.append(tr_data['id'])

        # 2. Define Themes & Hierarchy Organised by Track
        data = [
            {
                'track': 'core',
                'themes': [
                    {
                        'id': 'vcs-workflows',
                        'name': 'Version Control & Team Workflows',
                        'description': 'Universal tools for collaborative development.',
                        'subCategories': [
                            {
                                'id': 'git-fundamentals',
                                'name': 'Git Fundamentals',
                                'skills': [
                                    {'id': 'git-commits', 'name': 'Commits & Branching Strategies', 'description': 'Mastery of atomic commits, meaningful commit messages, and the use of feature branches to isolate development.'},
                                    {'id': 'git-merging', 'name': 'Merging Mechanics', 'description': 'Understanding the difference between fast-forward, recursive merges, and squashing to maintain a clean project history.'},
                                    {'id': 'git-conflicts', 'name': '3-way Conflict Resolution', 'description': 'Techniques for identifying and resolving code conflicts using base, local, and remote file versions.'},
                                ]
                            },
                            {
                                'id': 'git-internals',
                                'name': 'Git Internals',
                                'skills': [
                                    {'id': 'git-objects', 'name': '.git Folder (Blobs, Trees, Objects)'},
                                    {'id': 'git-hashes', 'name': 'Cryptographic Hashes'},
                                ]
                            },
                            {
                                'id': 'engineering-hygiene',
                                'name': 'Engineering Hygiene',
                                'skills': [
                                    {'id': 'vcs-flows', 'name': 'Trunk-based vs Git Flow'},
                                    {'id': 'pr-formatting', 'name': 'PR Formatting & Async Review'},
                                    {'id': 'semver', 'name': 'Semantic Versioning (SemVer)'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'data-persistence-basics',
                        'name': 'Data & Persistence Basics',
                        'description': 'Essential data management for every dev.',
                        'subCategories': [
                            {
                                'id': 'rdbms-foundations',
                                'name': 'Relational DB Foundations',
                                'skills': [
                                    {'id': 'db-crud', 'name': 'Basic CRUD Operations', 'description': 'Proficiency in SELECT, INSERT, UPDATE, and DELETE statements within relational database management systems.'},
                                    {'id': 'db-joins', 'name': 'JOIN & Aggregation Queries', 'description': 'Implementing complex relational logic using INNER, LEFT, RIGHT, and FULL outer joins along with GROUP BY aggregations.'},
                                ]
                            },
                            {
                                'id': 'indexing-acid',
                                'name': 'Indexing & ACID',
                                'skills': [
                                    {'id': 'btree-lookups', 'name': 'B-Tree Lookups'},
                                    {'id': 'acid-principles', 'name': 'ACID (Data Safety)'},
                                ]
                            },
                            {
                                'id': 'data-serialization',
                                'name': 'Data Serialization',
                                'skills': [
                                    {'id': 'serialization-formats', 'name': 'JSON / XML'},
                                    {'id': 'schema-validation', 'name': 'Schema Validation'},
                                    {'id': 'db-migrations-basic', 'name': 'Basic Schema Migrations'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'networking-web-mechanics',
                        'name': 'Networking & Web Mechanics',
                        'description': 'How the internet actually works.',
                        'subCategories': [
                            {
                                'id': 'protocols-lifecycle',
                                'name': 'Protocols & Lifecycle',
                                'skills': [
                                    {'id': 'http-methods', 'name': 'HTTP/HTTPS (GET, POST, etc.)', 'description': 'Deep understanding of HTTP verb semantics, statelessness, and the transition from HTTP/1.1 to modern HTTP/2 and 3.'},
                                    {'id': 'status-codes', 'name': 'Status Codes', 'description': 'The standard grammar of the web: handling 2xx (Success), 3xx (Redirect), 4xx (Client Error), and 5xx (Server Error) responses.'},
                                    {'id': 'dns-resolution', 'name': 'DNS Resolution', 'description': 'How human-readable domain names are translated into machine-readable IP addresses across the global name server hierarchy.'},
                                ]
                            },
                            {
                                'id': 'api-design-core',
                                'name': 'API Design',
                                'skills': [
                                    {'id': 'rest-contract', 'name': 'RESTful Principles'},
                                    {'id': 'statelessness', 'name': 'Statelessness & Payloads'},
                                ]
                            },
                            {
                                'id': 'web-security-basics',
                                'name': 'Web Security Basics',
                                'skills': [
                                    {'id': 'cors-csp', 'name': 'CORS & CSP'},
                                    {'id': 'cookie-security', 'name': 'Cookie & Header Security'},
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'track': 'frontend',
                'themes': [
                    {
                        'id': 'core-ui-tech',
                        'name': 'Core UI Technologies',
                        'description': 'Modern layouts and styling.',
                        'subCategories': [
                            {
                                'id': 'modern-css',
                                'name': 'Modern CSS',
                                'skills': [
                                    {'id': 'css-layouts', 'name': 'Flexbox, Grid, Subgrid'},
                                    {'id': 'css-in-js-tailwind', 'name': 'CSS-in-JS & Tailwind'},
                                    {'id': 'container-queries', 'name': 'Container Queries'},
                                    {'id': 'html5-semantic', 'name': 'Semantic HTML5'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'js-ts-mastery',
                        'name': 'JavaScript & TypeScript Mastery',
                        'description': 'Advanced language features.',
                        'subCategories': [
                            {
                                'id': 'runtime-execution',
                                'name': 'Runtime & Execution',
                                'skills': [
                                    {'id': 'async-event-loop', 'name': 'Async & Event Loop'},
                                    {'id': 'reactivity-models', 'name': 'DOM vs Signal-based Reactivity'},
                                ]
                            },
                            {
                                'id': 'ts-abstractions',
                                'name': 'TypeScript Abstractions',
                                'skills': [
                                    {'id': 'ts-generics', 'name': 'Generics & Conditional Types'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'architectural-rendering',
                        'name': 'Architectural Rendering',
                        'description': 'Modern delivery patterns.',
                        'subCategories': [
                            {
                                'id': 'rendering-strategies',
                                'name': 'Rendering Strategies',
                                'skills': [
                                    {'id': 'ssr-ssg-isr', 'name': 'SSR / SSG / ISR'},
                                    {'id': 'progressive-hydration', 'name': 'Progressive Hydration'},
                                    {'id': 'rsc', 'name': 'React Server Components (RSC)'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'perf-telemetry',
                        'name': 'Performance & Telemetry',
                        'description': 'Optimization and monitoring.',
                        'subCategories': [
                            {
                                'id': 'web-vitals',
                                'name': 'Web Vitals',
                                'skills': [
                                    {'id': 'core-web-vitals', 'name': 'INP, LCP, CLS Optimization'},
                                    {'id': 'crp-tuning', 'name': 'Critical Rendering Path Tuning'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'fe-state-architecture',
                        'name': 'State Architecture',
                        'description': 'Managing complex client-side data.',
                        'subCategories': [
                            {
                                'id': 'fe-state-models',
                                'name': 'State Models',
                                'skills': [
                                    {'id': 'atomic-state-jotai', 'name': 'Atomic State (Jotai)'},
                                    {'id': 'unidirectional-flow', 'name': 'Zustand / Redux'},
                                    {'id': 'server-cache-query', 'name': 'TanStack / React Query'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'fe-tooling',
                        'name': 'Frontend Tooling',
                        'description': 'Development and testing infrastructure.',
                        'subCategories': [
                            {
                                'id': 'bundlers-testing',
                                'name': 'Bundlers & Testing',
                                'skills': [
                                    {'id': 'vite-rspack', 'name': 'Vite / Rspack'},
                                    {'id': 'component-testing', 'name': 'Vitest / Jest'},
                                    {'id': 'e2e-playwright', 'name': 'Playwright E2E'},
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'track': 'backend',
                'themes': [
                    {
                        'id': 'be-system-architecture',
                        'name': 'System Architecture',
                        'description': 'Patterns for scalable services.',
                        'subCategories': [
                            {
                                'id': 'architectural-patterns-be',
                                'name': 'Patterns',
                                'skills': [
                                    {'id': 'microservices-orch', 'name': 'Microservices Orchestration'},
                                    {'id': 'ddd', 'name': 'Domain-Driven Design (DDD)'},
                                    {'id': 'hexagonal-clean', 'name': 'Hexagonal / Clean Architecture'},
                                    {'id': 'event-driven-async', 'name': 'Event-Driven Design'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'advanced-api-paradigms',
                        'name': 'Advanced API Paradigms',
                        'description': 'Beyond standard REST.',
                        'subCategories': [
                            {
                                'id': 'api-protocols',
                                'name': 'Protocols & Schemas',
                                'skills': [
                                    {'id': 'grpc-proto', 'name': 'gRPC & Protocol Buffers'},
                                    {'id': 'graphql-federation', 'name': 'GraphQL Schema Federation'},
                                ]
                            },
                            {
                                'id': 'real-time-streaming',
                                'name': 'Real-time & Streaming',
                                'skills': [
                                    {'id': 'websockets-sse', 'name': 'WebSockets & SSE'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'data-tiering-perf',
                        'name': 'Data Tiering & Performance',
                        'description': 'High-performance data access.',
                        'subCategories': [
                            {
                                'id': 'caching-pooling',
                                'name': 'Caching & Pooling',
                                'skills': [
                                    {'id': 'distributed-caching', 'name': 'Redis / Memcached'},
                                    {'id': 'invalidation-strategies', 'name': 'Write-through / Write-behind'},
                                    {'id': 'connection-pooling', 'name': 'Connection Pooling'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'iam-control',
                        'name': 'Identity & Access Control',
                        'description': 'Security and authorization.',
                        'subCategories': [
                            {
                                'id': 'auth-flows',
                                'name': 'Auth Flows',
                                'skills': [
                                    {'id': 'oauth-oidc-jwt', 'name': 'OAuth 2.0 / OIDC / JWT'},
                                    {'id': 'rbac-abac-be', 'name': 'RBAC vs ABAC'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'be-app-sec',
                        'name': 'Application Security',
                        'description': 'Securing the backend.',
                        'subCategories': [
                            {
                                'id': 'owasp-mitigation',
                                'name': 'OWASP Mitigation',
                                'skills': [
                                    {'id': 'sql-injection-ssrf', 'name': 'SQLi, SSRF, BOLA Mitigation'},
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'track': 'hpc',
                'themes': [
                    {
                        'id': 'hardware-perf',
                        'name': 'Hardware-Level Performance',
                        'description': 'Optimizing for the metal.',
                        'subCategories': [
                            {
                                'id': 'cpu-memory-opt',
                                'name': 'CPU & Memory',
                                'skills': [
                                    {'id': 'cache-line-opt', 'name': 'L1/L2/L3 Cache Line & False Sharing'},
                                    {'id': 'simd-vectorization', 'name': 'SIMD Vectorization'},
                                    {'id': 'memory-alignment-padding', 'name': 'Alignment & Struct Padding'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'concurrency-mechanics',
                        'name': 'Concurrency Mechanics',
                        'description': 'Low-level thread management.',
                        'subCategories': [
                            {
                                'id': 'low-level-sync',
                                'name': 'Low-level Sync',
                                'skills': [
                                    {'id': 'lock-free-ds', 'name': 'Lock-free Data Structures'},
                                    {'id': 'atomic-primitives', 'name': 'Atomic Primitives'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'compilation-infra',
                        'name': 'Compilation Infrastructure',
                        'description': 'Language and compiler internals.',
                        'subCategories': [
                            {
                                'id': 'compiler-internals',
                                'name': 'Compiler Internals',
                                'skills': [
                                    {'id': 'ast-manipulation', 'name': 'AST Manipulation'},
                                    {'id': 'custom-jit', 'name': 'Custom JIT Logic'},
                                    {'id': 'llvm-ir-opt', 'name': 'LLVM IR Optimization'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'hpc-profiling',
                        'name': 'Profiling Systems',
                        'description': 'Deep performance analysis.',
                        'subCategories': [
                            {
                                'id': 'deep-tracing',
                                'name': 'Tracing & Analysis',
                                'skills': [
                                    {'id': 'hardware-tracing', 'name': 'Hardware Tracing'},
                                    {'id': 'ebpf-analysis', 'name': 'eBPF Kernel Analysis'},
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'track': 'dist-sys',
                'themes': [
                    {
                        'id': 'fault-tolerant-consensus',
                        'name': 'Fault-Tolerant Consensus',
                        'description': 'Coordination at scale.',
                        'subCategories': [
                            {
                                'id': 'consensus-protocols',
                                'name': 'Protocols',
                                'skills': [
                                    {'id': 'paxos-multi', 'name': 'Multi-Paxos'},
                                    {'id': 'raft-mechanics', 'name': 'Raft Leader & Replication'},
                                    {'id': 'pbft', 'name': 'Practical Byzantine Fault Tolerance'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'dist-storage-mechanics',
                        'name': 'Distributed Storage Mechanics',
                        'description': 'Managing data across nodes.',
                        'subCategories': [
                            {
                                'id': 'sharding-hashing',
                                'name': 'Sharding & Hashing',
                                'skills': [
                                    {'id': 'cap-pacelc', 'name': 'PACELC / CAP Theorem'},
                                    {'id': 'dynamic-sharding', 'name': 'Dynamic Database Sharding'},
                                    {'id': 'consistent-hashing', 'name': 'Consistent Hashing Algorithms'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'high-throughput-streams',
                        'name': 'High-Throughput Streams',
                        'description': 'Messaging and event pipelines.',
                        'subCategories': [
                            {
                                'id': 'event-log-systems',
                                'name': 'Event Logs',
                                'skills': [
                                    {'id': 'kafka-partitioning', 'name': 'Kafka Partition Rebalancing'},
                                    {'id': 'cdc-pipelines', 'name': 'CDC Pipelines'},
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'track': 'ai-eng',
                'themes': [
                    {
                        'id': 'context-augmentation-rag',
                        'name': 'Context Augmentation (RAG)',
                        'description': 'Knowledge retrieval for AI.',
                        'subCategories': [
                            {
                                'id': 'rag-tuning',
                                'name': 'Retrieval Tuning',
                                'skills': [
                                    {'id': 'vector-embeddings-selection', 'name': 'Embedding Selection'},
                                    {'id': 'hnsw-ivf-pq', 'name': 'HNSW & IVF-PQ Parameters'},
                                    {'id': 'hierarchical-chunking', 'name': 'Document Hierarchical Chunking'},
                                    {'id': 'cross-encoder-reranking', 'name': 'Cross-Encoder Reranking'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'agentic-ai-arch',
                        'name': 'Agentic AI Architectures',
                        'description': 'Autonomous AI systems.',
                        'subCategories': [
                            {
                                'id': 'agents-evaluation',
                                'name': 'Agents & Eval',
                                'skills': [
                                    {'id': 'function-calling', 'name': 'Function Calling Mechanics'},
                                    {'id': 'langgraph-loops', 'name': 'LangGraph State Loops'},
                                    {'id': 'llm-judge-ragas', 'name': 'LLM-as-a-judge (Ragas)'},
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

        # 3. Populate Database and collect valid IDs for cleanup
        valid_theme_ids = []
        valid_subcat_ids = []
        valid_skill_ids = []

        for track_group in data:
            track = Track.objects.get(id=track_group['track'])
            for t_idx, t_data in enumerate(track_group['themes']):
                theme, created = SkillTheme.objects.update_or_create(
                    id=t_data['id'],
                    defaults={
                        'track': track,
                        'name': t_data['name'],
                        'description': t_data['description'],
                        'order': t_idx
                    }
                )
                valid_theme_ids.append(theme.id)

                for sc_idx, sc_data in enumerate(t_data['subCategories']):
                    subcat, created = SkillSubCategory.objects.update_or_create(
                        id=sc_data['id'],
                        defaults={'theme': theme, 'name': sc_data['name'], 'order': sc_idx}
                    )
                    valid_subcat_ids.append(subcat.id)

                    for s_idx, s_data in enumerate(sc_data['skills']):
                        skill, created = Skill.objects.update_or_create(
                            id=s_data['id'],
                            defaults={'sub_category': subcat, 'name': s_data['name'], 'order': s_idx}
                        )
                        valid_skill_ids.append(skill.id)
        
        # 4. Cleanup Stale Data
        self.stdout.write("Cleaning up stale data...")
        
        deleted_skills, _ = Skill.objects.exclude(id__in=valid_skill_ids).delete()
        self.stdout.write(f"Deleted {deleted_skills} stale skills.")
        
        deleted_subcats, _ = SkillSubCategory.objects.exclude(id__in=valid_subcat_ids).delete()
        self.stdout.write(f"Deleted {deleted_subcats} stale sub-categories.")
        
        deleted_themes, _ = SkillTheme.objects.exclude(id__in=valid_theme_ids).delete()
        self.stdout.write(f"Deleted {deleted_themes} stale themes.")
        
        deleted_tracks, _ = Track.objects.exclude(id__in=valid_track_ids).delete()
        self.stdout.write(f"Deleted {deleted_tracks} stale tracks.")

        self.stdout.write(self.style.SUCCESS('Successfully synchronized skills matrix with database.'))
