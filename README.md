# MSPAlwaysOn

MSPAlwaysOn is a comprehensive AIOps and alert management platform designed specifically for Managed Service Providers (MSPs). It provides a unified platform for MSP operations, bringing together alerts, tickets, and automation workflows from all your tools into a single, powerful interface.

## Overview

MSPAlwaysOn is a comprehensive AIOps and alert management platform designed specifically for Managed Service Providers (MSPs). It provides a unified platform for MSP operations, bringing together alerts, tickets, and automation workflows from all your tools into a single, powerful interface. It's built from the ground up to address the unique challenges faced by MSPs managing multiple client environments.

## Key Features

- **Unified Alert Management**: Centralize alerts from all your MSP tools into a single, powerful interface
- **MSP-Specific Integrations**: Connect with ConnectWise, SentinelOne, Veeam, and more, with a simple, extensible integration framework
- **AI-Powered Automation**: Leverage advanced AIOps capabilities for intelligent automation
- **Client-Aware Operations**: Manage alerts and tickets with full client context
- **Custom MSP Workflows**: Automate common MSP scenarios with declarative workflows, with a simple, extensible workflow engine

## Architecture

MSPAlwaysOn is built with a modern, scalable architecture:

1. **Modular Backend**: Robust alert management, correlation, and workflow execution engine
2. **MSP-Specific Data Model**: Purpose-built data models for clients, sites, assets, and more
3. **Intuitive Frontend**: Clean, responsive UI designed specifically for MSP technicians and managers
4. **Extensible Integration Framework**: Easy-to-implement provider system for connecting to any MSP tool

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/paulhshort/MSPAlwaysOn.git
   cd MSPAlwaysOn
   ```

2. Start the development environment:
   ```
   docker-compose up -d
   ```

3. Access the applications:
   - MSPAlwaysOn Frontend: `http://localhost:3001`
   - MSPAlwaysOn API: `http://localhost:8000`

## Development

See the [Integration Plan](docs/integration_plan.md) for detailed information about the development roadmap and integration approach.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Keep.dev](https://github.com/keephq/keep) - An open-source AIOps platform that provided inspiration for some components
- [Tremor](https://www.tremor.so/) - React UI components for dashboards
- [FastAPI](https://fastapi.tiangolo.com/) - High-performance API framework
- [Next.js](https://nextjs.org/) - React framework for the frontend
