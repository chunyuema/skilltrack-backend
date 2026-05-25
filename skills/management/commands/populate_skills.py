from django.core.management.base import BaseCommand
from skills.models import Track, SkillTheme, SkillSubCategory, Skill

class Command(BaseCommand):
    help = 'Populates the tiered skills matrix (T-Shaped Engineer)'

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

        for tr_data in tracks_data:
            Track.objects.update_or_create(
                id=tr_data['id'],
                defaults={'name': tr_data['name'], 'track_type': tr_data['track_type']}
            )

        # 2. Define Themes & Hierarchy
        # We'll organize these by track
        data = [
            {
                'track': 'core',
                'themes': [
                    {
                        'id': 'git-vcs',
                        'name': 'Version Control & Git',
                        'description': 'Universal tools for collaborative development.',
                        'subCategories': [
                            {
                                'id': 'git-basics',
                                'name': 'Git Fundamentals',
                                'skills': [
                                    {'id': 'git-commit', 'name': 'Commits & Branching'},
                                    {'id': 'git-merge-rebase', 'name': 'Merging vs Rebasing'},
                                    {'id': 'git-conflict', 'name': 'Conflict Resolution'},
                                ]
                            },
                            {
                                'id': 'vcs-workflows',
                                'name': 'Workflows',
                                'skills': [
                                    {'id': 'git-flow', 'name': 'Git Flow / GitHub Flow'},
                                    {'id': 'pr-reviews', 'name': 'Code Review Best Practices'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'sql-fundamentals',
                        'name': 'SQL & Data Basics',
                        'description': 'Essential data management for every dev.',
                        'subCategories': [
                            {
                                'id': 'sql-basics',
                                'name': 'Basic SQL',
                                'skills': [
                                    {'id': 'sql-crud', 'name': 'CRUD Operations'},
                                    {'id': 'sql-joins', 'name': 'Joins & Aggregations'},
                                    {'id': 'sql-indexes', 'name': 'Basic Indexing'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'web-mechanics',
                        'name': 'Web Mechanics',
                        'description': 'How the internet actually works.',
                        'subCategories': [
                            {
                                'id': 'http-basics',
                                'name': 'HTTP/HTTPS',
                                'skills': [
                                    {'id': 'http-verbs', 'name': 'Methods (GET, POST, etc.)'},
                                    {'id': 'dns-basics', 'name': 'DNS Fundamentals'},
                                    {'id': 'rest-principles', 'name': 'RESTful API Design'},
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
                        'id': 'fe-rendering',
                        'name': 'Rendering & Performance',
                        'description': 'Client-side delivery patterns.',
                        'subCategories': [
                            {
                                'id': 'rendering-patterns',
                                'name': 'Patterns',
                                'skills': [
                                    {'id': 'ssr', 'name': 'Server-Side Rendering (SSR)'},
                                    {'id': 'ssg', 'name': 'Static Site Gen (SSG)'},
                                    {'id': 'hydration-fe', 'name': 'Partial Hydration'},
                                ]
                            }
                        ]
                    },
                    {
                        'id': 'fe-state',
                        'name': 'State & Architecture',
                        'description': 'Managing complex client-side data.',
                        'subCategories': [
                            {
                                'id': 'state-mgmt',
                                'name': 'State Models',
                                'skills': [
                                    {'id': 'atomic-state-fe', 'name': 'Atomic State (Jotai/Recoil)'},
                                    {'id': 'flux-redux', 'name': 'Flux/Redux Patterns'},
                                    {'id': 'server-cache', 'name': 'Server State (React Query)'},
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
                        'id': 'be-patterns',
                        'name': 'System Architecture',
                        'description': 'Patterns for scalable services.',
                        'subCategories': [
                            {
                                'id': 'arch-patterns-be',
                                'name': 'Structural Patterns',
                                'skills': [
                                    {'id': 'microservices-be', 'name': 'Microservices'},
                                    {'id': 'hexagonal-be', 'name': 'Hexagonal/Clean Arch'},
                                    {'id': 'event-driven', 'name': 'Event-Driven Design'},
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
                        'id': 'low-level',
                        'name': 'HPC & Foundations',
                        'description': 'Hardware-level performance.',
                        'subCategories': [
                            {
                                'id': 'cpu-theory',
                                'name': 'CPU & Memory',
                                'skills': [
                                    {'id': 'cpu-cache-hpc', 'name': 'CPU Caching (L1/L2/L3)'},
                                    {'id': 'simd', 'name': 'SIMD / Vectorization'},
                                    {'id': 'memory-alignment-hpc', 'name': 'Memory Alignment'},
                                ]
                            },
                            {
                                'id': 'compilers',
                                'name': 'Compiler Theory',
                                'skills': [
                                    {'id': 'ast-hpc', 'name': 'AST & JIT'},
                                    {'id': 'llvm', 'name': 'LLVM IR Fundamentals'},
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
                        'id': 'consensus-theory',
                        'name': 'Distributed Consensus',
                        'description': 'Solving coordination at scale.',
                        'subCategories': [
                            {
                                'id': 'consensus-algos',
                                'name': 'Algorithms',
                                'skills': [
                                    {'id': 'paxos', 'name': 'Paxos'},
                                    {'id': 'raft', 'name': 'Raft'},
                                    {'id': 'byzantine', 'name': 'Byzantine Fault Tolerance'},
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
                        'id': 'llm-engineering',
                        'name': 'LLM & RAG',
                        'description': 'Building with large language models.',
                        'subCategories': [
                            {
                                'id': 'rag-pipelines',
                                'name': 'RAG Fundamentals',
                                'skills': [
                                    {'id': 'embeddings', 'name': 'Vector Embeddings'},
                                    {'id': 'vector-db-rag', 'name': 'Vector DB (HNSW/IVF)'},
                                    {'id': 'chunking-rag', 'name': 'Chunking Strategies'},
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

        # 3. Populate Database
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
        
        self.stdout.write(self.style.SUCCESS('Successfully populated tiered skills matrix'))
