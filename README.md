## Insight Scripts

CircleCI doesn't provide great visuals on where credits go, how much you use over time, and if our changes in its config impact our usage negatively (or positively). To address this problem, I created a few simple Python scripts. Now, I'm by no means an expert Python programmer - it just had easy access to graphing libraries; so, if you see something you can improve, feel free to open a PR.

## Before Running

- Rename `main.cfg.rename` to `main.cfg`
- Add in your variables into `main.cfg`
  - Your personal `CIRCLE_TOKEN` (here: https://circleci.com/docs/2.0/managing-api-tokens/)
  - `VCS` is your version control system (e.g. `github`, `bitbucket`)
  - `ORG` is your VCS's org name (e.g. `github.com/<org-name>/repo`)
  - `REPO` is your VCS's repository name (e.g. `github.com/org-name/<repo>`)

## Notes

- `build-credits.py` obtains your branch-based insights. If it's a little slow, you might wanna adjust the `MAX_PAGES` in the script itself.
- `deploy-credits.py` gets your default branch's workflow credits.
