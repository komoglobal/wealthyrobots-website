#!/usr/bin/env python3
"""
Large File Optimization System
Compress, archive, and chunk large files for optimal storage
"""

import os
import json
import gzip
import bz2
import lzma
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import hashlib
import subprocess
import tarfile

class LargeFileOptimizer:
    def __init__(self, workspace_path: str = "/home/ubuntu/wealthyrobot"):
        self.workspace_path = Path(workspace_path)
        self.archive_path = self.workspace_path / "optimized_archives"
        self.chunk_storage = self.workspace_path / "file_chunks"
        self.backup_path = self.workspace_path / "large_file_backup"

        # Create directories
        for path in [self.archive_path, self.chunk_storage, self.backup_path]:
            path.mkdir(exist_ok=True)

        # Configuration
        self.large_file_threshold = 10 * 1024 * 1024  # 10MB
        self.chunk_size = 100 * 1024 * 1024  # 100MB chunks
        self.compression_methods = ['gzip', 'bz2', 'lzma']

        print("📦 LARGE FILE OPTIMIZER INITIALIZED")
        print("=" * 50)

    def scan_large_files(self) -> List[Dict[str, any]]:
        """Scan workspace for large files"""
        print("🔍 SCANNING FOR LARGE FILES...")

        large_files = []

        for root, dirs, files in os.walk(self.workspace_path):
            # Skip our optimization directories
            if any(skip in root for skip in ['optimized_archives', 'file_chunks', 'large_file_backup', '__pycache__', '.git']):
                continue

            for file in files:
                filepath = Path(root) / file
                try:
                    file_stat = filepath.stat()
                    size_mb = file_stat.st_size / (1024 * 1024)

                    if file_stat.st_size >= self.large_file_threshold:
                        file_info = {
                            "path": str(filepath),
                            "size_bytes": file_stat.st_size,
                            "size_mb": size_mb,
                            "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                            "file_type": self._get_file_type(filepath),
                            "compressible": self._is_compressible(filepath)
                        }
                        large_files.append(file_info)
                        print(f"   📁 Large file: {size_mb:.1f} MB")
                except Exception as e:
                    print(f"⚠️ Error scanning {filepath}: {e}")

        # Sort by size (largest first)
        large_files.sort(key=lambda x: x['size_bytes'], reverse=True)

        print(f"📊 Found {len(large_files)} large files")
        return large_files

    def _get_file_type(self, filepath: Path) -> str:
        """Determine file type for optimization strategy"""
        if filepath.suffix.lower() in ['.log', '.txt', '.json', '.py', '.md', '.csv', '.xml']:
            return "text"
        elif filepath.suffix.lower() in ['.gz', '.bz2', '.xz', '.zip', '.tar']:
            return "compressed"
        elif filepath.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
            return "image"
        elif filepath.suffix.lower() in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']:
            return "video"
        elif filepath.suffix.lower() in ['.mp3', '.wav', '.flac', '.aac']:
            return "audio"
        else:
            return "binary"

    def _is_compressible(self, filepath: Path) -> bool:
        """Check if file is likely compressible"""
        file_type = self._get_file_type(filepath)
        return file_type in ["text", "json", "log", "csv", "xml"]

    def optimize_large_files(self):
        """Main optimization function"""
        print("🚀 STARTING LARGE FILE OPTIMIZATION")
        print("=" * 60)

        large_files = self.scan_large_files()
        if not large_files:
            print("✅ No large files found requiring optimization")
            return

        optimization_results = {
            "timestamp": datetime.now().isoformat(),
            "total_files_processed": len(large_files),
            "total_original_size": sum(f['size_bytes'] for f in large_files),
            "optimization_results": [],
            "space_saved": 0,
            "method_used": {}
        }

        for i, file_info in enumerate(large_files, 1):
            print(f"\\n🎯 Optimizing {i}/{len(large_files)}: {Path(file_info['path']).name}")
            print(f"   📊 Size: {file_info['size_mb']:.1f} MB")
            result = self.optimize_single_file(file_info)
            if result:
                optimization_results["optimization_results"].append(result)
                optimization_results["space_saved"] += result.get("space_saved", 0)

                method = result.get("method", "unknown")
                optimization_results["method_used"][method] = optimization_results["method_used"].get(method, 0) + 1

        # Generate optimization report
        self.generate_optimization_report(optimization_results)

        print("\\n📊 LARGE FILE OPTIMIZATION COMPLETE!")
        print("=" * 50)
        print(f"📁 Files processed: {len(optimization_results['optimization_results'])}")
        print(".2f")
        print(".2f")
        print(f"📋 Methods used: {optimization_results['method_used']}")

    def optimize_single_file(self, file_info: Dict[str, any]) -> Optional[Dict[str, any]]:
        """Optimize a single large file"""
        filepath = Path(file_info['path'])

        if not filepath.exists():
            print(f"⚠️ File no longer exists: {filepath}")
            return None

        file_type = file_info['file_type']
        original_size = file_info['size_bytes']

        # Choose optimization method based on file type and size
        if file_type == "text" and file_info['compressible']:
            result = self.compress_text_file(filepath)
        elif file_type in ["video", "audio", "image"]:
            result = self.archive_media_file(filepath)
        elif original_size > 500 * 1024 * 1024:  # > 500MB
            result = self.chunk_large_file(filepath)
        else:
            result = self.compress_general_file(filepath)

        if result:
            result.update({
                "original_file": str(filepath),
                "original_size": original_size,
                "file_type": file_type,
                "optimization_timestamp": datetime.now().isoformat()
            })

        return result

    def compress_text_file(self, filepath: Path) -> Dict[str, any]:
        """Compress text-based files using optimal compression"""
        print(f"📝 Compressing text file: {filepath.name}")

        compressed_path = self.archive_path / f"{filepath.name}.gz"
        original_size = filepath.stat().st_size

        try:
            # Try different compression methods and choose best
            best_result = None
            best_ratio = 0

            for method in self.compression_methods:
                temp_path = self.archive_path / f"temp_{filepath.name}.{method}"

                if method == 'gzip':
                    with open(filepath, 'rb') as f_in:
                        with gzip.open(temp_path, 'wb', compresslevel=9) as f_out:
                            shutil.copyfileobj(f_in, f_out)
                elif method == 'bz2':
                    with open(filepath, 'rb') as f_in:
                        with bz2.open(temp_path, 'wb', compresslevel=9) as f_out:
                            shutil.copyfileobj(f_in, f_out)
                elif method == 'lzma':
                    with lzma.open(temp_path, 'wb', preset=9) as f_out:
                        with open(filepath, 'rb') as f_in:
                            shutil.copyfileobj(f_in, f_out)

                if temp_path.exists():
                    compressed_size = temp_path.stat().st_size
                    ratio = original_size / compressed_size if compressed_size > 0 else 0

                    if ratio > best_ratio:
                        best_ratio = ratio
                        if best_result and best_result['temp_path'].exists():
                            best_result['temp_path'].unlink()
                        best_result = {
                            'method': method,
                            'compressed_size': compressed_size,
                            'compression_ratio': ratio,
                            'temp_path': temp_path
                        }
                    else:
                        temp_path.unlink()

            if best_result:
                # Move best compression to final location
                final_path = self.archive_path / f"{filepath.name}.{best_result['method']}"
                best_result['temp_path'].rename(final_path)

                # Create backup of original
                backup_file = self.backup_path / filepath.name
                if not backup_file.exists():
                    shutil.copy2(filepath, backup_file)

                # Replace original with symbolic link
                filepath.unlink()
                filepath.symlink_to(final_path)

                space_saved = original_size - best_result['compressed_size']

                print(f"   💾 Space saved: {space_saved / (1024 * 1024):.1f} MB")
                print(f"   📊 Ratio: {best_result['compression_ratio']:.1f}x")
                return {
                    "method": "compression",
                    "compression_type": best_result['method'],
                    "compressed_path": str(final_path),
                    "compressed_size": best_result['compressed_size'],
                    "compression_ratio": best_result['compression_ratio'],
                    "space_saved": space_saved,
                    "backup_path": str(backup_file)
                }

        except Exception as e:
            print(f"❌ Compression failed: {e}")

        return None

    def archive_media_file(self, filepath: Path) -> Dict[str, any]:
        """Archive media files (keep original, create compressed archive)"""
        print(f"🎬 Archiving media file: {filepath.name}")

        original_size = filepath.stat().st_size
        archive_name = f"{filepath.name}.tar.gz"
        archive_path = self.archive_path / archive_name

        try:
            # Create compressed tar archive
            with tarfile.open(archive_path, "w:gz", compresslevel=9) as tar:
                tar.add(filepath, arcname=filepath.name)

            archived_size = archive_path.stat().st_size
            space_saved = 0  # We keep the original, just create archive for backup

            print(f"   📦 Archive created: {archive_name}")
            print(f"   📦 Archive size: {archived_size / (1024 * 1024):.1f} MB")
            return {
                "method": "archiving",
                "archive_path": str(archive_path),
                "archived_size": archived_size,
                "space_saved": space_saved,
                "compression_ratio": original_size / archived_size if archived_size > 0 else 0
            }

        except Exception as e:
            print(f"❌ Archiving failed: {e}")

        return None

    def chunk_large_file(self, filepath: Path) -> Dict[str, any]:
        """Chunk very large files into manageable pieces"""
        print(f"✂️ Chunking large file: {filepath.name}")

        original_size = filepath.stat().st_size
        chunk_dir = self.chunk_storage / filepath.stem
        chunk_dir.mkdir(exist_ok=True)

        chunks = []
        total_chunked_size = 0

        try:
            chunk_number = 0
            with open(filepath, 'rb') as f:
                while True:
                    chunk_data = f.read(self.chunk_size)
                    if not chunk_data:
                        break

                    chunk_filename = "04d"
                    chunk_path = chunk_dir / chunk_filename

                    with open(chunk_path, 'wb') as chunk_file:
                        chunk_file.write(chunk_data)

                    chunk_size = len(chunk_data)
                    total_chunked_size += chunk_size
                    chunks.append({
                        "filename": chunk_filename,
                        "size": chunk_size,
                        "path": str(chunk_path)
                    })
                    chunk_number += 1

            # Create chunk manifest
            manifest = {
                "original_file": str(filepath),
                "original_size": original_size,
                "chunk_size": self.chunk_size,
                "total_chunks": len(chunks),
                "chunks": chunks,
                "created": datetime.now().isoformat()
            }

            manifest_path = chunk_dir / "manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)

            # Create backup of original
            backup_file = self.backup_path / filepath.name
            if not backup_file.exists():
                shutil.move(filepath, backup_file)

            # Create reconstruction script
            reconstruction_script = chunk_dir / "reconstruct.py"
            with open(reconstruction_script, 'w') as f:
                f.write(f'''#!/usr/bin/env python3
import json
import shutil
from pathlib import Path

# Reconstruct {filepath.name} from chunks

def reconstruct_file():
    manifest_path = Path(__file__).parent / "manifest.json"
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    output_file = Path("{str(filepath)}")

    print("🔄 Reconstructing {filepath.name}...")

    with open(output_file, 'wb') as outfile:
        for chunk_info in manifest['chunks']:
            chunk_path = Path(__file__).parent / chunk_info['filename']
            with open(chunk_path, 'rb') as chunk_file:
                shutil.copyfileobj(chunk_file, outfile)
            print(f"   ✅ Added chunk {{chunk_info['filename']}}")

    print(f"✅ Reconstruction complete: {{output_file}}")

if __name__ == "__main__":
    reconstruct_file()
''')

            print(f"   ✂️ File chunked into {len(chunks)} pieces")
            print(f"   📋 Manifest: {manifest_path}")
            print(f"   🔧 Reconstruction script: {reconstruction_script}")

            return {
                "method": "chunking",
                "chunk_directory": str(chunk_dir),
                "total_chunks": len(chunks),
                "chunk_size": self.chunk_size,
                "space_saved": 0,  # Chunking doesn't save space, just makes files manageable
                "manifest_path": str(manifest_path),
                "reconstruction_script": str(reconstruction_script),
                "backup_path": str(backup_file)
            }

        except Exception as e:
            print(f"❌ Chunking failed: {e}")

        return None

    def compress_general_file(self, filepath: Path) -> Dict[str, any]:
        """Compress general binary files"""
        print(f"📦 Compressing general file: {filepath.name}")

        original_size = filepath.stat().st_size
        compressed_path = self.archive_path / f"{filepath.name}.gz"

        try:
            with open(filepath, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb', compresslevel=6) as f_out:  # Moderate compression for speed
                    shutil.copyfileobj(f_in, f_out)

            compressed_size = compressed_path.stat().st_size

            # Create backup of original
            backup_file = self.backup_path / filepath.name
            if not backup_file.exists():
                shutil.copy2(filepath, backup_file)

            # Replace original with symbolic link
            filepath.unlink()
            filepath.symlink_to(compressed_path)

            space_saved = original_size - compressed_size
            compression_ratio = original_size / compressed_size if compressed_size > 0 else 0

            print(f"   📦 Archive size: {archived_size / (1024 * 1024):.1f} MB")
            return {
                "method": "general_compression",
                "compressed_path": str(compressed_path),
                "compressed_size": compressed_size,
                "compression_ratio": compression_ratio,
                "space_saved": space_saved,
                "backup_path": str(backup_file)
            }

        except Exception as e:
            print(f"❌ General compression failed: {e}")

        return None

    def generate_optimization_report(self, results: Dict[str, any]):
        """Generate comprehensive optimization report"""
        report_path = self.workspace_path / f"large_file_optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # Add summary statistics
        results["summary"] = {
            "total_space_saved": sum(r.get("space_saved", 0) for r in results["optimization_results"]),
            "average_compression_ratio": sum(r.get("compression_ratio", 1) for r in results["optimization_results"] if "compression_ratio" in r) / len([r for r in results["optimization_results"] if "compression_ratio" in r]) if results["optimization_results"] else 0,
            "files_compressed": len([r for r in results["optimization_results"] if r.get("method") in ["compression", "general_compression"]]),
            "files_chunked": len([r for r in results["optimization_results"] if r.get("method") == "chunking"]),
            "files_archived": len([r for r in results["optimization_results"] if r.get("method") == "archiving"])
        }

        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"📄 Optimization report: {report_path}")

    def restore_file(self, original_path: str) -> bool:
        """Restore an optimized file to its original form"""
        print(f"🔄 Restoring: {original_path}")

        original_file = Path(original_path)

        # Check if it's a symbolic link
        if original_file.is_symlink():
            target = original_file.readlink()

            if target.exists():
                # Remove symlink and copy target back
                original_file.unlink()
                shutil.copy2(target, original_file)
                print(f"✅ Restored from {target.name}")
                return True

        # Check chunked files
        file_stem = original_file.stem
        chunk_dir = self.chunk_storage / file_stem

        if chunk_dir.exists():
            manifest_path = chunk_dir / "manifest.json"
            if manifest_path.exists():
                # Run reconstruction script
                reconstruct_script = chunk_dir / "reconstruct.py"
                if reconstruct_script.exists():
                    try:
                        subprocess.run(["python3", str(reconstruct_script)], check=True)
                        print(f"✅ Reconstructed from chunks")
                        return True
                    except subprocess.CalledProcessError as e:
                        print(f"❌ Reconstruction failed: {e}")

        print(f"❌ Could not restore {original_path}")
        return False

def main():
    """Main execution function"""
    optimizer = LargeFileOptimizer()
    optimizer.optimize_large_files()

if __name__ == "__main__":
    main()
