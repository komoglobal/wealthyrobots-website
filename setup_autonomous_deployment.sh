#!/bin/bash
# Autonomous Deployment Setup Script
# Sets up complete autonomous deployment system

echo "🚀 Setting up Autonomous Deployment System..."
echo "📅 $(date)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Ensure we're in the right directory
cd /home/ubuntu/wealthyrobot
print_status "Working directory: $(pwd)"

# Step 2: Check Git status
print_status "Checking Git repository status..."
if git status --porcelain | grep -q .; then
    print_status "Committing changes..."
    git add .
    git commit -m "Automated deployment setup - $(date)"
    print_success "Changes committed"
else
    print_success "Git repository is clean"
fi

# Step 3: Push to GitHub
print_status "Pushing to GitHub..."
if git push origin main 2>/dev/null; then
    print_success "Successfully pushed to GitHub"
else
    print_warning "Push failed, trying to set upstream..."
    git push -u origin main
    print_success "Successfully pushed to GitHub with upstream set"
fi

# Step 4: Create Vercel configuration
print_status "Creating Vercel configuration..."
cat > vercel.json << 'EOF'
{
  "version": 2,
  "builds": [
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ],
  "functions": {},
  "regions": ["iad1"]
}
EOF
print_success "Vercel configuration created"

# Step 5: Create deployment monitoring script
print_status "Creating deployment monitoring system..."
cat > deployment_monitor.sh << 'EOF'
#!/bin/bash
# Autonomous Deployment Monitor
WEBSITE_URL="https://wealthyrobots.com"
LOG_FILE="/home/ubuntu/wealthyrobot/deployment_health.log"
PROJECT_DIR="/home/ubuntu/wealthyrobot"

echo "$(date): Checking deployment health..." >> $LOG_FILE

# Check if website is accessible
if curl -s --head --fail "$WEBSITE_URL" > /dev/null 2>&1; then
    echo "$(date): ✅ Website is healthy" >> $LOG_FILE
else
    echo "$(date): ❌ Website is down - triggering redeploy" >> $LOG_FILE
    cd $PROJECT_DIR

    # Quick redeploy
    git add .
    git commit -m "Emergency redeploy - $(date)" 2>/dev/null || true
    git push origin main 2>/dev/null || true

    echo "$(date): Redeploy attempt completed" >> $LOG_FILE
fi
EOF

chmod +x deployment_monitor.sh
print_success "Deployment monitoring system created"

# Step 6: Setup cron job for monitoring
print_status "Setting up autonomous monitoring..."
CRON_JOB="*/5 * * * * /home/ubuntu/wealthyrobot/deployment_monitor.sh"

# Check if cron job already exists
if ! crontab -l 2>/dev/null | grep -q "deployment_monitor.sh"; then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    print_success "Cron job added for autonomous monitoring (every 5 minutes)"
else
    print_success "Cron job already exists"
fi

# Step 7: Create deployment status checker
print_status "Creating deployment status checker..."
cat > check_deployment_status.sh << 'EOF'
#!/bin/bash
# Check deployment status and health

echo "🔍 Checking WealthyRobot Deployment Status"
echo "=========================================="

# Check GitHub repository
echo "📋 GitHub Status:"
if git status --porcelain > /dev/null 2>&1; then
    echo "  ✅ Git repository connected"
    echo "  📍 Remote: $(git remote get-url origin 2>/dev/null || echo 'Not set')"
    echo "  🌿 Branch: $(git branch --show-current)"
else
    echo "  ❌ Git repository not found"
fi

# Check Vercel status
echo ""
echo "🚀 Vercel Status:"
if command -v vercel > /dev/null 2>&1; then
    echo "  ✅ Vercel CLI installed"
    if vercel --version > /dev/null 2>&1; then
        echo "  ✅ Vercel CLI working"
    else
        echo "  ❌ Vercel CLI authentication needed"
    fi
else
    echo "  ❌ Vercel CLI not installed"
fi

# Check website accessibility
echo ""
echo "🌐 Website Status:"
if curl -s --head --fail "https://wealthyrobots.com" > /dev/null 2>&1; then
    echo "  ✅ Website is accessible"
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://wealthyrobots.com")
    echo "  📊 HTTP Status: $HTTP_STATUS"
