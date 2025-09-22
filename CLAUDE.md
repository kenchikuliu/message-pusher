# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a message pushing service built with Go (backend) and React (frontend). It supports 15+ message channels including email, WeChat, QQ, DingTalk, Slack, Telegram, Discord, Bark, and more. The service provides a unified API for sending messages across multiple platforms with support for Markdown, async messaging, and webhook integration.

## Development Commands

### Backend (Go)
- **Build**: `go build -ldflags "-s -w" -o message-pusher`
- **Run**: `./message-pusher --port 3000 --log-dir ./logs`
- **Dependencies**: `go mod download`
- **Test**: `go test ./...`
- **Hot reload**: Use `air` or manually restart after changes

### Frontend (React)
- **Install dependencies**: `cd web && npm install`
- **Development server**: `cd web && npm start` (runs on port 3001)
- **Build**: `cd web && npm run build`
- **Test**: `cd web && npm test`
- **Lint/Format**: `cd web && npx prettier --write .`

### Complete Build Process
For full application build:
1. `cd web && npm install && npm run build`
2. `cd .. && go mod download && go build -ldflags "-s -w" -o message-pusher`

### Development Setup
- Frontend dev server (port 3001) proxies API calls to backend (port 3000)
- Use `GIN_MODE=debug` environment variable for detailed logging
- SQLite database (`message-pusher.db`) created automatically on first run
- Default admin: username `root`, password `123456`

## Architecture

### Core Components

**MVC Structure:**
- `main.go`: Application entry point, initializes Gin server, database, Redis, sessions
- `model/`: Database models and ORM operations (User, Message, Channel, Option, Webhook)
- `controller/`: HTTP request handlers for API endpoints
- `router/`: Route definitions split into API routes and web routes
- `channel/`: Message sending implementations for different platforms
- `middleware/`: Authentication and rate limiting middleware

**Key Files:**
- `main.go`: Application entry point with embedded web assets (`//go:embed web/build`)
- `model/main.go`: Database initialization with auto-migration
- `channel/main.go`: Central message dispatcher that routes to specific channel handlers
- `channel/message-queue.go`: Async message processing queue
- `channel/token-store.go`: Secure token authentication storage
- `router/main.go`: Router setup combining API and web routes

### Database

Uses GORM with auto-migration support:
- **SQLite** (default): Single file database `message-pusher.db`
- **MySQL**: Configured via `SQL_DSN` environment variable

**Core Models:**
- `User`: User accounts with role-based access
- `Message`: Message records with status tracking
- `Channel`: Channel configurations for different platforms
- `Option`: System configuration key-value pairs
- `Webhook`: Webhook endpoint configurations

### Channel System

The message pushing system supports 15+ channel types:
- **Email**: SMTP-based email notifications
- **WeChat**: Test account (`wechat-test-account.go`) and corp account (`wechat-corp-account.go`)
- **Enterprise Messaging**: DingTalk (`ding.go`), Lark (`lark.go`, `lark-app.go`), Discord (`discord.go`)
- **Mobile/Desktop**: Bark App (`bark.go`), Telegram (`telegram.go`)
- **Custom Integration**: WebSocket clients (`client.go`), custom webhooks (`custom.go`)
- **Meta Channels**: Group channels (`group.go`) combine multiple channels, OneBot protocol (`one-bot.go`)
- **Cloud Services**: Tencent Alarm (`tencent-alarm.go`)

Each channel type has its own handler in `channel/` directory. The main dispatcher (`channel/main.go`) routes messages to appropriate handlers based on channel type.

### Frontend

React SPA with modern tooling:
- **UI Framework**: Semantic UI React components
- **Routing**: React Router v6 for navigation
- **HTTP Client**: Axios for API communication
- **Real-time**: Server-Sent Events for live updates
- **Code Quality**: Prettier for formatting (configured in package.json)
- **Proxy**: Development server proxies backend at `http://localhost:3000`

Build artifacts are embedded in Go binary via `//go:embed web/build`, eliminating the need for separate static file serving.

## Configuration

**Environment Variables:**
- `REDIS_CONN_STRING`: Redis connection for rate limiting
- `SESSION_SECRET`: Fixed session key for cookie persistence
- `SQL_DSN`: MySQL connection string (optional)
- `GIN_MODE`: Set to "debug" for development
- `PORT`: Server port (default 3000)

**Command Line Arguments:**
- `--port`: Server port
- `--log-dir`: Log directory path
- `--version`: Show version

## API Usage

The service provides a unified API for message sending:

**Endpoint**: `POST /push/{username}` or `GET /push/{username}`

**Key Parameters**:
- `title`: Message title (optional)
- `description` or `desp`: Message content (required)
- `content`: Markdown content (optional)
- `channel`: Target channel name (uses default if not specified)
- `token`: Authentication token (required if configured)
- `async`: Set to `true` for background processing
- `to`: Target recipients (`@all` for all users, `user1|user2` for specific users)

**Channel Types**: `email`, `test`, `corp_app`, `lark_app`, `corp`, `lark`, `ding`, `bark`, `client`, `telegram`, `discord`, `group`, `custom`, `tencent_alarm`, `none`

## Development Notes

- **Authentication**: Default admin account `root`/`123456` (change immediately)
- **Port Configuration**: Frontend dev (3001) → Backend (3000)
- **WebSocket Production**: Requires Nginx timeout config (`proxy_read_timeout 300s`)
- **Message Processing**: Supports both sync and async modes via `async` parameter
- **Webhook Integration**: Reverse compatibility with Server酱 and other services
- **Database Migration**: GORM auto-migration runs on startup
- **Security**: Token-based API authentication with channel-specific and global tokens
- **Embedded Assets**: Frontend build is embedded in Go binary for single-file deployment