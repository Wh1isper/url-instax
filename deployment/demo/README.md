# URL-Instax Docker Deployment

This directory contains the necessary files to deploy URL-Instax using Docker Compose with Caddy as a reverse proxy.

## Files

- `docker-compose.yaml`: The main Docker Compose configuration file
- `Caddyfile`: Configuration for the Caddy reverse proxy
- `Dockerfile.caddy`: Dockerfile to build Caddy with Cloudflare DNS provider
- `.env.example`: Example environment variables file (copy to `.env` and update with your values)

## Setup Instructions

1. Copy the example environment file and update it with your values:

```bash
cp .env.example .env
```

2. Edit the `.env` file and update the following variables:

   - `API_TOKEN`: A secure token for URL-Instax API authentication
   - `DOMAIN`: Your domain name (e.g., instax.example.com)
   - `CURRENT_SERVER_LOCATION`: The location of your server (e.g., `http://localhost:8890`, etc.)
   - `CLOUDFLARE_API_TOKEN`: Your Cloudflare API token with DNS edit permissions
   - `CLOUDFLARE_ZONE_ID`: Your Cloudflare Zone ID for the domain

1. Start the services:

```bash
docker compose up -d
```

## Cloudflare API Token Setup

To create a Cloudflare API token with the necessary permissions:

1. Log in to your Cloudflare dashboard
1. Go to "My Profile" > "API Tokens"
1. Click "Create Token"
1. Use the "Edit zone DNS" template
1. Under "Zone Resources", select "Include" > "Specific zone" > your domain
1. Click "Continue to summary" and then "Create Token"
1. Copy the token to your `.env` file

## Cloudflare Zone ID

To find your Cloudflare Zone ID:

1. Log in to your Cloudflare dashboard
1. Select your domain
1. The Zone ID is displayed on the right side of the "Overview" page
1. Copy the Zone ID to your `.env` file

## Accessing URL-Instax

Once deployed, URL-Instax will be available at:

```
https://your-domain.com
```

The API endpoints will be available at:

```
https://your-domain.com/api/v1/screenshot
```