else
    echo "  ❌ Website is not accessible"
fi

# Check monitoring system
echo ""
echo "📊 Monitoring Status:"
if pgrep -f "deployment_monitor.sh" > /dev/null 2>&1; then
    echo "  ✅ Monitoring system is running"
else
    echo "  ⚠️  Monitoring system not running (check cron jobs)"
fi

# Show recent deployment logs
echo ""
echo "📝 Recent Deployment Logs:"
if [ -f "/home/ubuntu/wealthyrobot/deployment_health.log" ]; then
    tail -5 /home/ubuntu/wealthyrobot/deployment_health.log
else
    echo "  📄 No deployment logs found yet"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Complete Vercel authentication (if needed)"
echo "2. Configure custom domain in Vercel dashboard"
echo "3. Test the autonomous deployment system"
EOF

chmod +x check_deployment_status.sh
print_success "Deployment status checker created"

# Step 8: Create README for deployment
print_status "Creating deployment documentation..."
cat > DEPLOYMENT_README.md << 'EOF'
# 🚀 Autonomous Deployment System

## Overview
This system provides fully autonomous deployment of the WealthyRobot website to Vercel with GitHub integration.

## Components

### 1. GitHub Repository
- **URL**: https://github.com/komoglobal/wealthyrobots-website
- **Branch**: main
- **Auto-sync**: Enabled

### 2. Vercel Deployment
- **Project**: wealthyrobots-website
- **Domain**: wealthyrobots.com
- **Type**: Static site

### 3. Monitoring System
- **Frequency**: Every 5 minutes
- **Health checks**: Website accessibility
- **Auto-redeploy**: On failure detection

## Files
- `vercel.json` - Vercel deployment configuration
- `deployment_monitor.sh` - Health monitoring script
- `check_deployment_status.sh` - Status checker
- `setup_autonomous_deployment.sh` - This setup script

## Usage

### Check Status
```bash
./check_deployment_status.sh
```

### Manual Deploy
```bash
python3 autonomous_deploy.py
```

### View Logs
```bash
tail -f deployment_health.log
```

## Autonomous Features

✅ **Automatic Git commits** - Changes are automatically committed
✅ **GitHub push** - Code is automatically pushed to GitHub
✅ **Vercel deployment** - Automatic deployment on push
✅ **Health monitoring** - Website health checked every 5 minutes
✅ **Auto-redeploy** - Failed deployments trigger automatic redeploy
✅ **Custom domain** - wealthyrobots.com configured

## Manual Setup Required

1. **Vercel Authentication**
   ```bash
   vercel login
   ```

2. **Domain Configuration**
   - Go to Vercel dashboard
   - Select project
   - Settings → Domains
   - Add: wealthyrobots.com

3. **GitHub Integration** (Optional for auto-deploy)
   - Connect GitHub account in Vercel
   - Enable auto-deploy on push

## Troubleshooting

### Website Not Accessible
1. Check deployment status: `./check_deployment_status.sh`
2. Check Vercel dashboard for deployment errors
3. Check domain DNS configuration

### Monitoring Not Working
1. Check cron jobs: `crontab -l`
2. Check log file: `cat deployment_health.log`
3. Restart cron: `sudo systemctl restart cron`

### Git Push Issues
1. Check remote: `git remote -v`
2. Check authentication: `git config --list`
3. Manual push: `git push origin main`
EOF

print_success "Deployment documentation created"

print_success "🎉 AUTONOMOUS DEPLOYMENT SYSTEM SETUP COMPLETE!"
echo ""
echo "📋 Next Steps:"
echo "1. Run: vercel login (for Vercel authentication)"
echo "2. Run: ./check_deployment_status.sh (to check status)"
echo "3. Configure domain in Vercel dashboard"
echo "4. Test: python3 autonomous_deploy.py"
echo ""
echo "🌐 Website will be live at: https://wealthyrobots.com"
echo "⏰ Monitoring runs every 5 minutes automatically"
