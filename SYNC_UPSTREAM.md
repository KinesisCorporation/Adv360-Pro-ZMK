# Syncing with Upstream Repository

This repository is configured to sync with the official Kinesis Adv360-Pro-ZMK repository while maintaining custom modifications.

## Branch Structure

- `latest` - Your main development branch with custom modifications
- `V3.0` - Tracks the upstream V3.0 branch for syncing

## Remote Repositories

- `origin` - Your fork (flaticols/Adv360-Pro-ZMK)
- `upstream` - Official Kinesis repository (KinesisCorporation/Adv360-Pro-ZMK)

## Syncing Process

### 1. Fetch Latest Changes from Upstream

```bash
# Fetch all upstream branches
git fetch upstream

# View available upstream branches
git branch -r | grep upstream
```

### 2. Update V3.0 Branch with Upstream

```bash
# Switch to V3.0 branch
git checkout V3.0

# Merge or rebase upstream changes
git merge upstream/V3.0
# OR for a cleaner history
git rebase upstream/V3.0

# Push updated V3.0 to your fork
git push origin V3.0
```

### 3. Merge Upstream Changes into Latest

```bash
# Switch to your latest branch
git checkout latest

# Merge V3.0 changes into latest
git merge V3.0

# Resolve any conflicts if they occur
# After resolving conflicts:
git add .
git commit -m "Merge upstream V3.0 changes"

# Push updated latest branch
git push origin latest
```

## Alternative: Cherry-pick Specific Commits

If you only want specific updates from upstream:

```bash
# View upstream commits
git log upstream/V3.0 --oneline

# Cherry-pick specific commits
git checkout latest
git cherry-pick <commit-hash>
```

## Automated Release Creation

Releases are automatically created when:
- Pushing to the `latest` branch
- Creating git tags

The GitHub Actions workflow will:
1. Build both Legacy and Clique firmware versions
2. Create a GitHub release with the commit hash or tag as the version
3. Attach all firmware files to the release

## Quick Sync Script

You can create a script to automate the sync process:

```bash
#!/bin/bash
# sync-upstream.sh

echo "Fetching upstream..."
git fetch upstream

echo "Updating V3.0 branch..."
git checkout V3.0
git merge upstream/V3.0
git push origin V3.0

echo "Merging into latest..."
git checkout latest
git merge V3.0

echo "Done! Review changes and push when ready:"
echo "  git push origin latest"
```

## Troubleshooting

### Merge Conflicts
If you encounter merge conflicts:
1. Review conflicting files with `git status`
2. Edit files to resolve conflicts
3. Mark as resolved with `git add <file>`
4. Complete merge with `git commit`

### Reset to Upstream
If you need to completely reset to upstream:
```bash
git checkout V3.0
git reset --hard upstream/V3.0
git push origin V3.0 --force
```

**Warning:** This will lose any custom changes in the V3.0 branch.

### Check Remote Configuration
```bash
git remote -v
```

Should show:
- origin pointing to your fork
- upstream pointing to KinesisCorporation repository