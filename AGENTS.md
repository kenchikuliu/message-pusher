# Repository Guidelines

## Project Structure & Module Organization
Core Go services live under `channel/` (provider adapters), `controller/` (HTTP handlers), `router/` (Gin route registration), `middleware/` (auth/logging), and `common/` (shared helpers). Persistence and domain types sit in `model/`, while `main.go` wires dependencies and boots the API server. Static docs and API references live in `docs/`; the React dashboard is maintained in `web/`. Use `bin/` for locally built artifacts, and keep deployment manifests (`Dockerfile`, `docker-compose.yml`) in the repository root.

## Build, Test, and Development Commands
- `go build -o bin/message-pusher ./` ? compile the backend binary.
- `go run ./` ? start the API server with the current configuration.
- `go test ./...` ? execute Go unit tests across all packages.
- `yarn --cwd web install` ? install web dependencies.
- `yarn --cwd web start` ? launch the React dev server proxied to the Go backend.
- `yarn --cwd web build` ? produce the production-ready frontend bundle in `web/build/`.
- `docker-compose up -d` ? run the full stack (API, database, dashboard) for integration checks.

## Coding Style & Naming Conventions
Run `gofmt` and `goimports` on every Go change; Go code stays tab-indented with PascalCase for exported symbols and camelCase for internals. Keep handler files small and colocate channel-specific logic inside `channel/<provider>/`. For the dashboard, follow the repository Prettier config (single quotes) and keep React components under `web/src/components/` using PascalCase filenames. Validate linting locally with `npx eslint` if you introduce new rules.

## Testing Guidelines
Add table-driven Go tests alongside the code under test as `<file>_test.go`. Exercises that hit external services should be wrapped behind interfaces so they can be mocked. Frontend behavior belongs in React Testing Library suites within `web/src/__tests__/`, runnable via `yarn --cwd web test --watch=false`. Prefer covering new endpoints and UI flows before submitting a pull request.

## Commit & Pull Request Guidelines
Follow the existing Conventional Commit style (`feat:`, `fix:`, `perf:`, etc.) and reference issues with `(#123)` when applicable. Squash noisy work-in-progress commits before publishing. Each PR should explain the change, list manual or automated verification steps, and attach screenshots or cURL examples for user-facing updates. Keep docs and sample configuration in sync whenever you add or rename environment variables.
