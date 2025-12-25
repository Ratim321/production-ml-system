# GitHub Repository Setup Guide

Follow these steps to set up your GitHub repository for the production-ml-system project.

## 1. Create Repository

1. Go to GitHub and create a new repository
2. Name it: `production-ml-system`
3. Description: "Production-ready ML system for customer churn prediction with real-time and batch inference"
4. Set visibility (Public recommended for showcase)
5. **Don't** initialize with README (we already have one)

## 2. Push Your Code

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Production ML System"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/production-ml-system.git

# Push to main branch
git branch -M main
git push -u origin main
```

## 3. Update Repository URLs

After pushing, update these files with your actual GitHub username:

1. **README.md**: Replace `yourusername` with your GitHub username
2. **app/main.py**: Update repository URL
3. **.github/workflows/docker-publish.yml**: Already uses `${{ github.repository }}`
4. **SECURITY.md**: Update email if needed

## 4. Enable GitHub Features

### GitHub Actions
- Go to Settings → Actions → General
- Enable "Allow all actions and reusable workflows"
- Save

### Dependabot
- Go to Settings → Security
- Enable "Dependabot alerts"
- Enable "Dependabot security updates"

### Discussions (Optional)
- Go to Settings → General → Features
- Enable "Discussions"

### Issues
- Go to Settings → General → Features
- Ensure "Issues" is enabled

## 5. Add Topics/Tags

Add these topics to your repository for better discoverability:
- `machine-learning`
- `mlops`
- `fastapi`
- `docker`
- `postgresql`
- `mlflow`
- `churn-prediction`
- `production-ready`
- `python`
- `react`

## 6. Create Initial Release

```bash
# Tag the initial release
git tag -a v1.0.0 -m "Initial release: Production ML System"
git push origin v1.0.0
```

Or use GitHub UI:
- Go to Releases → Create a new release
- Tag: `v1.0.0`
- Title: "Production ML System v1.0.0"
- Description: Use content from PROJECT_SHOWCASE.md

## 7. Add Repository Description

In repository settings, add:
```
Production-ready end-to-end ML system with FastAPI, MLflow, Docker, and React dashboard. Features include real-time/batch inference, canary deployments, and comprehensive monitoring.
```

## 8. Pin Important Files

Pin these files in your repository:
- README.md
- QUICKSTART.md
- ARCHITECTURE.md

## 9. Set Up Branch Protection (Optional)

For production use:
- Settings → Branches
- Add rule for `main` branch
- Require pull request reviews
- Require status checks to pass

## 10. Verify Everything Works

1. Check Actions tab - CI should run automatically
2. Check Security tab - Dependabot should be active
3. Test creating an issue - templates should appear
4. Test creating a PR - template should appear
5. Visit repository URL - README should display properly

## 11. Add Social Preview

Add a social preview image (1280x640px) showing:
- Project name
- Key features
- Architecture diagram

## 12. Update Badges (Optional)

After first CI run, update README badges with actual status URLs:
- Replace workflow badge URLs with your repository path
- Add coverage badge if using coverage service

## Done! 🎉

Your repository is now ready for GitHub showcase. Share it and watch the stars roll in!

