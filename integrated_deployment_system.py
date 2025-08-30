#!/usr/bin/env python3
"""
EMPIRE_AGENT_INFO:
NAME: Integrated Deployment System
PURPOSE: Coordinates with all empire agents and automatically deploys website updates
CATEGORY: Deployment & Coordination
STATUS: Active
FREQUENCY: Continuous
"""

import os
import json
import time
import shutil
import subprocess
from datetime import datetime
import glob
import hashlib

from agent_logging_utils import AgentLogger, AgentUtils, with_timeout, with_retry

class IntegratedDeploymentSystem:
    def __init__(self):
        self.logger = AgentLogger("integrated_deployment_system")
        self.website_dir = "wealthyrobots_website"
        self.deployment_log = "deployment_log.json"
        self.agent_coordination = {}
        self.deployment_status = {}
        self.manifest_path = "deploy_manifest.json"
        self.manifest = self._load_manifest()

        # Load existing agent coordination
        self.load_agent_coordination()
        
    def _load_manifest(self):
        if os.path.exists(self.manifest_path):
            try:
                with open(self.manifest_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_manifest(self):
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def _sha256_file(self, path):
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()

    def _should_deploy(self, relative_path):
        abs_path = os.path.join(self.website_dir, relative_path)
        if not os.path.exists(abs_path):
            return False
        digest = self._sha256_file(abs_path)
        old = self.manifest.get(relative_path)
        if old != digest:
            self.manifest[relative_path] = digest
            return True
        return False

    def load_agent_coordination(self):
        """Load coordination with existing agents"""
        self.logger.info("Loading agent coordination", agent_count=len(self.agent_coordination))

        # Check which agents are available and active
        self.agent_coordination = {
            "orchestrator": {
                "file": "optimized_orchestrator.py",
                "status": "active",
                "purpose": "Master coordination and workflow management"
            },
            "content_agent": {
                "file": "optimized_content_agent.py",
                "status": "active",
                "purpose": "Content generation and SEO optimization"
            },
            "social_media": {
                "file": "social_media_agent.py",
                "status": "active",
                "purpose": "Twitter posting and social media management"
            },
            "website_manager": {
                "file": "authority_website_manager.py",
                "status": "active",
                "purpose": "Website structure and content management"
            },
            "content_system": {
                "file": "automated_content_system.py",
                "status": "active",
                "purpose": "Automated content generation and scheduling"
            },
            "github_deploy": {
                "file": "github_auto_deploy_agent.py",
                "status": "available",
                "purpose": "GitHub deployment and Vercel integration"
            },
            "smart_scheduler": {
                "file": "smart_scheduler.py",
                "status": "active",
                "purpose": "Task scheduling and timing management"
            },
            "ceo_agent": {
                "file": "ultimate_ceo_agent.py",
                "status": "active",
                "purpose": "Strategic decision making and budget allocation"
            }
        }

        # Verify agent availability
        available_count = 0
        for agent_name, agent_info in self.agent_coordination.items():
            if os.path.exists(agent_info["file"]):
                self.logger.info("Agent available", agent=agent_name, purpose=agent_info['purpose'])
                available_count += 1
            else:
                self.logger.warning("Agent file not found", agent=agent_name, file=agent_info["file"])
                agent_info["status"] = "unavailable"

        self.logger.info("Agent coordination loaded", total=len(self.agent_coordination), available=available_count)
        return self.agent_coordination
    
    def check_agent_status(self):
        """Check current status of all agents"""
        self.logger.info("Checking agent status")

        status_report = {}
        active_count = 0

        for agent_name, agent_info in self.agent_coordination.items():
            if agent_info["status"] == "active":
                status_report[agent_name] = "active"
                active_count += 1

        self.logger.info("Agent status checked", active=active_count, total=len(self.agent_coordination))
        return status_report
    
    def coordinate_website_deployment(self):
        self.logger.info("Coordinating website deployment")
        self.deploy_website()
        self.update_agent_coordination()
        
    def deploy_website(self):
        """Deploy website to GitHub/Vercel with incremental manifest"""
        self.logger.info("Starting website deployment")

        # Check if GitHub deployment agent is available
        if self.agent_coordination["github_deploy"]["status"] == "available":
            self.logger.info("Using GitHub Auto-Deploy Agent")
            self.deploy_via_github_agent()
            # Save manifest after successful loop
            self._save_manifest()
        else:
            self.logger.info("Manual deployment required")
            self.provide_manual_deployment_instructions()
    
    def deploy_via_github_agent(self):
        """Deploy using GitHub auto-deploy agent (only changed files)"""
        try:
            from github_auto_deploy_agent import GitHubAutoDeployAgent
            deploy_agent = GitHubAutoDeployAgent()
            
            def deploy_if_changed(rel_path):
                if self._should_deploy(rel_path):
                    abs_path = os.path.join(self.website_dir, rel_path)
                    with open(abs_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.logger.info("Deploying file", file=rel_path)
                    ok = deploy_agent.auto_deploy_article(rel_path, content)
                    if ok:
                        self.logger.info("File deployed successfully", file=rel_path)
                    else:
                        self.logger.error("File deployment failed", file=rel_path)
                else:
                    self.logger.debug("Skipped unchanged file", file=rel_path)
            
            # Core files
            core_files = [
                "index.html",
                "assets/css/main.css",
                "assets/js/main.js", 
                "sitemap.xml",
                "robots.txt",
                "feed.xml",
                "404.html"
            ]
            for rel in core_files:
                if os.path.exists(os.path.join(self.website_dir, rel)):
                    deploy_if_changed(rel)
            
            # Section index pages
            section_dirs = ["strategies","tools","resources","about","contact","articles"]
            for section in section_dirs:
                rel = f"{section}/index.html"
                if os.path.exists(os.path.join(self.website_dir, rel)):
                    deploy_if_changed(rel)
            
            # Section sitemaps
            for sec in ["articles","strategies","tools","resources","about","contact"]:
                rel = f"sitemap_{sec}.xml"
                if os.path.exists(os.path.join(self.website_dir, rel)):
                    deploy_if_changed(rel)
            
            # vercel.json at repo root
            if os.path.exists("vercel.json"):
                rel = "vercel.json"
                # manifest for root-managed file: use separate key prefix
                key = f"__root__/{rel}"
                digest = self._sha256_file(rel)
                old = self.manifest.get(key)
                if old != digest:
                    with open(rel, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.logger.info("Deploying file", file=rel)
                    ok = deploy_agent.auto_deploy_article(rel, content)
                    if ok:
                        self.logger.info("File deployed successfully", file=rel)
                    else:
                        self.logger.error("File deployment failed", file=rel)
                    self.manifest[key] = digest
                else:
                    self.logger.debug("Skipped unchanged file", file=rel)
            
            # Articles
            articles_dir = os.path.join(self.website_dir, "articles")
            if os.path.exists(articles_dir):
                article_files = glob.glob(os.path.join(articles_dir, "*.html"))
                for article_file in article_files:
                    article_name = os.path.basename(article_file)
                    rel = f"articles/{article_name}"
                    deploy_if_changed(rel)

            # Affiliate redirect pages (/go/*.html)
            go_dir = os.path.join(self.website_dir, "go")
            if os.path.exists(go_dir):
                go_files = glob.glob(os.path.join(go_dir, "*.html"))
                for go_file in go_files:
                    rel = f"go/{os.path.basename(go_file)}"
                    deploy_if_changed(rel)
        except Exception as e:
            self.logger.error("GitHub deployment failed", error=str(e))
            self.provide_manual_deployment_instructions()
    
    def provide_manual_deployment_instructions(self):
        """Provide manual deployment instructions"""
        instructions = """
📋 MANUAL DEPLOYMENT INSTRUCTIONS
========================================
1. Go to: https://github.com/komoglobal/wealthyrobots-website
2. Upload website files from: wealthyrobots_website/
3. Vercel will auto-deploy from GitHub
4. Website will be live at: https://wealthyrobots.com
5. Check deployment status in Vercel dashboard
        """.strip()

        self.logger.info("Manual deployment required", instructions=instructions)
    
    def update_agent_coordination(self):
        """Update agent coordination status"""
        self.logger.info("Updating agent coordination")

        self.deployment_status = {
            "last_deployment": datetime.now().isoformat(),
            "website_status": "deployed" if os.path.exists(self.website_dir) else "not_built",
            "content_count": len(glob.glob(os.path.join(self.website_dir, "articles", "*.html"))) if os.path.exists(self.website_dir) else 0,
            "agent_coordination": self.agent_coordination
        }

        try:
            with open("deployment_coordination.json", 'w') as f:
                json.dump(self.deployment_status, f, indent=2)
            self.logger.info("Agent coordination updated successfully")
        except Exception as e:
            self.logger.error("Failed to update coordination file", error=str(e))
    
    def run_continuous_deployment(self):
        """Run continuous deployment monitoring"""
        self.logger.info("Starting continuous deployment monitoring")
        while True:
            try:
                self.check_agent_status()
                self.coordinate_website_deployment()
                time.sleep(1800)
            except KeyboardInterrupt:
                self.logger.info("Continuous deployment stopped by user")
                break
            except Exception as e:
                self.logger.error("Deployment loop error", error=str(e))
                time.sleep(300)

if __name__ == '__main__':
    ids = IntegratedDeploymentSystem()
    ids.logger.info("Running deployment cycle")
    ids.logger.info("Checking agent status")
    ids.check_agent_status()
    ids.coordinate_website_deployment()
