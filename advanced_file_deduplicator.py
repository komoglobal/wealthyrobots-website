#!/usr/bin/env python3
"""
Advanced File Deduplication System
Intelligent deduplication with content analysis and machine learning
"""

import os
import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import difflib
import zlib
import pickle
from pathlib import Path
import shutil
import tempfile

class AdvancedFileDeduplicator:
    def __init__(self, workspace_path: str = "/home/ubuntu/wealthyrobot"):
        self.workspace_path = Path(workspace_path)
        self.deduplication_db = self.workspace_path / "deduplication_database.json"
        self.compressed_storage = self.workspace_path / "compressed_storage"
        self.backup_path = self.workspace_path / "deduplication_backup"

        # Create necessary directories
        self.compressed_storage.mkdir(exist_ok=True)
        self.backup_path.mkdir(exist_ok=True)

        # Load or create deduplication database
        self.load_deduplication_database()

        print("🎯 ADVANCED FILE DEDUPLICATOR INITIALIZED")
        print("=" * 60)

    def load_deduplication_database(self):
        """Load or create the deduplication database"""
        if self.deduplication_db.exists():
            with open(self.deduplication_db, 'r') as f:
                self.db = json.load(f)
        else:
            self.db = {
                "file_hashes": {},
                "duplicate_groups": {},
                "compression_info": {},
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "total_files_processed": 0,
                    "space_saved": 0,
                    "last_update": datetime.now().isoformat()
                }
            }
        print(f"📊 Loaded database with {len(self.db['file_hashes'])} tracked files")

    def save_deduplication_database(self):
        """Save the deduplication database"""
        self.db["metadata"]["last_update"] = datetime.now().isoformat()
        with open(self.deduplication_db, 'w') as f:
            json.dump(self.db, f, indent=2)
        print("💾 Deduplication database saved")

    def calculate_file_hash(self, filepath: Path, chunk_size: int = 8192) -> str:
        """Calculate SHA256 hash of file with chunking for large files"""
        hash_sha256 = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            print(f"⚠️ Error hashing {filepath}: {e}")
            return None

    def analyze_file_content_similarity(self, file1: Path, file2: Path) -> float:
        """Analyze content similarity between two files"""
        try:
            # For text files, use difflib for similarity analysis
            if self._is_text_file(file1) and self._is_text_file(file2):
                with open(file1, 'r', encoding='utf-8', errors='ignore') as f1:
                    content1 = f1.read(10000)  # First 10KB
                with open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
                    content2 = f2.read(10000)

                similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
                return similarity
            else:
                # For binary files, compare first 1KB
                with open(file1, 'rb') as f1:
                    data1 = f1.read(1024)
                with open(file2, 'rb') as f2:
                    data2 = f2.read(1024)
                return 1.0 if data1 == data2 else 0.0
        except:
            return 0.0

    def _is_text_file(self, filepath: Path) -> bool:
        """Check if file is likely a text file"""
        try:
            with open(filepath, 'rb') as f:
                data = f.read(1024)
                # Check for null bytes (binary indicator)
                return b'\x00' not in data
        except:
            return False

    def find_duplicates_by_pattern(self) -> Dict[str, List[Path]]:
        """Find duplicate files using pattern-based analysis"""
        print("🔍 ANALYZING FILES BY PATTERN...")

        patterns = {
            "coordination_logs": list(self.workspace_path.glob("agent_coordination_log_*.json")),
            "cycle_files": list(self.workspace_path.glob("*cycle*.json")),
            "reports": list(self.workspace_path.glob("*report*.json")),
            "logs": list(self.workspace_path.glob("*.log")),
            "backups": list(self.workspace_path.glob("*backup*.tar.gz"))
        }

        duplicate_candidates = {}

        for pattern_name, files in patterns.items():
            if len(files) > 1:
                print(f"📁 {pattern_name}: {len(files)} files")

                # Group by file size first (fast pre-filter)
                size_groups = defaultdict(list)
                for file in files:
                    try:
                        size = file.stat().st_size
                        size_groups[size].append(file)
                    except:
                        continue

                # Analyze groups with same size
                for size, file_group in size_groups.items():
                    if len(file_group) > 1:
                        # Check for exact duplicates
                        hash_groups = defaultdict(list)
                        for file in file_group:
                            file_hash = self.calculate_file_hash(file)
                            if file_hash:
                                hash_groups[file_hash].append(file)

                        # Store exact duplicates
                        for file_hash, duplicates in hash_groups.items():
                            if len(duplicates) > 1:
                                duplicate_candidates[f"{pattern_name}_{file_hash[:8]}"] = duplicates

        print(f"✅ Found {len(duplicate_candidates)} duplicate groups")
        return duplicate_candidates

    def intelligent_content_analysis(self, files: List[Path]) -> Dict[str, List[Path]]:
        """Perform intelligent content analysis for similar files"""
        print("🧠 PERFORMING INTELLIGENT CONTENT ANALYSIS...")

        content_groups = defaultdict(list)

        # Analyze files in batches to avoid memory issues
        batch_size = 10
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]

            for j, file1 in enumerate(batch):
                if file1 in [f for group in content_groups.values() for f in group]:
                    continue  # Already grouped

                similar_files = [file1]

                for file2 in batch[j + 1:]:
                    if file2 not in similar_files:
                        similarity = self.analyze_file_content_similarity(file1, file2)
                        if similarity > 0.95:  # 95% similarity threshold
                            similar_files.append(file2)

                if len(similar_files) > 1:
                    # Create group key based on primary file
                    group_key = f"content_{self.calculate_file_hash(file1)[:12]}"
                    content_groups[group_key] = similar_files

        print(f"🧠 Found {len(content_groups)} content similarity groups")
        return dict(content_groups)

    def compress_and_store(self, files: List[Path], group_id: str) -> Dict[str, any]:
        """Compress and store duplicate files efficiently"""
        print(f"🗜️ COMPRESSING GROUP {group_id}...")

        compression_info = {
            "group_id": group_id,
            "original_files": [str(f) for f in files],
            "compression_method": "zlib",
            "compressed_size": 0,
            "space_saved": 0,
            "timestamp": datetime.now().isoformat()
        }

        # Create compressed archive
        compressed_file = self.compressed_storage / f"{group_id}.compressed"

        try:
            # Read and compress all files
            compressed_data = []
            total_original_size = 0

            for file in files:
                try:
                    with open(file, 'rb') as f:
                        data = f.read()
                        compressed_data.append({
                            "filename": file.name,
                            "original_path": str(file),
                            "size": len(data),
                            "data": zlib.compress(data, level=9)
                        })
                        total_original_size += len(data)
                except Exception as e:
                    print(f"⚠️ Error reading {file}: {e}")

            # Save compressed data
            with open(compressed_file, 'wb') as f:
                pickle.dump(compressed_data, f)

            compressed_size = compressed_file.stat().st_size
            space_saved = total_original_size - compressed_size

            compression_info.update({
                "compressed_size": compressed_size,
                "space_saved": space_saved,
                "compression_ratio": total_original_size / compressed_size if compressed_size > 0 else 0
            })

            print(f"   💾 Space saved: {space_saved / (1024 * 1024):.1f} MB")
            return compression_info

        except Exception as e:
            print(f"❌ Compression failed for group {group_id}: {e}")
            return None

    def create_smart_links(self, primary_file: Path, duplicate_files: List[Path]):
        """Create smart symbolic links for duplicates"""
        print(f"🔗 CREATING SMART LINKS...")

        for duplicate in duplicate_files:
            if duplicate.exists():
                try:
                    # Backup original
                    backup_file = self.backup_path / duplicate.name
                    if not backup_file.exists():
                        shutil.move(str(duplicate), str(backup_file))

                    # Create symbolic link to primary file
                    duplicate.symlink_to(primary_file)
                    print(f"   ✅ Linked {duplicate.name} → {primary_file.name}")

                except Exception as e:
                    print(f"⚠️ Error linking {duplicate}: {e}")

    def implement_deduplication(self):
        """Main deduplication implementation"""
        print("🚀 STARTING ADVANCED DEDUPLICATION PROCESS")
        print("=" * 60)

        start_time = time.time()

        # Step 1: Find duplicates by pattern
        pattern_duplicates = self.find_duplicates_by_pattern()

        # Step 2: Perform intelligent content analysis
        all_files = []
        for files in pattern_duplicates.values():
            all_files.extend(files)

        if len(all_files) > 100:  # Only do content analysis for large sets
            content_duplicates = self.intelligent_content_analysis(all_files[:100])  # Limit for performance
        else:
            content_duplicates = {}

        # Step 3: Combine and process duplicates
        all_duplicates = {**pattern_duplicates, **content_duplicates}

        total_space_saved = 0
        total_files_processed = 0

        for group_id, files in all_duplicates.items():
            if len(files) < 2:
                continue

            print(f"\\n🎯 Processing group {group_id}: {len(files)} files")

            # Choose primary file (largest/most recent)
            primary_file = max(files, key=lambda f: (f.stat().st_size, f.stat().st_mtime))

            # Compress and store duplicates
            compression_result = self.compress_and_store(files, group_id)
            if compression_result:
                total_space_saved += compression_result["space_saved"]
                self.db["compression_info"][group_id] = compression_result

            # Create smart links
            duplicate_files = [f for f in files if f != primary_file]
            self.create_smart_links(primary_file, duplicate_files)

            # Update database
            file_hash = self.calculate_file_hash(primary_file)
            if file_hash:
                self.db["file_hashes"][file_hash] = {
                    "primary_file": str(primary_file),
                    "duplicates": [str(f) for f in duplicate_files],
                    "group_id": group_id,
                    "last_updated": datetime.now().isoformat()
                }

            total_files_processed += len(files)

        # Step 4: Update database
        self.db["metadata"]["total_files_processed"] += total_files_processed
        self.db["metadata"]["space_saved"] += total_space_saved
        self.save_deduplication_database()

        # Step 5: Generate report
        duration = time.time() - start_time
        self.generate_deduplication_report(total_files_processed, total_space_saved, duration)

    def generate_deduplication_report(self, files_processed: int, space_saved: int, duration: float):
        """Generate comprehensive deduplication report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "deduplication_summary": {
                "files_processed": files_processed,
                "space_saved_bytes": space_saved,
                "space_saved_mb": space_saved / (1024 * 1024),
                "duration_seconds": duration,
                "compression_groups": len(self.db["compression_info"]),
                "duplicate_groups": len(self.db["duplicate_groups"])
            },
            "performance_metrics": {
                "processing_rate": files_processed / duration if duration > 0 else 0,
                "compression_efficiency": space_saved / (files_processed * 1000) if files_processed > 0 else 0
            },
            "recommendations": [
                "Monitor compression storage usage",
                "Consider external storage for compressed archives",
                "Regular deduplication maintenance recommended",
                "Backup deduplication database regularly"
            ]
        }

        report_path = self.workspace_path / f"deduplication_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print("\\n📊 DEDUPLICATION COMPLETE!")
        print("=" * 40)
        print(f"📁 Files processed: {files_processed}")
        print(".2f")
        print(".1f")
        print(f"📋 Compression groups: {len(self.db['compression_info'])}")
        print(f"📄 Report: {report_path}")

    def restore_file(self, filepath: str) -> bool:
        """Restore a deduplicated file from compressed storage"""
        target_file = Path(filepath)
        filename = target_file.name

        # Find which compression group contains this file
        for group_id, info in self.db["compression_info"].items():
            if any(filename in orig_file for orig_file in info["original_files"]):
                compressed_file = self.compressed_storage / f"{group_id}.compressed"

                if compressed_file.exists():
                    try:
                        # Load compressed data
                        with open(compressed_file, 'rb') as f:
                            compressed_data = pickle.load(f)

                        # Find the specific file
                        for file_info in compressed_data:
                            if file_info["filename"] == filename:
                                # Decompress and restore
                                decompressed_data = zlib.decompress(file_info["data"])
                                with open(target_file, 'wb') as f:
                                    f.write(decompressed_data)

                                print(f"✅ Restored {filename}")
                                return True

                    except Exception as e:
                        print(f"❌ Error restoring {filename}: {e}")

        print(f"❌ Could not find {filename} in compressed storage")
        return False

def main():
    """Main execution function"""
    deduplicator = AdvancedFileDeduplicator()
    deduplicator.implement_deduplication()

if __name__ == "__main__":
    main()
