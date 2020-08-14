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
