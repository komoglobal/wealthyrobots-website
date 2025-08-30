"""
ENHANCED MEMORY SYSTEM
=====================
Advanced memory management for AGI with long-term retention,
knowledge consolidation, and intelligent retrieval capabilities.
"""

import time
import json
import hashlib
import threading
import random
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import heapq

class EnhancedMemorySystem:
    """Advanced memory system with multiple memory types and intelligent management"""

    def __init__(self):
        self.short_term_memory = []  # Recent events and context
        self.long_term_memory = {}   # Consolidated knowledge
        self.episodic_memory = []    # Personal experiences
        self.semantic_memory = {}    # Factual knowledge
        self.procedural_memory = {}  # How-to knowledge
        self.working_memory = {}     # Currently active information

        self.memory_strength = {}    # Memory consolidation strength
        self.memory_associations = defaultdict(list)  # Memory links
        self.memory_tags = defaultdict(set)  # Memory categorization
        self.memory_timestamp = {}   # Memory timestamps

        self.consolidation_threshold = 10  # Memories to trigger consolidation
        self.forgetfulness_rate = 0.1      # Rate at which weak memories fade
        self.max_short_term_size = 1000
        self.max_working_memory_size = 100

        self.memory_lock = threading.Lock()
        self.consolidation_thread = None
        self.cleanup_thread = None

        self._initialize_memory_system()
        self._start_memory_management()

    def _initialize_memory_system(self):
        """Initialize the enhanced memory system"""
        print("🧠 ENHANCED MEMORY SYSTEM INITIALIZING...")
        print("=" * 50)

        # Load existing memories if available
        self._load_memory_state()

        # Initialize memory structures
        print("✅ Short-term memory initialized")
        print("✅ Long-term memory initialized")
        print("✅ Episodic memory initialized")
        print("✅ Semantic memory initialized")
        print("✅ Procedural memory initialized")
        print("✅ Working memory initialized")

        # Memory performance metrics
        self.memory_stats = {
            "total_memories": 0,
            "consolidation_cycles": 0,
            "retrieval_requests": 0,
            "memory_hits": 0,
            "memory_misses": 0,
            "compression_rate": 0,
            "last_cleanup": datetime.now().isoformat()
        }

    def _start_memory_management(self):
        """Start background memory management threads"""
        print("\n🚀 STARTING MEMORY MANAGEMENT...")
        print("=" * 40)

        # Start consolidation thread
        self.consolidation_thread = threading.Thread(target=self._memory_consolidation_loop)
        self.consolidation_thread.daemon = True
        self.consolidation_thread.start()

        # Start cleanup thread
        self.cleanup_thread = threading.Thread(target=self._memory_cleanup_loop)
        self.cleanup_thread.daemon = True
        self.cleanup_thread.start()

        print("✅ Memory consolidation thread started")
        print("✅ Memory cleanup thread started")

    def store_memory(self, content: Any, memory_type: str = "episodic",
                    tags: List[str] = None, importance: float = 1.0) -> str:
        """Store information in appropriate memory system"""
        with self.memory_lock:
            try:
                # Generate unique memory ID
                memory_id = self._generate_memory_id(content)

                # Create memory object
                memory_object = {
                    "id": memory_id,
                    "content": content,
                    "type": memory_type,
                    "tags": tags or [],
                    "importance": importance,
                    "timestamp": datetime.now().isoformat(),
                    "access_count": 0,
                    "last_access": datetime.now().isoformat(),
                    "strength": importance,
                    "associations": []
                }

                # Store based on type
                if memory_type == "short_term":
                    self._store_short_term_memory(memory_object)
                elif memory_type == "long_term":
                    self._store_long_term_memory(memory_object)
                elif memory_type == "episodic":
                    self.episodic_memory.append(memory_object)
                elif memory_type == "semantic":
                    self._store_semantic_memory(memory_object)
                elif memory_type == "procedural":
                    self._store_procedural_memory(memory_object)
                elif memory_type == "working":
                    self._store_working_memory(memory_object)
                else:
                    # Default to episodic
                    self.episodic_memory.append(memory_object)

                # Update metadata
                self.memory_timestamp[memory_id] = memory_object["timestamp"]
                self.memory_strength[memory_id] = memory_object["strength"]

                # Add tags
                for tag in memory_object["tags"]:
                    self.memory_tags[tag].add(memory_id)

                self.memory_stats["total_memories"] += 1

                return memory_id

            except Exception as e:
                print(f"⚠️  Memory storage error: {e}")
                return None

    def _store_short_term_memory(self, memory_object):
        """Store in short-term memory with size management"""
        self.short_term_memory.append(memory_object)

        # Maintain size limit
        if len(self.short_term_memory) > self.max_short_term_size:
            # Move oldest to long-term memory
            oldest = self.short_term_memory.pop(0)
            oldest["type"] = "long_term"
            self._store_long_term_memory(oldest)

    def _store_long_term_memory(self, memory_object):
        """Store in long-term memory with compression"""
        memory_id = memory_object["id"]
        compressed_memory = self._compress_memory(memory_object)
        self.long_term_memory[memory_id] = compressed_memory

    def _store_semantic_memory(self, memory_object):
        """Store factual knowledge"""
        # Extract key concepts for semantic storage
        concepts = self._extract_concepts(memory_object["content"])
        for concept in concepts:
            if concept not in self.semantic_memory:
                self.semantic_memory[concept] = []
            self.semantic_memory[concept].append(memory_object["id"])

    def _store_procedural_memory(self, memory_object):
        """Store procedural knowledge (how-to)"""
        procedures = self._extract_procedures(memory_object["content"])
        for procedure in procedures:
            if procedure not in self.procedural_memory:
                self.procedural_memory[procedure] = []
            self.procedural_memory[procedure].append(memory_object["id"])

    def _store_working_memory(self, memory_object):
        """Store in working memory (limited capacity)"""
        memory_id = memory_object["id"]

        # Check if we need to evict something
        if len(self.working_memory) >= self.max_working_memory_size:
            self._evict_least_recently_used()

        self.working_memory[memory_id] = memory_object

    def retrieve_memory(self, query: str, memory_type: str = None,
                       tags: List[str] = None, limit: int = 10) -> List[Dict]:
        """Retrieve memories based on query and criteria"""
        with self.memory_lock:
            try:
                self.memory_stats["retrieval_requests"] += 1

                candidates = []
                all_memories = self._get_all_memories()

                for memory_id, memory in all_memories.items():
                    # Filter by type
                    if memory_type and memory.get("type") != memory_type:
                        continue

                    # Filter by tags
                    if tags:
                        memory_tags = set(memory.get("tags", []))
                        if not set(tags).intersection(memory_tags):
                            continue

                    # Calculate relevance score
                    relevance_score = self._calculate_relevance(query, memory)

                    if relevance_score > 0:
                        candidates.append((relevance_score, memory))

                # Sort by relevance and return top results
                candidates.sort(key=lambda x: x[0], reverse=True)
                results = [memory for _, memory in candidates[:limit]]

                # Update access patterns
                for memory in results:
                    self._update_memory_access(memory["id"])

                self.memory_stats["memory_hits"] += len(results)
                return results

            except Exception as e:
                print(f"⚠️  Memory retrieval error: {e}")
                self.memory_stats["memory_misses"] += 1
                return []

    def _get_all_memories(self) -> Dict[str, Dict]:
        """Get all memories in a unified format"""
        all_memories = {}

        # Add episodic memories
        for memory in self.episodic_memory:
            all_memories[memory["id"]] = memory

        # Add long-term memories
        all_memories.update(self.long_term_memory)

        # Add working memories
        all_memories.update(self.working_memory)

        return all_memories

    def _calculate_relevance(self, query: str, memory: Dict) -> float:
        """Calculate relevance score between query and memory"""
        try:
            content = str(memory.get("content", ""))
            query_lower = query.lower()
            content_lower = content.lower()

            # Exact match bonus
            if query_lower in content_lower:
                return 1.0

            # Word overlap score
            query_words = set(query_lower.split())
            content_words = set(content_lower.split())
            overlap = len(query_words.intersection(content_words))

            if overlap == 0:
                return 0.0

            # Calculate score based on overlap and memory strength
            base_score = overlap / len(query_words)
            strength_bonus = memory.get("strength", 1.0) * 0.1
            recency_bonus = self._calculate_recency_bonus(memory)

            return min(1.0, base_score + strength_bonus + recency_bonus)

        except Exception:
            return 0.0

    def _calculate_recency_bonus(self, memory: Dict) -> float:
        """Calculate bonus based on memory recency"""
        try:
            last_access = memory.get("last_access", memory.get("timestamp"))
            last_access_dt = datetime.fromisoformat(last_access)
            hours_old = (datetime.now() - last_access_dt).total_seconds() / 3600

            # Recent memories get bonus
            if hours_old < 1:
                return 0.3
            elif hours_old < 24:
                return 0.2
            elif hours_old < 168:  # 1 week
                return 0.1
            else:
                return 0.0

        except Exception:
            return 0.0

    def _update_memory_access(self, memory_id: str):
        """Update memory access patterns"""
        try:
            # Update access count and timestamp
            all_memories = self._get_all_memories()
            if memory_id in all_memories:
                memory = all_memories[memory_id]
                memory["access_count"] = memory.get("access_count", 0) + 1
                memory["last_access"] = datetime.now().isoformat()

                # Strengthen memory through access
                current_strength = memory.get("strength", 1.0)
                memory["strength"] = min(2.0, current_strength + 0.1)

                self.memory_strength[memory_id] = memory["strength"]

        except Exception as e:
            print(f"⚠️  Memory access update error: {e}")

    def create_memory_association(self, memory_id1: str, memory_id2: str,
                                 association_type: str = "related"):
        """Create association between memories"""
        with self.memory_lock:
            try:
                # Add bidirectional association
                if memory_id2 not in self.memory_associations[memory_id1]:
                    self.memory_associations[memory_id1].append({
                        "target_id": memory_id2,
                        "type": association_type,
                        "strength": 1.0,
                        "created": datetime.now().isoformat()
                    })

                if memory_id1 not in self.memory_associations[memory_id2]:
                    self.memory_associations[memory_id2].append({
                        "target_id": memory_id1,
                        "type": association_type,
                        "strength": 1.0,
                        "created": datetime.now().isoformat()
                    })

            except Exception as e:
                print(f"⚠️  Memory association error: {e}")

    def get_related_memories(self, memory_id: str, limit: int = 5) -> List[Dict]:
        """Get memories related to given memory"""
        try:
            related_ids = []
            associations = self.memory_associations.get(memory_id, [])

            for association in associations:
                related_ids.append(association["target_id"])

            # Retrieve related memories
            related_memories = []
            all_memories = self._get_all_memories()

            for related_id in related_ids[:limit]:
                if related_id in all_memories:
                    related_memories.append(all_memories[related_id])

            return related_memories

        except Exception as e:
            print(f"⚠️  Related memory retrieval error: {e}")
            return []

    def _memory_consolidation_loop(self):
        """Background memory consolidation"""
        while True:
            try:
                time.sleep(300)  # 5 minutes

                # Check if consolidation is needed
                if len(self.short_term_memory) >= self.consolidation_threshold:
                    self._consolidate_short_term_memories()

                # Consolidate weak long-term memories
                self._consolidate_weak_memories()

            except Exception as e:
                print(f"⚠️  Memory consolidation error: {e}")
                time.sleep(60)

    def _consolidate_short_term_memories(self):
        """Consolidate short-term memories into long-term"""
        with self.memory_lock:
            try:
                print("🔄 CONSOLIDATING SHORT-TERM MEMORIES...")

                # Group related memories
                memory_groups = self._group_related_memories(self.short_term_memory)

                consolidated_count = 0
                for group in memory_groups:
                    if len(group) > 1:
                        # Create consolidated memory
                        consolidated = self._create_consolidated_memory(group)
                        self._store_long_term_memory(consolidated)
                        consolidated_count += len(group)

                        # Remove from short-term
                        for memory in group:
                            if memory in self.short_term_memory:
                                self.short_term_memory.remove(memory)

                self.memory_stats["consolidation_cycles"] += 1
                print(f"✅ Consolidated {consolidated_count} memories into {len(memory_groups)} groups")

            except Exception as e:
                print(f"⚠️  Short-term consolidation error: {e}")

    def _group_related_memories(self, memories: List[Dict]) -> List[List[Dict]]:
        """Group memories by similarity"""
        groups = []

        for memory in memories:
            # Find best group
            best_group = None
            best_similarity = 0

            for group in groups:
                similarity = self._calculate_memory_similarity(memory, group[0])
                if similarity > 0.3 and similarity > best_similarity:
                    best_group = group
                    best_similarity = similarity

            if best_group:
                best_group.append(memory)
            else:
                groups.append([memory])

        return groups

    def _calculate_memory_similarity(self, memory1: Dict, memory2: Dict) -> float:
        """Calculate similarity between two memories"""
        try:
            content1 = str(memory1.get("content", ""))
            content2 = str(memory2.get("content", ""))

            # Simple word overlap similarity
            words1 = set(content1.lower().split())
            words2 = set(content2.lower().split())

            if not words1 or not words2:
                return 0.0

            overlap = len(words1.intersection(words2))
            union = len(words1.union(words2))

            return overlap / union if union > 0 else 0.0

        except Exception:
            return 0.0

    def _create_consolidated_memory(self, memory_group: List[Dict]) -> Dict:
        """Create consolidated memory from group"""
        try:
            # Combine contents
            combined_content = []
            all_tags = set()
            total_importance = 0
            total_access_count = 0

            for memory in memory_group:
                combined_content.append(str(memory.get("content", "")))
                all_tags.update(memory.get("tags", []))
                total_importance += memory.get("importance", 1.0)
                total_access_count += memory.get("access_count", 0)

            consolidated_content = " | ".join(combined_content)

            # Create consolidated memory object
            consolidated = {
                "id": self._generate_memory_id(consolidated_content),
                "content": consolidated_content,
                "type": "long_term",
                "tags": list(all_tags),
                "importance": total_importance / len(memory_group),
                "timestamp": datetime.now().isoformat(),
                "access_count": total_access_count,
                "last_access": datetime.now().isoformat(),
                "strength": total_importance / len(memory_group),
                "associations": [],
                "consolidated_from": [m["id"] for m in memory_group],
                "consolidation_timestamp": datetime.now().isoformat()
            }

            return consolidated

        except Exception as e:
            print(f"⚠️  Memory consolidation creation error: {e}")
            return memory_group[0]  # Return first memory if consolidation fails

    def _consolidate_weak_memories(self):
        """Consolidate or remove weak memories"""
        try:
            weak_threshold = 0.3
            weak_memories = []

            # Find weak memories
            for memory_id, strength in self.memory_strength.items():
                if strength < weak_threshold:
                    weak_memories.append(memory_id)

            # Consolidate or remove weak memories
            for memory_id in weak_memories[:10]:  # Process 10 at a time
                if random.random() < 0.5:  # 50% chance to consolidate
                    self._consolidate_weak_memory(memory_id)
                else:
                    self._remove_memory(memory_id)

        except Exception as e:
            print(f"⚠️  Weak memory consolidation error: {e}")

    def _consolidate_weak_memory(self, memory_id: str):
        """Consolidate weak memory with related memories"""
        try:
            related_memories = self.get_related_memories(memory_id, limit=3)
            if related_memories:
                # Create consolidated memory
                all_memories = [self._get_memory_by_id(memory_id)] + related_memories
                consolidated = self._create_consolidated_memory(all_memories)

                # Replace original with consolidated
                self._store_long_term_memory(consolidated)
                self._remove_memory(memory_id)

        except Exception as e:
            print(f"⚠️  Weak memory consolidation error: {e}")

    def _memory_cleanup_loop(self):
        """Background memory cleanup and optimization"""
        while True:
            try:
                time.sleep(600)  # 10 minutes

                # Apply forgetfulness to unused memories
                self._apply_forgetfulness()

                # Clean up orphaned data
                self._cleanup_orphaned_data()

                # Update memory statistics
                self.memory_stats["last_cleanup"] = datetime.now().isoformat()

            except Exception as e:
                print(f"⚠️  Memory cleanup error: {e}")
                time.sleep(120)

    def _apply_forgetfulness(self):
        """Apply forgetfulness to unused memories"""
        try:
            forgetfulness_threshold = 0.2

            memories_to_weaken = []
            for memory_id, strength in list(self.memory_strength.items()):
                if strength > forgetfulness_threshold:
                    memories_to_weaken.append(memory_id)

            # Weaken random subset of memories
            weaken_count = int(len(memories_to_weaken) * self.forgetfulness_rate)
            to_weaken = random.sample(memories_to_weaken, min(weaken_count, 50))

            for memory_id in to_weaken:
                self.memory_strength[memory_id] *= 0.95  # Reduce strength by 5%

        except Exception as e:
            print(f"⚠️  Forgetfulness application error: {e}")

    def _cleanup_orphaned_data(self):
        """Clean up orphaned memory data"""
        try:
            # Remove associations to non-existent memories
            valid_memory_ids = set(self._get_all_memories().keys())

            for memory_id in list(self.memory_associations.keys()):
                if memory_id not in valid_memory_ids:
                    del self.memory_associations[memory_id]
                else:
                    # Clean up invalid associations
                    self.memory_associations[memory_id] = [
                        assoc for assoc in self.memory_associations[memory_id]
                        if assoc["target_id"] in valid_memory_ids
                    ]

            # Remove strength data for non-existent memories
            for memory_id in list(self.memory_strength.keys()):
                if memory_id not in valid_memory_ids:
                    del self.memory_strength[memory_id]

            # Remove timestamp data for non-existent memories
            for memory_id in list(self.memory_timestamp.keys()):
                if memory_id not in valid_memory_ids:
                    del self.memory_timestamp[memory_id]

        except Exception as e:
            print(f"⚠️  Orphaned data cleanup error: {e}")

    def _generate_memory_id(self, content: Any) -> str:
        """Generate unique memory ID"""
        content_str = str(content) + str(datetime.now().timestamp())
        return hashlib.md5(content_str.encode()).hexdigest()[:16]

    def _compress_memory(self, memory: Dict) -> Dict:
        """Compress memory for long-term storage"""
        try:
            # Simple compression: summarize if content is too long
            content = str(memory.get("content", ""))
            if len(content) > 1000:
                memory["original_content"] = content
                memory["content"] = content[:500] + "...[COMPRESSED]"
                memory["compressed"] = True

            return memory

        except Exception:
            return memory

    def _extract_concepts(self, content: Any) -> List[str]:
        """Extract key concepts from content"""
        # Simple keyword extraction (in real implementation, use NLP)
        content_str = str(content).lower()
        words = content_str.split()
        concepts = [word for word in words if len(word) > 4]  # Simple heuristic
        return list(set(concepts))[:10]  # Top 10 concepts

    def _extract_procedures(self, content: Any) -> List[str]:
        """Extract procedural knowledge"""
        # Simple procedure extraction
        content_str = str(content).lower()
        procedures = []

        # Look for action words
        action_words = ["how", "process", "method", "steps", "procedure", "guide"]
        for word in action_words:
            if word in content_str:
                procedures.append(word)

        return list(set(procedures))

    def _evict_least_recently_used(self):
        """Evict least recently used memory from working memory"""
        try:
            if not self.working_memory:
                return

            # Find oldest access time
            oldest_id = None
            oldest_time = datetime.now()

            for memory_id, memory in self.working_memory.items():
                last_access = memory.get("last_access", memory.get("timestamp"))
                access_time = datetime.fromisoformat(last_access)

                if access_time < oldest_time:
                    oldest_time = access_time
                    oldest_id = memory_id

            # Move to long-term and remove from working
            if oldest_id:
                memory = self.working_memory[oldest_id]
                memory["type"] = "long_term"
                self._store_long_term_memory(memory)
                del self.working_memory[oldest_id]

        except Exception as e:
            print(f"⚠️  LRU eviction error: {e}")

    def _get_memory_by_id(self, memory_id: str) -> Optional[Dict]:
        """Get memory by ID"""
        all_memories = self._get_all_memories()
        return all_memories.get(memory_id)

    def _remove_memory(self, memory_id: str):
        """Remove memory from all storage locations"""
        try:
            # Remove from all memory types
            all_memories = self._get_all_memories()
            if memory_id in all_memories:
                memory = all_memories[memory_id]

                if memory["type"] == "episodic":
                    self.episodic_memory = [m for m in self.episodic_memory if m["id"] != memory_id]
                elif memory["type"] == "long_term" and memory_id in self.long_term_memory:
                    del self.long_term_memory[memory_id]
                elif memory["type"] == "working" and memory_id in self.working_memory:
                    del self.working_memory[memory_id]

            # Clean up metadata
            if memory_id in self.memory_strength:
                del self.memory_strength[memory_id]
            if memory_id in self.memory_timestamp:
                del self.memory_timestamp[memory_id]
            if memory_id in self.memory_associations:
                del self.memory_associations[memory_id]

        except Exception as e:
            print(f"⚠️  Memory removal error: {e}")

    def _load_memory_state(self):
        """Load memory state from disk"""
        try:
            memory_file = "memory_state.json"
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    state = json.load(f)

                self.long_term_memory = state.get("long_term_memory", {})
                self.semantic_memory = state.get("semantic_memory", {})
                self.procedural_memory = state.get("procedural_memory", {})
                self.memory_strength = state.get("memory_strength", {})
                self.memory_associations = state.get("memory_associations", {})
                self.memory_tags = state.get("memory_tags", {})
                self.memory_timestamp = state.get("memory_timestamp", {})

                print("✅ Memory state loaded from disk")

        except Exception as e:
            print(f"⚠️  Memory state loading error: {e}")

    def save_memory_state(self):
        """Save memory state to disk"""
        try:
            state = {
                "long_term_memory": self.long_term_memory,
                "semantic_memory": self.semantic_memory,
                "procedural_memory": self.procedural_memory,
                "memory_strength": self.memory_strength,
                "memory_associations": self.memory_associations,
                "memory_tags": self.memory_tags,
                "memory_timestamp": self.memory_timestamp,
                "memory_stats": self.memory_stats,
                "saved_at": datetime.now().isoformat()
            }

            with open("memory_state.json", 'w') as f:
                json.dump(state, f, indent=2)

            print("💾 Memory state saved to disk")

        except Exception as e:
            print(f"⚠️  Memory state saving error: {e}")

    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        with self.memory_lock:
            try:
                stats = {
                    "memory_stats": self.memory_stats,
                    "short_term_count": len(self.short_term_memory),
                    "long_term_count": len(self.long_term_memory),
                    "episodic_count": len(self.episodic_memory),
                    "working_memory_count": len(self.working_memory),
                    "semantic_concepts": len(self.semantic_memory),
                    "procedural_knowledge": len(self.procedural_memory),
                    "total_associations": sum(len(assoc) for assoc in self.memory_associations.values()),
                    "average_memory_strength": sum(self.memory_strength.values()) / max(len(self.memory_strength), 1),
                    "memory_types_distribution": self._get_memory_type_distribution(),
                    "retrieval_accuracy": self._calculate_retrieval_accuracy(),
                    "consolidation_efficiency": self._calculate_consolidation_efficiency()
                }

                return stats

            except Exception as e:
                print(f"⚠️  Memory statistics error: {e}")
                return {"error": str(e)}

    def _get_memory_type_distribution(self) -> Dict[str, int]:
        """Get distribution of memory types"""
        distribution = defaultdict(int)
        all_memories = self._get_all_memories()

        for memory in all_memories.values():
            distribution[memory.get("type", "unknown")] += 1

        return dict(distribution)

    def _calculate_retrieval_accuracy(self) -> float:
        """Calculate memory retrieval accuracy"""
        total_requests = self.memory_stats["retrieval_requests"]
        if total_requests == 0:
            return 0.0

        accuracy = self.memory_stats["memory_hits"] / total_requests
        return round(accuracy * 100, 2)

    def _calculate_consolidation_efficiency(self) -> float:
        """Calculate memory consolidation efficiency"""
        if self.memory_stats["consolidation_cycles"] == 0:
            return 0.0

        # Efficiency based on compression and retention
        efficiency = min(100.0, len(self.long_term_memory) * 2)
        return round(efficiency, 2)

    def search_memories(self, query: str, search_type: str = "semantic",
                       limit: int = 20) -> List[Dict]:
        """Advanced memory search with different strategies"""
        try:
            if search_type == "semantic":
                return self._semantic_search(query, limit)
            elif search_type == "temporal":
                return self._temporal_search(query, limit)
            elif search_type == "associative":
                return self._associative_search(query, limit)
            elif search_type == "tag_based":
                return self._tag_based_search(query, limit)
            else:
                return self.retrieve_memory(query, limit=limit)

        except Exception as e:
            print(f"⚠️  Memory search error: {e}")
            return []

    def _semantic_search(self, query: str, limit: int) -> List[Dict]:
        """Search memories based on semantic meaning"""
        # Use enhanced retrieval with semantic understanding
        return self.retrieve_memory(query, limit=limit)

    def _temporal_search(self, query: str, limit: int) -> List[Dict]:
        """Search memories based on temporal patterns"""
        try:
            all_memories = self._get_all_memories()
            temporal_memories = []

            for memory in all_memories.values():
                timestamp = memory.get("timestamp")
                if timestamp:
                    # Check if memory matches temporal pattern in query
                    if "recent" in query.lower() and self._is_recent_memory(timestamp):
                        temporal_memories.append(memory)
                    elif "old" in query.lower() and not self._is_recent_memory(timestamp):
                        temporal_memories.append(memory)

            return temporal_memories[:limit]

        except Exception:
            return []

    def _is_recent_memory(self, timestamp: str) -> bool:
        """Check if memory is recent (within 24 hours)"""
        try:
            memory_time = datetime.fromisoformat(timestamp)
            return (datetime.now() - memory_time).total_seconds() < 86400
        except Exception:
            return False

    def _associative_search(self, query: str, limit: int) -> List[Dict]:
        """Search memories using association networks"""
        try:
            # Find initial memories
            initial_memories = self.retrieve_memory(query, limit=5)

            associated_memories = []
            for memory in initial_memories:
                associated = self.get_related_memories(memory["id"], limit=3)
                associated_memories.extend(associated)

            # Remove duplicates
            seen_ids = set()
            unique_associated = []
            for memory in associated_memories:
                if memory["id"] not in seen_ids:
                    unique_associated.append(memory)
                    seen_ids.add(memory["id"])

            return unique_associated[:limit]

        except Exception:
            return []

    def _tag_based_search(self, query: str, limit: int) -> List[Dict]:
        """Search memories based on tags"""
        try:
            # Extract potential tags from query
            query_words = set(query.lower().split())
            matching_memories = []

            for tag, memory_ids in self.memory_tags.items():
                if tag.lower() in query_words:
                    for memory_id in memory_ids:
                        memory = self._get_memory_by_id(memory_id)
                        if memory:
                            matching_memories.append(memory)

            return matching_memories[:limit]

        except Exception:
            return []

    def shutdown(self):
        """Graceful shutdown with memory preservation"""
        print("🧠 ENHANCED MEMORY SYSTEM SHUTTING DOWN...")
        self.save_memory_state()
        print("✅ Memory state saved")
        print("✅ Memory system shutdown complete")

