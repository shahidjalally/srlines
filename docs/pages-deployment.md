# GitHub Pages deployment

This repository contains the ready-to-publish static website. `build_site.py`
updates the primary HTML pages locally; commit its generated output alongside
source changes. The root `.nojekyll` file tells branch-based GitHub Pages
publishing to serve the static files without Jekyll processing.

## Publish an update

1. Run `python build_site.py` and `python tests/validate_site.py`.
2. Review and merge the pull request into `main`.
3. Open the repository's Actions tab and inspect the new `pages build and deployment`
   run for that merge commit. A pull request alone does not publish the site.
4. Confirm the deploy job succeeds, then check the public site.

Keep the existing Pages branch/source and custom domain settings. This change
requires no switch to a custom Actions workflow and no DNS changes.

## Deployment stalls

A successful build followed by a deployment timeout at `syncing_files` means
Pages accepted the artifact but did not finish publishing within the action's
wait period. It does not by itself establish a problem in the HTML.

Check https://www.githubstatus.com/ for Actions or Pages incidents. Avoid
repeated retries while an attempt is queued. If GitHub refuses to cancel a
queued attempt, retain the run URL and contact GitHub Support at
https://support.github.com/ if the queue persists.

Merging a new commit requests a fresh branch-based Pages build. Neither a new
commit nor `.nojekyll` can guarantee recovery of a GitHub-side stuck deployment,
force-cancel an old run, or prove the public site has updated. Verify the new
run's final deployment status before reporting a successful publish.

## Portrait update deployment retry

PR #35 includes Muhammad Soban's uploaded portrait, leadership spacing and
connecting lines. If its deployment fails, merge the follow-up static-publish
commit to request a fresh build from `main`; the existing `.nojekyll` marker is
retained. Its contents are explanatory only: GitHub Pages uses the marker's
presence to skip Jekyll.

After merging, verify the new Pages run completes and open `/team.html`.
Confirm Soban's photograph loads from `/assets/team/muhammad-oban.jpeg` and
the leadership cards show the updated spacing and connector. If deployment
fails again, inspect that run's deploy-job logs before deciding on another retry.
