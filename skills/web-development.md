---
description: Web development patterns for full-stack applications. Framework-agnostic best practices for frontend, backend, testing, and deployment. Auto-applies when working with web technologies.
globs:
  - "**/*.html"
  - "**/*.css"
  - "**/*.scss"
  - "**/*.jsx"
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.svelte"
  - "**/next.config.*"
  - "**/vite.config.*"
  - "**/webpack.config.*"
  - "**/package.json"
  - "**/tsconfig.json"
---

# Web Development Skill

## Overview

Framework-agnostic best practices for building web applications. Covers frontend, backend, testing, deployment, and browser automation.

## When This Skill Applies

- Building or modifying web applications (React, Vue, Svelte, etc.)
- Setting up APIs or backend services
- Writing frontend/backend tests
- Browser automation and testing
- Performance optimization

## Available Tools

- **Playwright MCP**: Browser automation and testing
- **Puppeteer**: Headless browser with anti-detection
- **Daytona**: Container sandbox for full-stack development
- **Omnisearch**: Search for libraries, patterns, solutions
- **Context7**: Live documentation for web frameworks
- **mcpdoc**: Documentation via llms.txt endpoints
- **E2B**: Cloud sandbox for quick prototyping

## Frontend Patterns

### Component Architecture

- Keep components small and focused (single responsibility)
- Separate presentation from logic
- Use composition over inheritance
- Co-locate styles, tests, and types with components

### State Management

- Start with local state; lift only when needed
- Use framework-native solutions first (React Context, Vue provide/inject)
- Add external state management only for complex shared state
- Keep server state separate from UI state

### Performance

- Lazy load routes and heavy components
- Optimize images (WebP, proper sizing, lazy loading)
- Minimize bundle size (tree shaking, code splitting)
- Use proper caching headers and service workers

## Backend Patterns

### API Design

- Use RESTful conventions or GraphQL consistently
- Version APIs from the start
- Return consistent error shapes
- Implement proper pagination for list endpoints

### Database

- Use migrations for schema changes
- Add indexes for frequently queried columns
- Use connection pooling
- Implement proper error handling for DB operations

### Authentication

- Use established libraries (next-auth, passport, lucia)
- Store sessions server-side or use signed JWTs
- Implement CSRF protection for cookie-based auth
- Rate limit authentication endpoints

## Testing Strategy

### Browser Testing with Playwright

Use Playwright MCP for end-to-end testing:

- Test critical user journeys
- Visual regression testing
- Cross-browser compatibility
- Accessibility audits

### Test Pyramid

- **Unit tests**: Fast, isolated, cover business logic
- **Integration tests**: API endpoints, database queries
- **E2E tests**: Critical user flows via Playwright
- **Visual tests**: Screenshot comparison for UI changes

## Development Workflow

1. **Check docs first**: Use Context7 or mcpdoc for framework documentation
2. **Prototype in sandbox**: Use E2B or Daytona for quick experiments
3. **Build incrementally**: Small PRs, frequent commits
4. **Test continuously**: Run tests after each change
5. **Validate in browser**: Use Playwright for visual verification

## Security Checklist

- Sanitize all user inputs
- Use parameterized queries (never string concatenation for SQL)
- Set proper CORS headers
- Implement Content Security Policy
- Use HTTPS everywhere
- Validate and escape output (prevent XSS)
- Keep dependencies updated

## Best Practices

- Use TypeScript for type safety
- Implement proper error boundaries
- Add loading and error states for async operations
- Follow accessibility guidelines (WCAG 2.1)
- Use semantic HTML elements
- Implement responsive design from the start
- Set up linting and formatting (ESLint, Prettier)