# Global memory system instance
memory_system = None

def initialize_memory_system():
    """Initialize the Enhanced Memory System"""
    global memory_system
    if memory_system is None:
        memory_system = EnhancedMemorySystem()
    return memory_system

def store_memory(content, memory_type="episodic", tags=None, importance=1.0):
    """Store memory in the system"""
    if memory_system:
        return memory_system.store_memory(content, memory_type, tags, importance)
    else:
        return None

def retrieve_memory(query, memory_type=None, tags=None, limit=10):
    """Retrieve memories from the system"""
    if memory_system:
        return memory_system.retrieve_memory(query, memory_type, tags, limit)
    else:
        return []

def get_memory_stats():
    """Get memory system statistics"""
    if memory_system:
        return memory_system.get_memory_statistics()
    else:
        return {"status": "memory_system_not_initialized"}

def search_memories(query, search_type="semantic", limit=20):
    """Search memories using advanced techniques"""
    if memory_system:
        return memory_system.search_memories(query, search_type, limit)
    else:
        return []

# Auto-initialize when imported
if __name__ == "__main__":
    print("🧠 ENHANCED MEMORY SYSTEM")
    print("=" * 35)
    memory = initialize_memory_system()

    # Demonstration
    try:
        while True:
            # Store some test memories
            test_memories = [
                "AGI integration test completed successfully",
                "Memory consolidation improved system performance",
                "Autonomous optimization cycle running smoothly",
                "Empire monitoring detected performance anomaly",
                "Creative intelligence generated breakthrough insight"
            ]

            for memory_content in test_memories:
                memory_id = store_memory(memory_content, tags=["test", "agi"])
                print(f"💾 Stored memory: {memory_id}")

            # Test retrieval
            results = retrieve_memory("AGI")
            print(f"🔍 Retrieved {len(results)} memories for 'AGI'")

            # Show statistics
            stats = get_memory_stats()
            print(f"📊 Memory stats: {stats['memory_stats']['total_memories']} total memories")

            time.sleep(30)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down memory system...")
        memory.shutdown()







